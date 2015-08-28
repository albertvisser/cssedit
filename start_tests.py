import tests.test_cssedit as tst

def test_functions():
    for test in tst.test_functions:
        tst.test_functions[test]()

def test_editorclass():
    for test in tst.test_editorclass:
        tst.test_editorclass[test]()

def test_gui():
    for test in tst.gui_testtypes:
        tst.test_gui(test)

def run_all_tests():
    test_functions()
    test_editorclass()
    test_gui()

# for now
tst.test_gui('file')
