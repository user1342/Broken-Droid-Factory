import os
import random

import randomword

from patchers import patcher_interface


class common_patcher(patcher_interface.patcher):
    '''
    This patcher is used to perform standard alterations to the app, including modifying the name, creating a more interesting activity, and adding red herring code to the MainActivity.
    '''
    difficulty = 0

    def patch(self):
        '''
        Patch the source code to alter the app name, and main activity
        :return: a string of notes for this patch
        '''
        # Change app name and reverse domain notation
        self.logger("Patching out template app name to new name '{}'".format(self.name))
        self._replace_everywhere("demo_app", self.name.lower())
        reverse_domain = "{}.{}".format(random.choice(["com", "org", "me", "net"]), randomword.get_random_word())
        self._replace_everywhere("com.example", reverse_domain)
        self._replace_everywhere("demo-app", self.name.upper())

        # Create a custom main activity
        self.logger("Creating a pseudo random main activity. ")
        new_main_activity_xml = self._generate_activity_xml()
        main_activity_path = os.path.join(self.working_dir, "app", "src", "main", "res", "layout", "activity_main.xml")
        file_to_modify = open(main_activity_path, "w")
        file_to_modify.write(new_main_activity_xml)
        file_to_modify.close()

        # Add pseudo random code to MainActivity.java
        MainActivity_file_path = self._get_path_to_file("MainActivity.java")
        self.logger("Generating pseudo random code for MainActivity.java")
        for iterator in range(1, 40):
            code_block = self._get_random_java_code_block()
            import_code = code_block[0]
            code = code_block[1]
            self._add_imports_to_java_file(MainActivity_file_path, import_code)
            self._add_java_code_to_file(MainActivity_file_path, code)

        return "The application '{}' has been crafted and several vulnerabilities hidden amoung it.".format(self.name)
