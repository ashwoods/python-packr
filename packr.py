import os, sys, shutil
import subprocess

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

import setup_parser

INSTALL_DIR_ENV_VAR = 'DH_VIRTUALENV_INSTALL_ROOT'
DEFAULT_INSTALL_DIR = '/usr/share/python/'
TEMPLATES_DIR= os.path.join(sys.prefix, 'templates')

class Packr(object):

    def __init__(self, destdir, user, python, output, extra):
        self.destdir = destdir
        self.user = user
        self.python = python
        self.output = output
        self.extra = extra

    def setup(self):
        # Read project setup.py
        setup_file = os.path.join(os.getcwd(), 'setup.py')
        try:
            package = setup_parser.parse_setup_file(setup_file)
        except FileNotFoundError:
            print(sys.exc_info()[1])
            exit()

        # Set relevant options
        if self.destdir:
            os.environ[INSTALL_DIR_ENV_VAR] = self.destdir
        
        if not self.user:
            self.user = package['name'] 
        
        if self.python:
            self.python = "--python " +  self.python
        else:
            self.python = ''
        
        if self.extra:
            debdir = self.extra.pop()
            inst = ''
            while self.extra:
                inst = inst + self.extra.pop() + ' ' + debdir + '\n'
            self.extra = inst
        else:
            self.extra = ''

        # Path to the generated deb package
        parentdir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        pkgname = package['name'] + '_' + package['version'] + '_' + 'all.deb'
        self.debpkg = os.path.join(parentdir, pkgname) 

        # Project home, also home to the user created in preinst script 
        self.project_home=os.environ.get(INSTALL_DIR_ENV_VAR,
                            os.path.join(DEFAULT_INSTALL_DIR, package['name']))

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
        debian_dir = os.path.join(os.getcwd(), 'debian')

        if not os.path.exists(debian_dir):
            os.mkdir(debian_dir) 
        
        # Fill in the templates
        self.control = control.render(
            name= package['name'],
            author=package['author'],
            author_email=package['author_email'],
            url = package['url'],
            description=package['description'],
            source=package['name'],
            arch = 'all',
        )

        self.changelog = changelog.render(
            author=package['author'],
            author_email=package['author_email'],
            source=package['name'],
            version=package['version'],
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
            name=package['name']
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
        p = subprocess.Popen(['dpkg-buildpackage', '-us', '-uc'])
        p.wait()
        if self.output:
            shutil.move(self.debpkg,  self.output)


