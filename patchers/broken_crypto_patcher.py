import hashlib
import random
import randomword
from patchers import patcher_interface


class broken_crypto_patcher(patcher_interface.patcher):
    '''
    Adds vulnerable code to the main activity of the application relating to broken crypto configurations
    '''
    difficulty = 1

    def _introduce_insecure_algo(self):
        '''
        This function will modify the working dir source to introduce an insecure algorithm usage inside of the app.
        :return: notes as a string
        '''

        algo_options = ["SHA1", "MD4", "MD5"]
        chosen_algo = random.choice(algo_options)

        hash = None
        if chosen_algo == "SHA1":
            # SHA1
            hashable_string = str.encode(randomword.get_random_word())
            hash_object = hashlib.sha1(hashable_string)
            hash = hash_object.hexdigest()

        elif chosen_algo == "MD4":
            text = randomword.get_random_word()
            hashObject = hashlib.new('md4', text.encode('utf-8'))
            hash = hashObject.hexdigest()

        elif chosen_algo == "MD5":
            # MD5
            hashable_string = str.encode(randomword.get_random_word())
            hash = hashlib.md5(hashable_string)

        text_options = ["log", "toast", "string"]
        chosen_text_option = random.choice(text_options)

        code_block = None

        if chosen_text_option == "log":
            code_block = ["import android.util.Log;",
                          'Log.{}("{}","{}");'.format(random.choice(["d", "e", "i", "v", "wtf"]),
                                                      randomword.get_random_word(), hash)]
        elif chosen_text_option == "toast":
            code_block = ["import android.widget.Toast;",
                          '''Toast.makeText(getApplicationContext(),"{}",Toast.{}).show();'''.format(hash,
                                                                                                     random.choice([
                                                                                                                       "LENGTH_SHORT",
                                                                                                                       "LENGTH_LONG"]))]
        elif chosen_text_option == "string":
            var_name = "{}{}".format(str(randomword.get_random_word()).upper(), random.randint(1, 1000))
            code_block = ["", 'String {} = "{}";'.format(var_name, hash)]

        mainActivity_file_path = self._get_path_to_file("MainActivity.java")
        self._add_imports_to_java_file(mainActivity_file_path, code_block[0])
        self._add_java_code_to_file(mainActivity_file_path, code_block[1])

        return "A {} hash has been left in the APK in a {} code block".format(chosen_algo, chosen_text_option)

    def _introduce_predictable_key(self):
        '''
        The function will modify the code in the working dir by introducing a predictable key code block.
        :return: notes
        '''

        var_one = "{}{}".format(randomword.get_random_word(), random.randint(0, 1000))

        code_block = [
            '''import java.security.InvalidKeyException; import java.security.NoSuchAlgorithmException; import java.security.spec.InvalidKeySpecException; import java.util.Base64; import javax.crypto.BadPaddingException; import javax.crypto.Cipher; import javax.crypto.IllegalBlockSizeException; import javax.crypto.NoSuchPaddingException; import javax.crypto.SecretKey; import javax.crypto.SecretKeyFactory; import javax.crypto.spec.DESKeySpec;''',
            '''String password{password_var} = "{password_text}";

        try {{
            DESKeySpec keySpec{key_spec_var} = new DESKeySpec("{key_text}".getBytes());
            SecretKeyFactory keyFactory{key_factory_var} = SecretKeyFactory.getInstance("DES");
            SecretKey key{key_var} = keyFactory{key_factory_var}.generateSecret(keySpec{key_spec_var});
            byte[] cleartext{clear_text_var} = password{password_var}.getBytes();

            Cipher cipher{cipher_var} = Cipher.getInstance("DES"); // cipher is not thread safe
            cipher{cipher_var}.init(Cipher.ENCRYPT_MODE, key{key_var});
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {{
                String encrypted{encrypted_var} = Base64.getEncoder().encodeToString(cipher{cipher_var}.doFinal(cleartext{clear_text_var}));
                Log.v("Encrypted Message", encrypted{encrypted_var});
            }}

        }} catch (NoSuchPaddingException | IllegalBlockSizeException | NoSuchAlgorithmException | InvalidKeySpecException | BadPaddingException | InvalidKeyException e) {{
            e.printStackTrace();
        }}'''.format(password_var=randomword.get_random_word() + str(random.randint(0, 100)),
                     password_text=randomword.get_random_word(),
                     key_spec_var=randomword.get_random_word() + str(random.randint(0, 100)),
                     key_text=randomword.get_random_word(),
                     key_var=randomword.get_random_word() + str(random.randint(0, 100)),
                     key_factory_var=randomword.get_random_word() + str(random.randint(0, 100)),
                     clear_text_var=randomword.get_random_word() + str(random.randint(0, 100)),
                     cipher_var=randomword.get_random_word() + str(random.randint(0, 100)),
                     encrypted_var=randomword.get_random_word() + str(random.randint(0, 100))

                     )]

        mainActivity_file_path = self._get_path_to_file("MainActivity.java")
        self._add_imports_to_java_file(mainActivity_file_path, code_block[0])
        self._add_java_code_to_file(mainActivity_file_path, code_block[1])

        return "The application logs a DES encrypted password to Logcat. Find the key and identify why this is an insecure method of encryption."

    def patch(self):
        '''
        Adds a vulnerable/ insecure code block to the main activity
        :return: notes
        '''

        options = ["insecure", "predictable"]
        chosen_option = random.choice(options)

        if chosen_option == "insecure":
            self.logger("Introducing an insecure algorithem issue")
            return self._introduce_insecure_algo()
        elif chosen_option == "predictable":
            self.logger("Introducing a predictable algorithm issue")
            return self._introduce_predictable_key()
