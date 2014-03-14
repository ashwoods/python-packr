import os
import shutil

import unittest

from packr import Packr

TEST_INSTALL_ROOT_FOLDER = 'test_root'

class PackrTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(TEST_INSTALL_ROOT_FOLDER):
            os.mkdir(TEST_INSTALL_ROOT_FOLDER)

    def test_missing_values_in_setup_file(self):
        pass

    def test_source_by_path(self):
        pass

    def test_dest_dir_env_var_set(self):
        packr = Packr(destdir="/opt/user")
        packr.setup()
        assertEquals(packr.destdir, os.env['DH_VIRTUALENV_INSTALL_ROOT'])
    
    def test_python(self):
        pass

    def test_user(self):
        pass

    @classmethod
    def tearDownClass(cls):    
        shutil.rmtree(TEST_INSTALL_ROOT_FOLDER)
    
if __name__ == '__main__':
    unittest.main()
