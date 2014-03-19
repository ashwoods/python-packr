import os
import shutil

import unittest
from subprocess import call

from packr import Packr

TEST_INSTALL_ROOT_FOLDER = '/opt/packr-test'
TEST_PYTHON_PROJECT_PATH = './test/django-polls'

class PackrTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass

    def test_build(self):
        packr = Packr(destdir=TEST_INSTALL_ROOT_FOLDER, srcdir=TEST_PYTHON_PROJECT_PATH)
        packr.setup()
        packr.build()

    def test_missing_values_in_setup_file(self):
        #self.assertRaises()
        pass

    def test_source_by_path(self):
        pass

    def test_dest_dir_env_var_set(self):
        packr = Packr(destdir="/opt/user", srcdir=TEST_PYTHON_PROJECT_PATH)
        packr.setup()
        self.assertEqual(packr.destdir, os.environ['DH_VIRTUALENV_INSTALL_ROOT'])
    
    def test_python(self):
        pass

    def test_user(self):
        pass

    @classmethod
    def tearDownClass(cls):    
        #shutil.rmtree(os.path.join(TEST_PYTHON_PROJECT_PATH, 'debian'))
        #shutil.rmtree(os.path.join(TEST_PYTHON_PROJECT_PATH, 'build'))
        # delete test user
        #call(["sudo userdel", packr.user])
        pass
    
if __name__ == '__main__':
    unittest.main()
