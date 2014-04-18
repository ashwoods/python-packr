import os, sys, shutil, tempfile
import subprocess

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

import setup_parser

INSTALL_DIR_ENV_VAR = 'DH_VIRTUALENV_INSTALL_ROOT'
DEFAULT_INSTALL_DIR = '/usr/share/python/'
TEMPLATES_DIR = os.path.join(sys.prefix, 'templates')

class Packr(object):

    def __init__(self, srcdir, destdir, user, python, output, extra):
        self.srcdir = srcdir
        self.destdir = destdir
        self.user = user
        self.python = python
        self.output = output
        self.extra = extra

    def setup(self):

        # Read project setup.py
        if not self.srcdir:
            self.srcdir = os.getcwd()
        setup_file = os.path.join(self.srcdir, 'setup.py')
        try:
            self.package = setup_parser.parse_setup_file(setup_file)
        except FileNotFoundError:
            print(sys.exc_info()[1])
            exit()

        # Set relevant options
        if self.destdir:
            os.environ[INSTALL_DIR_ENV_VAR] = self.destdir
        
        if not self.user:
            self.user = self.package['name'] 
        
        if self.python:
            self.python = "--python " +  self.python
        else:
            self.python = ''
        
        # Create temporary build directory and copy project folder to it
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp = self.tmpdir.name
        self.tmp_project = os.path.join(self.tmp, self.package['name'])
        shutil.copytree(self.srcdir, self.tmp_project)

        # Copy extra files to tmp and generate contents for install conffile
        if self.extra:
            debdir = self.extra.pop()
            inst = ''
            while self.extra:
                f = self.extra.pop()
                shutil.copy(f, self.tmp)
                inst = inst + os.path.join(os.pardir, os.path.basename(f)) + \
                                                            ' ' + debdir + '\n'
            self.extra = inst
        else:
            self.extra = ''

        # Project home, also home to the user created in preinst script 
        self.project_home=os.environ.get(INSTALL_DIR_ENV_VAR,
                            os.path.join(DEFAULT_INSTALL_DIR, self.package['name']))

        # Get the templates
        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

        control = env.get_template('control')
        changelog = env.get_template('changelog')
        preinst = env.get_template('preinst')
        postinst = env.get_template('postinst')
        postrm = env.get_template('postrm')
        rules = env.get_template('rules')
        install = env.get_template('install')
        dirs = env.get_template('dirs')

        # Make debian folder
        debian_dir = os.path.join(self.tmp_project, 'debian')

        if not os.path.exists(debian_dir):
            os.mkdir(debian_dir) 
        
        # Fill in the templates
        self.control = control.render(
            name= self.package['name'],
            author=self.package['author'],
            author_email=self.package['author_email'],
            url = self.package['url'],
            description=self.package['description'],
            source=self.package['name'],
            arch = 'all',
        )

        self.changelog = changelog.render(
            author=self.package['author'],
            author_email=self.package['author_email'],
            source=self.package['name'],
            version=self.package['version'],
        )

        self.preinst = preinst.render(
            home=self.project_home,
            user=self.user,
        )

        self.postinst = postinst.render(
            user=self.user,
            home=self.project_home
        )
        
        self.postrm = postrm.render(
            user=self.user,
            home=self.project_home
        )
        
        self.rules = rules.render(
            python=self.python,
        )

        self.install = install.render(
            extra=self.extra
        )

        self.dirs = dirs.render(
            name=self.package['name']
        )

        # Other non-template file contents
        self.compat = "9"

        # Write files to debian/
        self.write_conf_file(self.control, debian_dir, 'control')
        self.write_conf_file(self.changelog, debian_dir, 'changelog')
        self.write_conf_file(self.preinst, debian_dir, 'preinst')
        self.write_conf_file(self.postinst, debian_dir, 'postinst')
        self.write_conf_file(self.postrm, debian_dir, 'postrm')
        self.write_conf_file(self.rules, debian_dir, 'rules')
        self.write_conf_file(self.compat, debian_dir, 'compat')
        self.write_conf_file(self.install, debian_dir, 'install')
        self.write_conf_file(self.dirs, debian_dir, 'dirs')
        
    def write_conf_file(self, contents, folder, name):
        with open(os.path.join(folder, name), "w+") as conf_file:
            print(contents, file=conf_file)
    
    def build(self):
        build_dir = os.path.join(self.tmp, os.path.basename(self.srcdir))
        pkgname = self.package['name'] + '_' + self.package['version'] + '_' + 'all.deb'
        self.debpkg = os.path.join(self.tmp, pkgname) 

        p = subprocess.Popen(['dpkg-buildpackage', '-us', '-uc'], cwd=self.tmp_project)
        p.wait()

        if self.output:
            shutil.move(self.debpkg,  self.output)
        else:
            shutil.move(self.debpkg,  os.getcwd())
        
        self.tmpdir.cleanup()




