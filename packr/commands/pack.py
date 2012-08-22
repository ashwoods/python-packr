from packr.basecommand import Command, arg
import os, sys
import subprocess
from draxoft.tools import pkginfo
from jinja2 import Template
from jinja2 import Environment, PackageLoader


# - reading on debian packaging
#
#
# http://www.debian.org/doc/debian-policy/
# http://www.debian.org/doc/manuals/securing-debian-howto/ch9.en.html#s-bpp-lower-privs
# http://www.debian-administration.org/articles/336
# http://www.webupd8.org/2010/01/how-to-create-deb-package-ubuntu-debian.html

class Pack(Command):
    """Create native os package"""

    args = [
        arg('source',
            help='path to source file',
            nargs='?',
            default=os.getcwd()
        ),
        arg('--destination',
            help='destination folder',
            default=os.getcwd()
        )
    ]

    def find_architecture(self):
        pass
        # dpkg-architecture -qDEB_HOST_ARCH


    def parse_sys_requirements(self):
        pass


    def create_virtualenv(self):
        pass


    def create_package(self):
        pass





    def execute(self, args):

        env = Environment(loader=PackageLoader('packr', 'templates'))
        control = env.get_template('control')

        project_dir = args.source

        setup = os.path.join(project_dir, 'setup.py')
        package = pkginfo.parse_setup_file(setup)

        control = control.render(
            name= package['name'],
            author=package['author'],
            author_email=package['author_email'],
            url = package['url'],
            description=package['description'],
            source=package['name'],
            arch = 'all',
        )

        SRC_FOLDER        =    os.path.join(args.source, 'packr-src')
        UNPACKED_FOLDER   =    os.path.join(args.source, 'packr-unpacked')
        TARGET_FOLDER     =    os.path.join(args.source, 'packr-build')

        REQ = ['stable.pip','stable.txt','requirements.pip', 'requirements.txt']



