"""setup module for cssedit

based on:
https://github.com/pypa/sampleproject/setup.py
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="cssedit",
    version="0.5",
    description="A simple csseditor",
    long_description=long_description,

    url='https://bitbucket.org/avisser/cssedit',
    author='Albert Visser',
    author_email='albert.visser@gmail.com',

    license="Don't know yet",
    classifiers=[], # this is for PyPI, let's leave it alone for now
    keywords="css editing",

    packages=find_packages(),
    install_requires=['cssutils', 'PyQt4'],
    package_data={}, # we don't need this here
    data_files=[], # we also don't need this
    entry_points={
        ## 'console_scripts': [
            ## 'start_csseditor = editor.csseditor_qt:main'
        ## ],
        'gui_scripts': [
            'cssedit = editor.csseditor_qt:main'
        ],
    }
)
