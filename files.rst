Files in this repository
========================

.hgignore
    do-not-track

.hgtags
    version tags

readme.rst
    what's all this then?

files.rst
    you're reading me right now

setup.py
    installation stuff

cssedit/
    The package to install

project files:
--------------

cssedit/__init__.py
    package indicator

cssedit/runtests
    script to start unittests from this directory

cssedit/start_editor.py
    script to start css editor from this directory

cssedit/start_tests.py
    script to start tests from this directory

cssedit/editor/__init__.py
    package indicator

cssedit/editor/cssedit.py
    processing functions and class

cssedit/editor/csseditor_qt.py
    GUI frontend

cssedit/editor/cssedit_I_did_it_my_way.py
    version of cssedit.py not using the cssutils package

cssedit/editor/csseditor_plaintext.py
    script to show the use of cssedit's Editor class

cssedit/tests/__init__.py
    package indicator

cssedit/tests/simplecss-compressed.css
    sample css all on one line

cssedit/tests/simplecss-long.css
    sample css with comments and selectors, data and braces on separate lines

cssedit/tests/simplecss-medium.css
    sample css with comments, selectors and properties on separate lines

cssedit/tests/simplecss-short.css
    sample css with comments and for each selector+data a separate line

cssedit/tests/unittests.py
    test functions

cssedit/tests/expected_results.py
    used by unittests
