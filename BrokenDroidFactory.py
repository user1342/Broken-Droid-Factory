import argparse
import os.path
import random
import shutil
import subprocess
from distutils.dir_util import copy_tree
import randomword
import patchers.broken_crypto_patcher
import patchers.common_patcher
import patchers.exported_intent_patcher
import patchers.data_in_memory_patcher

patcher_list = [patchers.common_patcher.common_patcher, patchers.broken_crypto_patcher.broken_crypto_patcher,
                patchers.exported_intent_patcher.exported_intent_patcher, patchers.data_in_memory_patcher.data_in_memory]


def delete_dir(dir_path):
    '''
    A helper function used for deleting all files inside of a dir and then deleting the dir itself.
    :param dir_path: The path to be deleted
    '''
    if os.path.isdir(dir_path):
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                raise Exception(
                    'Failed to delete %s, as part of previous working dir cleanup. Reason: %s. Please attempt to delete manually.' % (
                        file_path, e))

        os.rmdir(dir_path)


class BrokenDroidFactory():
    '''
    This function controls the processing of BDF and it's inner workings.
    '''
    is_verbose = False
    output_path = None
    template_path = None
    working_dir = None
    challenge_level = 0
    app_name = None

    def logger(self, text):
        '''
        A wrapper around print that will only print to the console if the verbose flag is true.
        :param text: The text to print if in verbose mode.
        :return:
        '''
        if self.is_verbose:
            print(text)

    def __init__(self, verbosity, template_path, output_dir, challenge_level, working_dir):
        '''
        Constructor
        :param verbosity: if in verbose mode
        :param template_path: the path of the directory that contains the stock android application source
        :param output_dir: the directory to save the output APK and README to
        :param challenge_level: the target challenge level for the apk to be created
        :param working_dir: the temp directory that is used to store the modifications to the template code
        '''
        self.is_verbose = verbosity
        self.template_path = template_path
        self.output_path = output_dir
        self.working_dir = working_dir
        self.challenge_level = challenge_level
        self.app_name = str("{}{}".format(str(randomword.get_random_word()).capitalize(),
                                          str(randomword.get_random_word()).capitalize()))
        self.logger(
            "Verbosity set to '{}'\nTemlplate path set to '{}', \nOutput patch set to '{}' \nWorking dir set to '{}' \nChallenge level set to '{}'".format(
                verbosity, template_path, output_path, working_dir, challenge_level
            ))

    def copy_template_to_working_dir(self):
        '''
        This function takes a one for one copy of the source code in the template dir and copies it to the working directory.
        '''
        working_dir = self.working_dir
        template_dir = self.template_path

        # Delete working dir if it already exists
        delete_dir(working_dir)
        os.mkdir(working_dir)

        # copy template dir to working dir
        copy_tree(template_dir, working_dir)

    def modify_working_dir_app(self):
        '''
        During this stage modifications are made to the working directory source code. Including patching to add vulnerabilities and standard modifications including changing the name of the app.
        return: notes: A list of strings that contain hints for how to identify the issues/ vulnerabilities present in the created application
        '''
        chosen_patchers = []
        random.shuffle(patcher_list)
        current_difficulty = 0
        # Loop through all potential patchers

        # Loop through all 0 difficulty patchers first (i.e. common_patcher.py)
        for patcher in patcher_list:
            if patcher.difficulty == 0:
                patcher = patcher(self.app_name, self.working_dir, self.is_verbose)
                chosen_patchers.append(patcher)

        # Then loop through all patchers that come with a difficulty level
        while current_difficulty <= self.challenge_level:
            # Continue looping untill the difficulty challenge level is reached
            for patcher in patcher_list:
                patcher = patcher(self.app_name, self.working_dir, self.is_verbose)
                # Add all patchers that have a difficulty of 0.
                if patcher.difficulty != 0 and current_difficulty + patcher.difficulty <= self.challenge_level:
                    chosen_patchers.append(patcher)

                current_difficulty = current_difficulty + patcher.difficulty

        # Patch chosen patchers
        notes = []
        for patcher in chosen_patchers:
            notes.append(patcher.patch())

        return notes

    def build_working_dir_app(self, notes):
        '''
        During this stage the source code in the working diretcory is built using gradle.
        :param notes: A list of strings that contain hints for how to identify the issues/ vulnerabilities present in the created application
        '''
        self.logger("Building APK - at '{}'".format(self.working_dir))
        current_cwd = os.getcwd()
        os.chdir(self.working_dir)
        build_command = [os.path.join(".", "gradlew"), "assembledebug"]
        result = subprocess.run(build_command, stdout=subprocess.PIPE, shell=True)

        build_result = result.stdout
        if not "BUILD SUCCESSFUL" in str(build_result):
            raise Exception(
                "Failed to build target APK: \n - Working Directory: {} \n - Command Run: {}".format(self.working_dir,
                                                                                                     build_command))
        else:
            self.logger("APK built, copying to output dir")
            os.mkdir(os.path.join(current_cwd, self.output_path))
            apk_name = str(self.app_name + ".apk")
            shutil.copyfile(os.path.join("app", "build", "outputs", "apk", "debug", "app-debug.apk"),
                            os.path.join(current_cwd, self.output_path, apk_name))

        os.chdir(current_cwd)

        # Delete working dir
        delete_dir(self.working_dir)

        running_directory = os.listdir(".")

        # Delete any artifacts
        for item in running_directory:
            if item.endswith(".iml"):
                os.remove(os.path.join(item))

        # Create notes output markdown file
        notes_file = open(os.path.join(self.output_path, "README.md"), "w")
        self.logger("Generating notes readme file at '{}'".format(notes_file.name))
        notes_file.write("# BDF Pseudo Random Vulnerable Android Application Report ({})\n".format(self.app_name))
        notes_file.write(
            "This README has been created as part of the pseudo randon vulnerable app creation as par of the [Broken Droid Factory](https://github.com/user1342/Broken-Droid-Factory) generation.\n")
        notes_file.write(
            "The goal of the created application is to identify the security misconfigurations present inside of the APK.\n")
        notes_file.write("## Run Configuration\n")
        notes_file.write(
            "- **Verbosity** set to: '{}'\n\n - **Temlplate path** set to: '{}', \n\n - **Output path** set to '{}' \n\n - **Working dir** set to: '{}' \n\n - **Challenge level** set to: '{}'\n\n - **App name** of: '{}'\n".format(
                self.is_verbose, self.template_path, self.output_path, self.working_dir, self.challenge_level, self.app_name))
        notes_file.write("## Vulnerable App Configuration Notes\n")
        notes_file.write(
            "Only read the below if you want a hint on the security misconfigurations inside of the vulnerable APK")

        # remove duplicates from notes. TODO remove this when it's nolonger needed
        notes = list(dict.fromkeys(notes))

        for line in notes:
            line_to_add = "- " + line + "\n\n"
            notes_file.write("- " + line + "\n\n")
        notes_file.close()


if __name__ == '__main__':
    '''
    Entrypoint for BDF
    '''

    # Set and get args
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=str,
                        help="The output directory for the compiled APK to be saved to.")
    parser.add_argument("-t", "--template", type=str,
                        help="The path to the template app. Do not alter unless you know what you're doing.")
    parser.add_argument("-c", "--challenge", type=int,
                        help="The desired challenge level for the created APK.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Increase output verbosity")

    args = parser.parse_args()

    output_path = args.output
    template_path = args.template
    challenge_level = args.challenge
    verbosity = args.verbose

    # Set a random challenge level if one has not been set
    if challenge_level == None:
        challenge_level = random.randint(4, 10)

    # Define the default app path
    if template_path == None:
        template_path = f"{os.path.dirname(os.path.abspath(__file__))}/demoapp"
        if not os.path.isdir(template_path):
            raise Exception(
                "No template APK path given and default path of '{}' cannot be found.".format(template_path))
        if not os.path.isfile(os.path.join(template_path, "gradlew")):
            raise Exception("Template ('{}') is not a valid Android application source directory".format(template_path))

    # Check if an output dir is given, if not use default 'out'
    if output_path == None:
        output_path = f"{os.path.dirname(os.path.abspath(__file__))}/out"
    # If output dir doesn't exist, create it.
    if os.path.isdir(output_path):
        delete_dir(output_path)

    # Set working dir
    work_dir = f"{os.path.dirname(os.path.abspath(__file__))}/working_dir"

    # Initialise BDF and go through the BDF steps
    print("Starting Broken Droid Factory (this may take some time)...")
    builder = BrokenDroidFactory(verbosity, template_path, output_path, challenge_level, work_dir)
    builder.copy_template_to_working_dir()
    notes = builder.modify_working_dir_app()
    builder.build_working_dir_app(notes)
    print("Broken Droid Factory completed, outputs saved to: '{}'".format(output_path))
