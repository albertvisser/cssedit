Files in this repository
========================

.hgignore
    do-not-track

.hgtags
    version tags

readme.rst
    what's all this then?

runtests
    script to start unittests from this directory

start_editor.py
    script to start css editor from this directory

start_tests.py
    script to start tests from this directory

files.rst
    you're reading me right now


editor/__init__.py
    package indicator

editor/cssedit.py
    processing functions and class

editor/csseditor_qt.py
    GUI frontend

editor/cssedit_I_did_it_my_way.py
    version of cssedit.py not using the cssutils package

editor/csseditor_plaintext.py
    script to show the use of cssedit's Editor class

tests/__init__.py
    package indicator

tests/simplecss-compressed.css
    sample css all on one line

tests/simplecss-long.css
    sample css with comments and selectors, data and braces on separate lines

tests/simplecss-medium.css
    sample css with comments, selectors and properties on separate lines

tests/simplecss-short.css
    sample css with comments and for each selector+data a separate line

tests/unittests.py
    test functions

tests/expected_results.py
    used by unittests
