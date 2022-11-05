import random

import randomword

from patchers import patcher_interface


class data_in_memory(patcher_interface.patcher):
    '''
    Adds code that displays having data in memory
    '''
    difficulty = 1

    def patch(self):
        '''
        Adds Java code to display having unknown data from a static re perspective be stored in memory.
        '''

        self.logger("Adding encryption of device data in memory")
        str_builder_name = "{}{}".format(randomword.get_random_word(), random.randint(0, 1000))

        list_of_data_calls = [
            'stringBuilder{}.append(Build.DEVICE).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.MODEL).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.PRODUCT).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.BOARD).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.getRadioVersion()).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.BOOTLOADER).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.DISPLAY).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.FINGERPRINT).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.HARDWARE).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.HOST).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.ID).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.MANUFACTURER).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.TAGS).append(" ");\n'.format(str_builder_name),
            'stringBuilder{}.append(Build.TYPE).append(" ");\n'.format(str_builder_name)]

        str_builder = 'StringBuilder stringBuilder{} = new StringBuilder();\n'.format(str_builder_name)
        for iterator in range(0, random.randint(0, 40)):
            str_builder = str_builder + random.choice(list_of_data_calls) + "\n"

        string_name = "{}{}".format(randomword.get_random_word(), random.randint(0, 1000))
        str_builder = str_builder + "String plainTextString{} = stringBuilder{}.toString();\n".format(string_name,
                                                                                                      str_builder_name)
        str_builder = str_builder + '''try {
            TimeUnit.SECONDS.sleep(30);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }'''

        str_builder = str_builder + '''try {{
            Cipher cipher{cipher_var} = null;
            cipher{cipher_var} = Cipher.getInstance("AES/CBC/PKCS5PADDING");
            KeyGenerator keygen{keygen_var} = null;
            keygen{keygen_var} = KeyGenerator.getInstance("AES");
            keygen{keygen_var}.init(256);
            SecretKey key{key_var} = keygen{keygen_var}.generateKey();

            byte[] plainText{plaintext_var} = plainTextString{string_var}.getBytes();
            cipher{cipher_var}.init(Cipher.ENCRYPT_MODE, key{key_var});
            byte[] cipherText{ciphertext_var} = new byte[0];
            cipherText{ciphertext_var} = cipher{cipher_var}.doFinal(plainText{plaintext_var});

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {{
                Log.v(getApplicationContext().getPackageName(), "Encrypted Data: "+Base64.getEncoder().encodeToString(cipherText{ciphertext_var}));
            }}

        }}catch (NoSuchAlgorithmException | InvalidKeyException | NoSuchPaddingException | IllegalBlockSizeException | BadPaddingException e) {{
            e.printStackTrace();
        }}\n'''.format(cipher_var=randomword.get_random_word() + str(random.randint(0, 1000)),
                       keygen_var=randomword.get_random_word() + str(random.randint(0, 1000)),
                       key_var=randomword.get_random_word() + str(random.randint(0, 1000)),
                       plaintext_var=randomword.get_random_word() + str(random.randint(0, 1000)),
                       string_var=string_name,
                       ciphertext_var=randomword.get_random_word() + str(random.randint(0, 1000)))

        code_block = [
            '''import android.os.Build; import android.util.Log; import java.security.InvalidKeyException;import java.security.NoSuchAlgorithmException;import java.util.Base64;import java.util.concurrent.TimeUnit;import javax.crypto.BadPaddingException;import javax.crypto.Cipher;import javax.crypto.IllegalBlockSizeException;import javax.crypto.KeyGenerator;import javax.crypto.NoSuchPaddingException;import javax.crypto.SecretKey;''',
            str_builder]

        mainActivity_file_path = self._get_path_to_file("MainActivity.java")
        self._add_imports_to_java_file(mainActivity_file_path, code_block[0])
        self._add_java_code_to_file(mainActivity_file_path, code_block[1])

        return "A series of device paramiters are being pulled off the device and immediately encrypted. However, are they in memory long enough for the data to be dumped?"
