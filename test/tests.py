import os
import shutil

import unittest
from subprocess import call

from packr import Packr

TEST_INSTALL_ROOT_FOLDER = '/opt/packr-test'
TEST_PYTHON_PROJECT_PATH = './test/django-polls'
INSTALL_DIR_ENV_VAR = 'DH_VIRTUALENV_INSTALL_ROOT'

class PackrTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass

    def test_missing_values_in_setup_file(self):
        pass

    def test_source_by_path(self):
        pass

    def test_dest_dir_env_var_set(self):
        packr = Packr(destdir="/opt/user", srcdir=TEST_PYTHON_PROJECT_PATH)
        packr.setup()
        self.assertEqual(packr.destdir, os.environ[INSTALL_DIR_ENV_VAR]
    
    def test_python(self):
        pass

    def test_user(self):
        pass

    @classmethod
    def tearDownClass(cls):    
        pass
    
if __name__ == '__main__':
    unittest.main()
