import os

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

import setup_parser

INSTALL_DIR = 'DH_VIRTUALENV_INSTALL_ROOT'
DEFAULT_INSTALL_DIR = '/usr/share/python/'
TEMPLATES_DIR= os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')

class Packr(object):

    def __init__(self, srcdir, destdir, user, python):
        self.srcdir = srcdir
        self.destdir = destdir
        self.user = user
        self.python = python

    def setup(self):
        # Read project setup.py
        if not self.srcdir:
            self.srcdir = os.getcwd()
        setup_file = os.path.join(self.srcdir, 'setup.py')
        package = setup_parser.parse_setup_file(setup_file)

        # Set relevant options
        if self.destdir:
            os.environ[INSTALL_DIR] = self.destdir
        if not self.user:
            self.user = package['name'] 
        if self.python:
            self.python = "--python " +  self.python
        else:
            self.python = ''
            
        # Get the templates
        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

        control = env.get_template('control')
        changelog = env.get_template('changelog')
        preinst = env.get_template('preinst')
        rules = env.get_template('rules')

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
        )

        self.preinst = preinst.render(
           home=os.environ.get(INSTALL_DIR,
               os.path.join(DEFAULT_INSTALL_DIR, package['name'])),
           user=self.user,
        )
        
        self.rules = rules.render(
           python=self.python,
        )


    def build(self):
        pass

#    @property 
#    def control(self):
#        return self.control
#
#    @property 
#    def changelog(self):
#        return self.changelog
#
#    @property 
#    def postinst(self):
#        return self.postinst
#
#    @property 
#    def rules(self):
#        return self.rules

