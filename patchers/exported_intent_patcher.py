import os.path
import random
import re

from patchers import patcher_interface


class exported_intent_patcher(patcher_interface.patcher):
    '''
    Removes a random intent filter
    '''
    difficulty = 1

    def patch(self):
        '''
        A simple patch to remove an intent filter from an exported activity
        '''

        self.logger("Removing an intent filter from an exported activity")
        path_to_android_manifest = self._get_path_to_file("AndroidManifest.xml", os.path.join(self.working_dir,"app","src","main"))
        manifest_file = open(path_to_android_manifest, "r")
        manifest_file_data = manifest_file.read()
        manifest_file.close()

        manifest_file_data = re.sub(r'(android:exported="true">(((.|\n)*)<\/intent-filter>))','android:exported="true">', manifest_file_data)

        manifest_file = open(path_to_android_manifest, "w")
        manifest_file.write(manifest_file_data)
        manifest_file.close()

        return "An activity is exported but does not have any active intent filters."

        # TODO: Add patch to add an exported True flag to an activity