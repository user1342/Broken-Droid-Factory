import os
import random
import re
import randomword


class patcher():
    '''
    An interface to be inherited by other patchers, including shared features.
    All patchers should also have a difficulty and a patch function (patch functions should return a string detailing what they did).
    '''
    name = None
    difficulty = None
    working_dir = None
    is_verbose = False

    def _get_path_to_file(self, file_name_to_find, dir_to_start_search=None):
        if dir_to_start_search == None:
            dir_to_start_search = self.working_dir

        for subdir, dirs, files in os.walk(dir_to_start_search):
            for file in files:
                file_path = str(os.path.join(subdir, file))
                if file == file_name_to_find:
                    return file_path

    def _add_java_code_to_file(self, path_to_file, code_to_add_as_string,
                               line_to_add_after='''setContentView(R.layout.activity_main);'''):
        lines = None
        with open(path_to_file, "r") as file:
            lines = file.readlines()

        line_to_add_to = 0
        for line in lines:
            if line_to_add_after in line:
                line_to_add_to = line_to_add_to + 1
                break
            line_to_add_to = line_to_add_to + 1

        new_data_as_list = [code_to_add_as_string]
        lines_to_write = lines[:line_to_add_to] + ["\n"] + new_data_as_list + ["\n"] + lines[line_to_add_to:]

        with open(path_to_file, "w") as file:
            file.writelines(lines_to_write)

    def _add_imports_to_java_file(self, path_to_java_file, import_as_string):
        lines = None
        with open(path_to_java_file, "r") as file:
            lines = file.readlines()

        found_import = False
        for line in lines:
            if import_as_string in line:
                found_import = True

        if not found_import:
            new_data_as_list = [import_as_string]
            lines_to_write = [lines[0]] + ["\n"] + new_data_as_list + ["\n"] + lines[1:]

            with open(path_to_java_file, "w") as file:
                file.writelines(lines_to_write)

    def _get_random_java_code_block(self):

        var_one_identifier = "{}{}".format(str(randomword.get_random_word()).capitalize(), random.randint(0, 1000))

        reflection_code_block = ['''import android.util.Log;import java.lang.reflect.Method;''',
                                 '''Method[] methods{} = this.getClass().getDeclaredMethods();
                                 for (Method method : methods{}) {{
                                     Log.v("{}", method.getName());
                                 }}'''.format(var_one_identifier, var_one_identifier, randomword.get_random_word())]

        log_code_block = ['''import android.util.Log;''',
                          'Log.{}("{}","{}");'.format(random.choice(["d", "e", "i", "v", "wtf"]),
                                                      randomword.get_random_word(), randomword.get_random_word())]

        toast_code_block = ['''import android.widget.Toast;''',
                            '''Toast.makeText(getApplicationContext(),"{}",Toast.{}).show();'''.format(
                                randomword.get_random_word(), random.choice(["LENGTH_SHORT", "LENGTH_LONG"]))]

        intent_code_block = ['''import android.content.Intent;''', '''Intent launchIntent{} = getPackageManager().getLaunchIntentForPackage("com.android.chrome");
        startActivity(launchIntent{});'''.format(var_one_identifier, var_one_identifier)]

        code_blocks = [reflection_code_block, log_code_block, toast_code_block, intent_code_block]

        return random.choice(code_blocks)

    def get_all_current_components_from_activity_path(self, path_to_activity=None):
        if path_to_activity == None:
            path_to_activity = os.path.join(self.working_dir, "app", "src", "main", "res", "layout",
                                            "activity_main.xml")

        activiy_file = open(path_to_activity, "r")
        activity_data = activiy_file.read()
        activiy_file.close()

        ids = re.findall(r'@\+id/(.+)', activity_data)

        return ids

    def logger(self, string_to_print):
        if self.is_verbose:
            print(string_to_print)

    def _generate_activity_xml(self, activity_name="MainActivity"):
        number_of_elements = random.randint(1, 10)

        string_builder = '''<?xml version="1.0" encoding="utf-8"?>
    <androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".{}">'''.format(activity_name)

        for iterator in range(0, number_of_elements):
            string_builder = string_builder + "\n\n{}".format(self._generate_random_xml_activity_component())

        string_builder = string_builder + "\n\n</androidx.constraintlayout.widget.ConstraintLayout>"
        return string_builder

    def _generate_random_xml_activity_component(self, id=None):

        if id == None:
            id = randomword.get_random_word() + str(random.randint(24, 400))

        text_view_xml = '''<TextView
        android:id="@+id/textView{}"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{}"
        android:textSize="{}sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />'''.format(id, randomword.get_random_word(),
                                                               random.randint(24, 400))

        button_view_xml = '''<Button
                android:id="@+id/button{}"
                android:layout_width="{}dp"
                android:layout_height="{}dp"
                android:layout_marginTop="{}dp"
                android:text="{}"
                app:layout_constraintEnd_toEndOf="parent"
                app:layout_constraintHorizontal_bias="0.542"
                app:layout_constraintStart_toStartOf="parent"
                app:layout_constraintTop_toTopOf="parent" />'''.format(id, random.randint(40, 400),
                                                                       random.randint(40, 400),
                                                                       random.randint(40, 400),
                                                                       randomword.get_random_word())

        image_view_xml = '''<ImageView
        android:id="@+id/imageView{}"
        android:layout_width="{}dp"
        android:layout_height="{}dp"
        android:layout_marginEnd="{}dp"
        android:layout_marginBottom="{}dp"
        app:layout_constraintBottom_toTopOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:srcCompat="@drawable/ic_launcher_foreground" />'''.format(id, random.randint(40, 400),
                                                                      random.randint(40, 400),
                                                                      random.randint(40, 400),
                                                                      random.randint(40, 400))

        edit_text_view_xml = '''<EditText
        android:id="@+id/editTextTextPersonName{}"
        android:layout_width="{}dp"
        android:layout_height="{}dp"
        android:layout_marginTop="{}dp"
        android:layout_marginBottom="{}dp"
        android:ems="10"
        android:inputType="textPersonName"
        android:text="{}"
        app:layout_constraintBottom_toTopOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />'''.format(id, random.randint(40, 400), random.randint(40, 400),
                                                               random.randint(40, 400),
                                                               random.randint(40, 400), randomword.get_random_word())

        list_of_views = [text_view_xml, button_view_xml, image_view_xml, edit_text_view_xml]

        return random.choice(list_of_views)

    def _replace_everywhere(self, string_to_replace, new_string):
        # To minimise conflicts these are done seperately
        # Replace file content
        for subdir, dirs, files in os.walk(self.working_dir):
            for file in files:
                file = str(os.path.join(subdir, file))
                self._replace_in_file(file, string_to_replace, "{}".format(new_string))

        # Rename files
        for subdir, dirs, files in os.walk(self.working_dir):
            for file in files:
                file_path = str(os.path.join(subdir, file))
                if string_to_replace in file:
                    os.rename(file_path, str(file).replace(string_to_replace, new_string))

        # rename dirs
        for subdir, dirs, files in os.walk(self.working_dir):
            if string_to_replace in subdir:
                name_to_replace = str(subdir).replace(string_to_replace, new_string)
                os.rename(subdir, name_to_replace)

    def _replace_in_file(self, file_path, string_to_remove, string_to_replace):
        fin = open(file_path, "rt")
        try:
            data = fin.read()
        except UnicodeDecodeError:
            return
        data = data.replace(string_to_remove, string_to_replace)
        fin.close()
        fin = open(file_path, "wt")
        fin.write(data)
        fin.close()

    def __init__(self, name, working_dir, verbosity=False):
        self.name = name
        self.working_dir = working_dir
        self.is_verbose = verbosity

    def patch(self):
        raise ("A patcher has been used that does not have an implemented patch function")
