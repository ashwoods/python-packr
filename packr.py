import os, sys
import subprocess

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

import setup_parser

INSTALL_DIR = 'DH_VIRTUALENV_INSTALL_ROOT'
DEFAULT_INSTALL_DIR = '/usr/share/python/'
TEMPLATES_DIR= os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')

class Packr(object):

    def __init__(self, srcdir=None, destdir=None, user=None, python=None):
        self.srcdir = srcdir
        self.destdir = destdir
        self.user = user
        self.python = python

    def setup(self):
        # Read project setup.py
        if not self.srcdir:
            self.srcdir = os.getcwd()
        setup_file = os.path.join(self.srcdir, 'setup.py')
        try:
            package = setup_parser.parse_setup_file(setup_file)
        except FileNotFoundError:
            print(sys.exc_info()[1])
            exit()

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
        postinst = env.get_template('postinst')
        postrm = env.get_template('postrm')
        rules = env.get_template('rules')
        uwsgi_up = env.get_template('uwsgi.ini')
        uwsgi_conf = env.get_template('uwsgi_init.conf')
        
        # Make the necessary folders for debian and conf files
        debian_dir = os.path.join(self.srcdir, 'debian')

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
           home=os.environ.get(INSTALL_DIR,
               os.path.join(DEFAULT_INSTALL_DIR, package['name'])),
           user=self.user,
        )

        self.postinst = postinst.render()
        
        self.postrm = postrm.render(
            user=self.user
        )
        
        self.rules = rules.render(
           python=self.python,
        )

        self.uwsgi_up = uwsgi_up.render()

        self.uwsgi_conf = uwsgi_conf.render()

        # Other non-template file contents
        self.compat = "9"
        self.install = """debian/uwsgi_init.conf etc/init
debian/uwsgi.ini etc/init"""


        # Write files to debian/
        self.write_conf_file(self.control, debian_dir, 'control')
        self.write_conf_file(self.changelog, debian_dir, 'changelog')
        self.write_conf_file(self.preinst, debian_dir, 'preinst')
        self.write_conf_file(self.preinst, debian_dir, 'postinst')
        self.write_conf_file(self.postrm, debian_dir, 'postrm')
        self.write_conf_file(self.rules, debian_dir, 'rules')
        self.write_conf_file(self.compat, debian_dir, 'compat')
        self.write_conf_file(self.install, debian_dir, 'install')
        self.write_conf_file(self.uwsgi_up, debian_dir, 'uwsgi.ini')
        self.write_conf_file(self.uwsgi_conf, debian_dir, 'uwsgi_init.conf')
        
    def write_conf_file(self, contents, folder, name):
        with open(os.path.join(folder, name), "w+") as conf_file:
            print(contents, file=conf_file)

    
    def build(self):
        p = subprocess.Popen(['dpkg-buildpackage', '-us', '-uc'], cwd=self.srcdir)
        p.wait()

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

