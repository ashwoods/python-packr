import os, sys
import subprocess
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
import setup_parser

DEFAULT_SRCDIR = os.getcwd()

class Packr(object):

    def __init__(self, srcdir, destdir=None, user=None,
                    python=None):
        if not srcdir:
            self.srcdir = DEFAULT_SRCDIR
        self.destdir = destdir
        self.user = user
        self.python = python

    def fill_templates(self):
        env = Environment(loader=FileSystemLoader('./templates'))

        setup_file = os.path.join(self.srcdir, 'setup.py')
        package = setup_parser.parse_setup_file(setup_file)

        control = env.get_template('control')

        self.control = control.render(
            name= package['name'],
            author=package['author'],
            author_email=package['author_email'],
            url = package['url'],
            description=package['description'],
            source=package['name'],
            arch = 'all',
        )

    def print_control(self):
        print(self.control)
