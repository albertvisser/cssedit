"""setup module for cssedit

based on:
https://github.com/pypa/sampleproject/setup.py
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.rst").read_text(encoding='utf-8')

setup(
    name="cssedit",
    version="0.5",
    description="A simple csseditor",
    long_description=long_description,

    url='https://github.com/albertvisser/cssedit',
    author='Albert Visser',
    author_email='albert.visser@gmail.com',

    classifiers=[],  # this is for PyPI, let's leave it alone for now
    keywords="css editing",

    packages=find_packages(),
    install_requires=['cssutils', 'PyQt5'],
    package_data={},  # we don't need this here
    data_files=[],  # we also don't need this
    entry_points={
        ## 'console_scripts': [
            ## 'start_csseditor = editor.csseditor_qt:main'
        ## ],
        ## 'gui_scripts': [
            ## 'cssedit = editor.csseditor_qt:main'
        ## ],
    }
)
