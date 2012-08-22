import sys
import os
from setuptools import setup

# If you change this version, change it also in docs/conf.py
version = "0.1.2"

#doc_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "docs")
#index_filename = os.path.join(doc_dir, "index.txt")
#news_filename = os.path.join(doc_dir, "news.txt")
long_description = """packr - native os packages for your python application."""

setup(name="packr",
      version=version,
      description="native os packages for your python applications",
      long_description=long_description,
      classifiers=[
        'Development Status :: 4 - Beta/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
      ],
      keywords='debian packages',
      author='Ashley Camba',
      author_email='ashwoods@gmail.com',
      url='http://github.com',
      license='MIT',
      packages=['packr', 'packr.commands',],
      install_requires=['Jinja2','draxoft.pkginfo'],
      entry_points=dict(console_scripts=['packr=packr:main', 'packr-%s=packr:main' % sys.version[:3]]),
      test_suite='nose.collector',
      tests_require=['nose', 'virtualenv>=1.6', 'scripttest>=1.1.1', 'mock'],
      zip_safe=False)
