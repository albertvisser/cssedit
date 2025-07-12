"""unittests for ./cssedit/editor/gui_qt.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from cssedit.editor import gui_qt as testee


exp_maingui = """\
called QMainWindow.__init__ with args () {}
called MainGui.set_window_title with arg 'xxx'
called Icon.__init__ with arg `yyy`
called MainWindow.setWindowIcon
called MainWindow.move with args (20, 20)
called MainWindow.resize with args (1800, 1500)
called MainWindow.statusBar
called StatusBar.__init__ with args ()
called Tree.__init__
called MainWidget.setCentralWindow with arg `TreePanel`
"""
exp_logdialog = """\
called Dialog.__init__ with args namespace(master=namespace(app_title='apptitle')) () {{}}
called Dialog.setWindowTitle with args ('apptitle - show log for current file',)
called Label.__init__ with args ('Dubbelklik op een regel om de context (definitie in de css) te bekijken',)
called List.__init__
called List.addItems with arg `['regel1', 'regel2']`
called PushButton.__init__ with args ('&Toon Context', {testobj}) {{}}
called Signal.connect with args ({testobj.show_context},)
called PushButton.__init__ with args ('&Klaar', {testobj}) {{}}
called Signal.connect with args ({testobj.done},)
called VBox.__init__
called HBox.__init__
called HBox.addWidget with arg MockLabel
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called HBox.addWidget with arg MockListBox
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called HBox.addWidget with arg MockPushButton
called HBox.addWidget with arg MockPushButton
called HBox.insertStretch
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called Dialog.setLayout
called Widget.resize with args (600, 480)
called Dialog.exec
"""
exp_textdialog = """\
called Dialog.__init__ with args namespace(master=namespace(app_title='apptitle')) () {{}}
called Dialog.setWindowTitle with args ('{title}',)
called Widget.resize with args (440, 280)
called VBox.__init__
called HBox.__init__
called Editor.__init__ with args ({testobj},)
called HBox.addSpacing
called Editor.setText with arg `{text}`
called HBox.addWidget with arg MockEditorWidget
called HBox.addSpacing
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Save', {testobj}) {{}}
called Signal.connect with args ({testobj.on_ok},)
called PushButton.setDefault with arg `True`
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}
called Signal.connect with args ({testobj.on_cancel},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called Dialog.setLayout
called Editor.setFocus
"""
exp_grid_start = """\
called Dialog.__init__ with args namespace(master=namespace(app_title='apptitle')) () {{}}
called Dialog.setWindowTitle with args ('{title}',)
called VBox.__init__
called Frame.__init__
called Frame.setFrameStyle with arg `{testee.qtw.QFrame.Box}`
called VBox.__init__
called HBox.__init__
called HBox.addStretch
called Label.__init__ with args ('Items in table:', {testobj})
called HBox.addWidget with arg MockLabel
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called Table.__init__ with args ({testobj},)
called Header.__init__
called Header.__init__
called Table.setColumnCount with arg '2'
called Table.setHorizontalHeaderLabels with arg '['property', 'value']'
called Table.horizontalHeader
called Header.resizeSection with args (0, 102)
called Header.resizeSection with args (1, 152)
called Header.setStretchLastSection with arg True
called Table.verticalHeader
called Header.setVisible with args 'False'
called Table.setTabKeyNavigation with arg False
"""
exp_grid_middle = """\
called Table.rowCount
called Table.insertRow with arg '0'
called Table.setItem with args (0, 0, QTableWidgetItem)
called Table.setItem with args (0, 1, QTableWidgetItem)
called Table.rowCount
called Table.insertRow with arg '1'
called Table.setItem with args (1, 0, QTableWidgetItem)
called Table.setItem with args (1, 1, QTableWidgetItem)
"""
exp_grid_end = """\
called HBox.addWidget with arg MockTable
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called HBox.addSpacing
called PushButton.__init__ with args ('&Add Item', {testobj}) {{}}
called Signal.connect with args ({testobj.on_add},)
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Delete Selected', {testobj}) {{}}
called Signal.connect with args ({testobj.on_del},)
called HBox.addWidget with arg MockPushButton
called HBox.addSpacing
called VBox.addLayout with arg MockHBoxLayout
called Frame.setLayout with arg MockVBoxLayout
called VBox.addWidget with arg MockFrame
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Save', {testobj}) {{}}
called Signal.connect with args ({testobj.on_ok},)
called PushButton.setDefault with arg `True`
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}
called Signal.connect with args ({testobj.on_cancel},)
called HBox.addWidget with arg MockPushButton
called VBox.addLayout with arg MockHBoxLayout
called HBox.addStretch
called Dialog.setLayout
"""
exp_list_start = """\
called Dialog.__init__ with args {parent} () {{}}
called Dialog.setWindowTitle with args ({title!r},)
called VBox.__init__
called Frame.__init__
called Frame.setFrameStyle with arg `{testee.qtw.QFrame.Box}`
called VBox.__init__
called HBox.__init__
called HBox.addStretch
called Label.__init__ with args ('Items in list:', {testobj})
called HBox.addWidget with arg MockLabel
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called List.__init__
"""
exp_list_middle = """\
called Tree.get_itemtext with arg 'yyy'
called Tree.get_itemtext with arg 'zzz'
called List.addItems with arg `['yyy', 'zzz']`
"""
exp_list_end = """\
called HBox.__init__
called HBox.addSpacing
called HBox.addWidget with arg MockListBox
called HBox.addSpacing
called VBox.addLayout with arg MockHBoxLayout
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Add Item', {testobj}) {{}}
called Signal.connect with args ({testobj.on_add},)
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Edit Selected', {testobj}) {{}}
called Signal.connect with args ({testobj.on_edit},)
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Delete Selected', {testobj}) {{}}
called Signal.connect with args ({testobj.on_del},)
called HBox.addWidget with arg MockPushButton
called HBox.addStretch
called VBox.addLayout with arg MockHBoxLayout
called Frame.setLayout with arg MockVBoxLayout
called VBox.addWidget with arg MockFrame
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Save', {testobj}) {{}}
called Signal.connect with args ({testobj.on_ok},)
called PushButton.setDefault with arg `True`
called HBox.addWidget with arg MockPushButton
called PushButton.__init__ with args ('&Cancel', {testobj}) {{}}
called Signal.connect with args ({testobj.on_cancel},)
called HBox.addWidget with arg MockPushButton
called VBox.addLayout with arg MockHBoxLayout
called HBox.addStretch
called Dialog.setLayout
"""


@pytest.fixture
def expected_output():
    """generic fixture for ouput expectations
    """
    return {'maingui': exp_maingui,
            'logdialog': exp_logdialog,
            'textdialog': exp_textdialog,
            'griddialog': exp_grid_start + exp_grid_end,
            'griddialog2': exp_grid_start + exp_grid_middle + exp_grid_end,
            'listdialog': exp_list_start + exp_list_end,
            'listdialog2': exp_list_start + exp_list_middle + exp_list_end}


class MockEditor:
    "stub for main.Editor"
    def __init__(self):
        print('called Editor.__init__')


class MockMainGui:
    "stub for gui_qt.MainGui"
    def __init__(self, *args):
        print('called MainGui.__init__ with args', args)


class MockTree:
    "stub for gui_qt.TreePanel"
    def __init__(self):
        print('called Tree.__init__')


class TestMainGui:
    """unittest for gui_qt.MainGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.MainGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MainGui.__init__ with args', args)
        monkeypatch.setattr(testee.MainGui, '__init__', mock_init)
        testobj = testee.MainGui()
        testobj.app = mockqtw.MockApplication()
        testobj.master = MockEditor()
        testobj.tree = MockTree()
        assert capsys.readouterr().out == ('called MainGui.__init__ with args ()\n'
                                           'called Application.__init__\n'
                                           'called Editor.__init__\n'
                                           'called Tree.__init__\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for MainGui.__init__
        """
        def mock_init(self, *args, **kwargs):
            print('called QMainWindow.__init__ with args', args, kwargs)
        def mock_set_title(self, title):
            print(f"called MainGui.set_window_title with arg '{title}'")
        monkeypatch.setattr(testee.qtw.QApplication, '__init__',
                            mockqtw.MockApplication.__init__)
        monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mock_init)
        #                   mockqtw.MockMainWindow.__init__)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowIcon',
                            mockqtw.MockMainWindow.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'move', mockqtw.MockMainWindow.move)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'statusBar', mockqtw.MockMainWindow.statusBar)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setCentralWidget',
                            mockqtw.MockMainWindow.setCentralWidget)
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.MainGui, 'set_window_title', mock_set_title)
        monkeypatch.setattr(testee.TreePanel, '__init__', mockqtw.MockTreeWidget.__init__)
        master = MockEditor()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        master.app_iconame = ''
        testobj = testee.MainGui(master, None)
        assert testobj.master == master
        assert isinstance(testobj.statusbar, mockqtw.MockStatusBar)
        assert isinstance(testobj.tree, testee.TreePanel)
        assert testobj.output_options == []
        assert capsys.readouterr().out == (
                "called Application.__init__\n"
                "called QMainWindow.__init__ with args () {}\n"
                "called MainGui.set_window_title with arg ''\n"
                "called MainWindow.move with args (10, 10)\n"
                "called MainWindow.resize with args (800, 500)\n"
                "called MainWindow.statusBar\n"
                "called StatusBar.__init__ with args ()\n"
                "called Tree.__init__\n"
                "called MainWidget.setCentralWindow with arg `TreePanel`\n")
        master.app_iconame = 'yyy'
        testobj = testee.MainGui(master, 'app', title='xxx', pos=(10, 10), size=(1800, 1500))
        assert capsys.readouterr().out == expected_output['maingui']

    def test_create_menu(self, monkeypatch, capsys):
        """unittest for MainGui.create_menu
        """
        def mock_callback():
            "stub"
        def mock_define(*args):
            print(f'called Editor.define_format_submenu with args (menu, {args[1]})')
        callback1 = mock_callback
        callback2 = mock_callback
        callback3 = mock_callback
        monkeypatch.setattr(testee.MainGui, 'menuBar', mockqtw.MockMainWindow.menuBar)
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.define_format_submenu = mock_define
        testobj.master.format_option = 'xxx'
        testobj.master.actiondict = {}
        menudata = ()
        testobj.create_menu(menudata)
        assert testobj.menus == {}
        assert testobj.master.actiondict == {}
        assert capsys.readouterr().out == "called MainWindow.menuBar\ncalled MenuBar.__init__\n"
        menudata = (('menutitle',
                     (('label-1', callback1, 'x, y', 'infotekst-1'),
                      (),
                      ('xxx', ('submenu', 'data')),
                      ('label-2', callback2, '', 'infotekst-2'),
                      ('', callback3, 'z', 'infotekst-2'),
                      ('label-3', callback3, 'z', ''))),)
        # breakpoint()
        testobj.create_menu(menudata)
        assert list(testobj.menus.keys()) == ['menutitle']
        assert isinstance(testobj.menus['menutitle'], mockqtw.MockMenu)
        assert list(testobj.master.actiondict.keys()) == ['label-1', 'label-2', 'label-3']
        for x in testobj.master.actiondict.values():
            assert isinstance(x, mockqtw.MockAction)
        assert capsys.readouterr().out == (
            "called MainWindow.menuBar\n"
            "called MenuBar.__init__\n"
            "called MenuBar.addMenu with arg  menutitle\n"
            "called Menu.__init__ with args ('menutitle',)\n"
            f"called Action.__init__ with args ('label-1', {testobj})\n"
            "called Action.setShortcuts with arg `['x', ' y']`\n"
            "called Action.setStatusTip with arg 'infotekst-1'\n"
            f"called Signal.connect with args ({callback1},)\n"
            "called Menu.addAction\n"
            "called Menu.addSeparator\n"
            "called Action.__init__ with args ('-----', None)\n"
            "called Editor.define_format_submenu with args (menu, ('xxx', ('submenu', 'data')))\n"
            f"called Action.__init__ with args ('label-2', {testobj})\n"
            "called Action.setStatusTip with arg 'infotekst-2'\n"
            f"called Signal.connect with args ({callback2},)\n"
            "called Menu.addAction\n"
            "called Menu.addSeparator\n"
            "called Action.__init__ with args ('-----', None)\n"
            f"called Action.__init__ with args ('label-3', {testobj})\n"
            "called Action.setShortcuts with arg `['z']`\n"
            f"called Signal.connect with args ({callback3},)\n"
            "called Menu.addAction\n")

    def test_define_format_submenu(self, monkeypatch, capsys):
        """unittest for MainGui.define_format_submenu
        """
        def mock_callback():
            "stub"
        menu = mockqtw.MockMenu()
        assert capsys.readouterr().out == "called Menu.__init__ with args ()\n"
        callback1 = mock_callback
        callback2 = mock_callback
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.output_options = []
        testobj.define_format_submenu(menu, ['title', (('item-1', callback1), ('item-2', callback2)),
                                             '', '', 'statustip'])
        assert len(testobj.output_options) == len([callback1, callback2])
        assert isinstance(testobj.output_options[0], mockqtw.MockAction)
        assert isinstance(testobj.output_options[1], mockqtw.MockAction)
        assert capsys.readouterr().out == (
                "called Menu.addMenu with args ('title',)\n"
                "called Menu.__init__ with args ()\n"
                f"called Menu.addAction with args `item-1` {callback1}\n"
                f"called Action.__init__ with args ('item-1', {callback1})\n"
                "called Action.setCheckable with arg `True`\n"
                f"called Menu.addAction with args `item-2` {callback2}\n"
                f"called Action.__init__ with args ('item-2', {callback2})\n"
                "called Action.setCheckable with arg `True`\n"
                "called Action.setChecked with arg `True`\n"
                "called Menu.setStatusTip with arg 'statustip'\n")

    def test_check_format_option(self, monkeypatch, capsys):
        """unittest for MainGui.check_format_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.output_options = [mockqtw.MockAction(), mockqtw.MockAction(), mockqtw.MockAction(),
                                  mockqtw.MockAction()]
        assert capsys.readouterr().out == ("called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n")
        testobj.check_format_option(2)
        assert capsys.readouterr().out == ("called Action.setChecked with arg `False`\n"
                                           "called Action.setChecked with arg `False`\n"
                                           "called Action.setChecked with arg `False`\n"
                                           "called Action.setChecked with arg `False`\n"
                                           "called Action.setChecked with arg `True`\n")

    def test_just_show(self, monkeypatch, capsys):
        """unittest for MainGui.just_show
        """
        def mock_show():
            print('called MainGui.show')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show = mock_show
        with pytest.raises(SystemExit):
            testobj.just_show()
        assert capsys.readouterr().out == ("called MainGui.show\ncalled Application.exec\n")

    def test_set_modality_and_show(self, monkeypatch, capsys):
        """unittest for MainGui.set_modality_and_show
        """
        def mock_show():
            print('called MainGui.show')
        monkeypatch.setattr(testee.MainGui, 'setWindowModality',
                            mockqtw.MockMainWindow.setWindowModality)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show = mock_show
        testobj.set_modality_and_show('')
        assert capsys.readouterr().out == (
                "called MainWindow.setWindowModality with arg"
                f" '{testee.core.Qt.WindowModality.NonModal}'\n"
                "called MainGui.show\n")
        testobj.set_modality_and_show('x')
        assert capsys.readouterr().out == (
                "called MainWindow.setWindowModality with arg"
                f" '{testee.core.Qt.WindowModality.ApplicationModal}'\n"
                "called MainGui.show\n")

    def test_show_message(self, monkeypatch, capsys):
        """unittest for MainGui.show_message
        """
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        testobj.show_message('qqq')
        assert capsys.readouterr().out == (
                f"called MessageBox.information with args `{testobj}` `xxx` `qqq`\n")
        testobj.show_message('qqq', 'yyy')
        assert capsys.readouterr().out == (
                f"called MessageBox.information with args `{testobj}` `yyy` `qqq`\n")

    def test_show_statusmessage(self, monkeypatch, capsys):
        """unittest for MainGui.show_statusmessage
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.statusbar = mockqtw.MockStatusBar()
        testobj.show_statusmessage('text')
        assert capsys.readouterr().out == ("called StatusBar.__init__ with args ()\n"
                                           "called StatusBar.showMessage with arg `text`\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for MainGui.close
        """
        def mock_close():
            print('called Editor.close')
        monkeypatch.setattr(testee.qtw.QMainWindow, 'close', mockqtw.MockMainWindow.close)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.close = mock_close
        testobj.close()
        assert capsys.readouterr().out == ("called Editor.close\ncalled MainWindow.close\n")

    def test_set_window_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_title
        """
        monkeypatch.setattr(testee.MainGui, 'setWindowTitle', mockqtw.MockMainWindow.setWindowTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        testobj.set_window_title()
        assert capsys.readouterr().out == ("called MainWindow.setWindowTitle with arg `xxx`\n")
        testobj.set_window_title('yyy')
        assert capsys.readouterr().out == ("called MainWindow.setWindowTitle with arg `yyy`\n")

    def test_set_waitcursor(self, monkeypatch, capsys):
        """unittest for MainGui.set_waitcursor
        """
        monkeypatch.setattr(testee.gui, 'QCursor', mockqtw.MockCursor)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_waitcursor(False)
        assert capsys.readouterr().out == ("called Application.restoreOverrideCursor\n")
        testobj.set_waitcursor(True)
        assert capsys.readouterr().out == (
                f"called Cursor.__init__ with arg {testee.core.Qt.CursorShape.WaitCursor}\n"
                "called Application.setOverrideCursor with arg MockCursor\n")

    def test_show_save_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_save_dialog
        """
        def mock_save(self, *args):
            print('called FileDialog.getSaveFilename with args', *args)
            return 'sss', True
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getSaveFileName', mock_save)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        assert testobj.show_save_dialog('start', 'filter') == "sss"
        assert capsys.readouterr().out == (
                "called FileDialog.getSaveFilename with args xxx start filter\n")

    def test_show_open_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_open_dialog
        """
        def mock_open(self, *args):
            print('called FileDialog.getOpenFilename with args', *args)
            return 'ooo', True
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_open)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        assert testobj.show_open_dialog('start', 'filter') == "ooo"
        assert capsys.readouterr().out == (
                "called FileDialog.getOpenFilename with args xxx start filter\n")

    def test_get_input_text(self, monkeypatch, capsys):
        """unittest for MainGui.get_input_text
        """
        def mock_get(self, *args):
            print('called InputDialog.getText with args', args)
            return 'yyy'
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        assert testobj.get_input_text('prompt') == "yyy"
        assert capsys.readouterr().out == "called InputDialog.getText with args ('xxx', 'prompt')\n"

    def test_get_input_choice(self, monkeypatch, capsys):
        """unittest for MainGui.get_input_choice
        """
        def mock_get(self, *args):
            print('called InputDialog.getItem with args', args)
            return 'yyy'
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.app_title = 'xxx'
        assert testobj.get_input_choice('prompt', ['a', 'b'], True) == "yyy"
        assert capsys.readouterr().out == (
                "called InputDialog.getItem with args ('xxx', 'prompt', ['a', 'b'], True)\n")
        assert testobj.get_input_choice('prompt', ['a', 'b']) == "yyy"
        assert capsys.readouterr().out == (
                "called InputDialog.getItem with args ('xxx', 'prompt', ['a', 'b'], False)\n")

    def test_show_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_dialog
        """
        def mock_exec(self):
            print('called Dialog.exec')
            return testee.qtw.QDialog.DialogCode.Accepted
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.dialog_data = {'x': 'y'}
        cls = mockqtw.MockDialog
        assert testobj.show_dialog(cls, 'args') == (False, None)
        assert capsys.readouterr().out == (
                f"called Dialog.__init__ with args {testobj} ('args',) {{}}\n"
                "called Dialog.exec\n")
        cls.exec = mock_exec
        assert testobj.show_dialog(cls, 'args') == (True, {'x': 'y'})
        assert capsys.readouterr().out == (
                f"called Dialog.__init__ with args {testobj} ('args',) {{}}\n"
                "called Dialog.exec\n")


class TestTreePanel:
    """unittest for gui_qt.TreePanel
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.TreePanel object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TreePanel.__init__ with args', args)
        monkeypatch.setattr(testee.TreePanel, '__init__', mock_init)
        testobj = testee.TreePanel()
        testobj.parent = MockMainGui()
        assert capsys.readouterr().out == ('called TreePanel.__init__ with args ()\n'
                                           'called MainGui.__init__ with args ()\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for TreePanel.__init__
        """
        parent = 'parent'
        monkeypatch.setattr(testee.qtw.QTreeWidget, '__init__',
                            mockqtw.MockTreeWidget.__init__)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setColumnCount',
                            mockqtw.MockTreeWidget.setColumnCount)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'hideColumn',
                            mockqtw.MockTreeWidget.hideColumn)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'headerItem',
                            mockqtw.MockTreeWidget.headerItem)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setSelectionMode',
                            mockqtw.MockTreeWidget.setSelectionMode)
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'setUniformRowHeights',
                            mockqtw.MockTreeWidget.setUniformRowHeights)
        testobj = testee.TreePanel(parent)
        assert testobj.parent == parent
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called Tree.setColumnCount with arg `2`\n"
                                           "called Tree.hideColumn\n"
                                           "called Tree.headerItem\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setHidden with arg `True`\n"
                                           "called Tree.setSelectionMode\n"
                                           "called Tree.setUniformRowHeights with arg `True`\n")

    def _test_selectionChanged(self, monkeypatch, capsys):
        """unittest for TreePanel.selectionChanged
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.selectionChanged('newsel', 'oldsel') == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_dropEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.dropEvent
        """
        def mock_handler(self, arg):
            print(f"called TreeWidget.dropEvent with arg '{arg}'")
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'dropEvent', mock_handler)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.dropEvent('event')
        assert capsys.readouterr().out == ("called TreeWidget.dropEvent with arg 'event'\n")

    def test_mousePressEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mousePressEvent
        """
        def mock_handler(self, arg):
            print(f"called TreeWidget.mousePressEvent with arg '{arg}'")
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'mousePressEvent', mock_handler)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mousePressEvent('event')
        assert capsys.readouterr().out == ("called TreeWidget.mousePressEvent with arg 'event'\n")

    def test_mouseReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mouseReleaseEvent
        """
        def mock_handler(self, arg):
            print(f"called TreeWidget.mouseReleaseEvent with arg '{arg}'")
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'mouseReleaseEvent', mock_handler)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mouseReleaseEvent('event')
        assert capsys.readouterr().out == ("called TreeWidget.mouseReleaseEvent with arg 'event'\n")

    def test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.keyReleaseEvent
        """
        def mock_handler(self, arg):
            print(f"called TreeWidget.keyReleaseEvent with arg '{arg}'")
        monkeypatch.setattr(testee.qtw.QTreeWidget, 'keyReleaseEvent', mock_handler)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.keyReleaseEvent('event')
        assert capsys.readouterr().out == ("called TreeWidget.keyReleaseEvent with arg 'event'\n")

    def _test_create_popupmenu(self, monkeypatch, capsys):
        """unittest for TreePanel.create_popupmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_popupmenu('item') == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_remove_root(self, monkeypatch, capsys):
        """unittest for TreePanel.remove_root
        """
        monkeypatch.setattr(testee.TreePanel, 'takeTopLevelItem',
                            mockqtw.MockTreeWidget.takeTopLevelItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_root()
        assert capsys.readouterr().out == "called Tree.takeTopLevelItem with arg `0`\n"

    def test_init_root(self, monkeypatch, capsys):
        """unittest for TreePanel.init_root
        """
        monkeypatch.setattr(testee.TreePanel, 'addTopLevelItem',
                            mockqtw.MockTreeWidget.addTopLevelItem)
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.init_root()
        assert isinstance(testobj.root, testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with args (0, '(untitled)')\n"
                                           "called Tree.addTopLevelItem\n")

    def test_set_root_text(self, monkeypatch, capsys):
        """unittest for TreePanel.set_root_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_root_text('text')
        assert capsys.readouterr().out == "called TreeItem.setText with args (0, 'text')\n"

    def test_get_root(self, monkeypatch, capsys):
        """unittest for TreePanel.get_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.root = root
        assert testobj.get_root() == root

    def test_activate_rootitem(self, monkeypatch, capsys):
        """unittest for TreePanel.activate_rootitem
        """
        monkeypatch.setattr(testee.TreePanel, 'setCurrentItem', mockqtw.MockTreeWidget.setCurrentItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.activate_rootitem()
        assert capsys.readouterr().out == f"called Tree.setCurrentItem with arg `{testobj.root}`\n"

    def test_set_activeitem(self, monkeypatch, capsys):
        """unittest for TreePanel.set_activeitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_activeitem('item')
        assert testobj.activeitem == 'item'

    def test_set_focus(self, monkeypatch, capsys):
        """unittest for TreePanel.set_focus
        """
        monkeypatch.setattr(testee.TreePanel, 'setFocus', mockqtw.MockTreeWidget.setFocus)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus()
        assert capsys.readouterr().out == "called Tree.setFocus\n"

    def test_add_to_parent(self, monkeypatch, capsys):
        """unittest for TreePanel.add_to_parent
        """
        def mock_new(arg):
            print(f"called Tree.new_treeitem with arg '{arg}'")
            return 'new item'
        def mock_add(*args):
            print("called Tree.add_subitem with args", args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.new_treeitem = mock_new
        testobj.add_subitem = mock_add
        assert testobj.add_to_parent('titel', 'parent') == "new item"
        assert capsys.readouterr().out == (
                "called Tree.new_treeitem with arg 'titel'\n"
                "called Tree.add_subitem with args ('parent', 'new item', -1)\n")
        assert testobj.add_to_parent('titel', 'parent', 3) == "new item"
        assert capsys.readouterr().out == (
                "called Tree.new_treeitem with arg 'titel'\n"
                "called Tree.add_subitem with args ('parent', 'new item', 3)\n")

    def test_setcurrent(self, monkeypatch, capsys):
        """unittest for TreePanel.setcurrent
        """
        monkeypatch.setattr(testee.TreePanel, 'setCurrentItem', mockqtw.MockTreeWidget.setCurrentItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.setcurrent(item)
        assert capsys.readouterr().out == f"called Tree.setCurrentItem with arg `{item}`\n"

    def test_getcurrent(self, monkeypatch, capsys):
        """unittest for TreePanel.getcurrent
        """
        monkeypatch.setattr(testee.TreePanel, 'currentItem', mockqtw.MockTreeWidget.currentItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getcurrent() == "called Tree.currentItem"

    def test_new_treeitem(self, monkeypatch, capsys):
        """unittest for TreePanel.new_treeitem
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.new_treeitem('item text')
        assert isinstance(result, testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with args (0, 'item text')\n"
                                           "called TreeItem.setTooltip with args (0, 'item text')\n")

    def test_add_subitem(self, monkeypatch, capsys):
        """unittest for TreePanel.add_subitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        parent = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.add_subitem(parent, 'child')
        assert capsys.readouterr().out == "called TreeItem.addChild\n"
        testobj.add_subitem(parent, 'child', 2)
        assert capsys.readouterr().out == "called TreeItem.insertChild at pos 2\n"

    def test_remove_subitem(self, monkeypatch, capsys):
        """unittest for TreePanel.remove_subitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        parent = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.remove_subitem(parent, 1)
        assert capsys.readouterr().out == ("called TreeItem.takeChild\n")

    def test_get_subitems(self, monkeypatch, capsys):
        """unittest for TreePanel.get_subitems
        """
        item = mockqtw.MockTreeItem()
        item.addChild('item0')
        item.addChild('item1')
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.addChild\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_subitems(item) == ['item0', 'item1']
        assert capsys.readouterr().out == ("called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 0\n"
                                           "called TreeItem.child with arg 1\n")

    def test_set_itemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.set_itemtext
        """
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_itemtext(item, 'item text')
        assert capsys.readouterr().out == ("called TreeItem.setText with args (0, 'item text')\n"
                                           "called TreeItem.setTooltip with args (0, 'item text')\n")

    def test_get_itemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.get_itemtext
        """
        item = mockqtw.MockTreeItem('item text')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('item text',)\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_itemtext(item) == "item text"
        assert capsys.readouterr().out == ("called TreeItem.text with arg 0\n")

    def test_getitemparentpos(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemparentpos
        """
        parent = mockqtw.MockTreeItem()
        def mock_parent(self):
            nonlocal parent
            print(f"called QTreeWidgetItem.parent with arg '{self}'")
            return parent
        def mock_parent_2(self):
            print(f"called QTreeWidgetItem.parent with arg '{self}'")
            return None
        monkeypatch.setattr(mockqtw.MockTreeItem, 'parent', mock_parent)
        item = mockqtw.MockTreeItem()
        parent.addChild('item0')
        parent.addChild(item)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.addChild\n"
                                           "called TreeItem.addChild\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.getitemparentpos(item)
        assert len(result) == 2
        assert isinstance(result[0], mockqtw.MockTreeItem)
        assert result[1] == 1
        assert capsys.readouterr().out == (f"called QTreeWidgetItem.parent with arg '{item}'\n"
                                           "called TreeItem.indexOfChild\n")
        monkeypatch.setattr(mockqtw.MockTreeItem, 'parent', mock_parent_2)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getitemparentpos(item) == (None, -1)
        assert capsys.readouterr().out == f"called QTreeWidgetItem.parent with arg '{item}'\n"

    def test_expand_item(self, monkeypatch, capsys):
        """unittest for TreePanel.expand_item
        """
        item = mockqtw.MockTreeItem('item text')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('item text',)\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.expand_item(item)
        assert capsys.readouterr().out == ("called TreeItem.setExpanded with arg `True`\n")

    def test_collapse_item(self, monkeypatch, capsys):
        """unittest for TreePanel.collapse_item
        """
        item = mockqtw.MockTreeItem('item text')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('item text',)\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.collapse_item(item)
        assert capsys.readouterr().out == ("called TreeItem.setExpanded with arg `False`\n")


class TestLogDialog:
    """unittest for gui_qt.LogDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.LogDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called LogDialog.__init__ with args', args)
        monkeypatch.setattr(testee.LogDialog, '__init__', mock_init)
        testobj = testee.LogDialog()
        testobj.parent = MockMainGui()
        testobj.parent.master = MockEditor()
        assert capsys.readouterr().out == ('called LogDialog.__init__ with args ()\n'
                                           'called MainGui.__init__ with args ()\n'
                                           'called Editor.__init__\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for LogDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockWidget.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'exec', mockqtw.MockDialog.exec)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        parent = types.SimpleNamespace(master=types.SimpleNamespace(app_title='apptitle'))
        testobj = testee.LogDialog(parent, ['regel1', 'regel2'])
        assert capsys.readouterr().out == expected_output['logdialog'].format(testobj=testobj)

    def test_itemDoubleClicked(self, monkeypatch, capsys):
        """unittest for LogDialog.itemDoubleClicked
        """
        def mock_show(*args):
            print('called LogDialog.show_context with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.show_context = mock_show
        testobj.itemDoubleClicked('item')
        assert capsys.readouterr().out == "called LogDialog.show_context with args ('item',)\n"

    def test_show_context(self, monkeypatch, capsys):
        """unittest for LogDialog.show_context
        """
        def mock_item():
            print('called List.currentItem')
            return mockqtw.MockListItem('xxx')
        def mock_parse(arg):
            print('called parse_log_line with arg', arg)
            return types.SimpleNamespace(line=1, pos=2)
        def mock_get_definition(*args):
            print('called get_definition_from_file with args', args)
            return 'context'
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee, 'parse_log_line', mock_parse)
        monkeypatch.setattr(testee, 'get_definition_from_file', mock_get_definition)
        testobj.lijst = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj.lijst.currentItem = mock_item
        testobj.parent.master.app_title = 'app title'
        testobj.parent.master.project_file = 'pfile'
        testobj.show_context()
        assert capsys.readouterr().out == (
                "called List.currentItem\n"
                "called ListItem.__init__ with args ('xxx',)\n"
                "called ListItem.text\n"
                "called parse_log_line with arg xxx\n"
                "called get_definition_from_file with args ('pfile', 1, 2)\n"
                f"called MessageBox.information with args `{testobj}`"
                " `app title - show context for log message`"
                " `css definition that triggers this message:\n\ncontext`\n")
        item = mockqtw.MockListItem('yyy')
        testobj.show_context(item)
        assert capsys.readouterr().out == (
                "called ListItem.__init__ with args ('yyy',)\n"
                "called ListItem.text\n"
                "called parse_log_line with arg yyy\n"
                "called get_definition_from_file with args ('pfile', 1, 2)\n"
                f"called MessageBox.information with args `{testobj}`"
                " `app title - show context for log message`"
                " `css definition that triggers this message:\n\ncontext`\n")

    def test_done(self, monkeypatch, capsys):
        """unittest for LogDialog.done
        """
        def mock_done(self, code):
            print(f'called Dialog.done with arg {code}')
        monkeypatch.setattr(testee.qtw.QDialog, 'done', mock_done)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.done()
        assert capsys.readouterr().out == ("called Dialog.done with arg 0\n")
        testobj.done('xxx')
        assert capsys.readouterr().out == ("called Dialog.done with arg 0\n")


class TestTextDialog:
    """unittest for gui_qt.TextDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.TextDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__ with args', args)
        monkeypatch.setattr(testee.TextDialog, '__init__', mock_init)
        testobj = testee.TextDialog('parent')
        assert capsys.readouterr().out == "called TextDialog.__init__ with args ('parent',)\n"
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for TextDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockWidget.resize)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        parent = types.SimpleNamespace(master=types.SimpleNamespace(app_title='apptitle'))
        testobj = testee.TextDialog(parent)  # , comment=False)
        assert testobj.parent == parent
        assert isinstance(testobj.data_text, testee.qtw.QTextEdit)
        assert capsys.readouterr().out == expected_output['textdialog'].format(testobj=testobj,
                                                                               title='', text='')
        testobj = testee.TextDialog(parent, title='xxx', text='yyyy')  # , comment=False)
        assert testobj.parent == parent
        assert isinstance(testobj.data_text, testee.qtw.QTextEdit)
        assert capsys.readouterr().out == expected_output['textdialog'].format(testobj=testobj,
                                                                               title='xxx',
                                                                               text='yyyy')

    def test_on_cancel(self, monkeypatch, capsys):
        """unittest for TextDialog.on_cancel
        """
        def mock_reject(self):
            print('called Dialog.reject')
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mock_reject)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_cancel()
        assert capsys.readouterr().out == ("called Dialog.reject\n")

    def test_on_ok(self, monkeypatch, capsys):
        """unittest for TextDialog.on_ok
        """
        def mock_accept(self):
            print('called Dialog.accept')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(dialog_data='')
        testobj.data_text = mockqtw.MockEditorWidget('xxx')
        assert capsys.readouterr().out == "called Editor.__init__ with args ('xxx',)\n"
        testobj.on_ok()
        assert testobj._parent.dialog_data == 'xxx'
        assert capsys.readouterr().out == "called Editor.toPlainText\ncalled Dialog.accept\n"


class TestGridDialog:
    """unittest for gui_qt.GridDialog)
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.GridDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called GridDialog.__init__ with args', args)
        monkeypatch.setattr(testee.GridDialog, '__init__', mock_init)
        testobj = testee.GridDialog()
        testobj.parent = MockMainGui()
        testobj.parent.master = MockEditor()
        assert capsys.readouterr().out == ('called GridDialog.__init__ with args ()\n'
                                           'called MainGui.__init__ with args ()\n'
                                           'called Editor.__init__\n')
        testobj.attr_table = mockqtw.MockTable(testobj)
        assert capsys.readouterr().out == (f"called Table.__init__ with args ({testobj},)\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for GridDialog.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        parent = types.SimpleNamespace(master=types.SimpleNamespace(app_title='apptitle'))
        testobj = testee.GridDialog(parent)
        assert testobj.parent == parent
        assert isinstance(testobj.attr_table, testee.qtw.QTableWidget)
        assert capsys.readouterr().out == expected_output['griddialog'].format(testee=testee,
                                                                               testobj=testobj,
                                                                               title='',
                                                                               text='yyyy')
        testobj = testee.GridDialog(parent, title='xxx', itemlist=['yy', 'zz'])
        assert testobj.parent == parent
        assert isinstance(testobj.attr_table, testee.qtw.QTableWidget)
        assert capsys.readouterr().out == expected_output['griddialog2'].format(testee=testee,
                                                                                testobj=testobj,
                                                                                title='xxx',
                                                                                text='yyyy')

    def test_on_add(self, monkeypatch, capsys):
        """unittest for GridDialog.on_add
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_add()
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.setRowCount with arg '1'\n")

    def test_on_del(self, monkeypatch, capsys):
        """unittest for GridDialog.on_del
        """
        def mock_question(parent, caption, message, buttons, default):
            print('called MessageBox.question with args'
                  f' `{caption}` `{message}` `{buttons}` `{default}`')
            return testee.qtw.QMessageBox.StandardButton.Cancel
        def mock_question_2(parent, caption, message, buttons, default):
            print('called MessageBox.question with args'
                  f' `{caption}` `{message}` `{buttons}` `{default}`')
            return testee.qtw.QMessageBox.StandardButton.Ok
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_question)
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj.on_del()
        assert capsys.readouterr().out == ("called MessageBox.question with args"
                                           " `Delete row from table` `Are you sure?` `3` `1`\n")
        monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_del()
        assert capsys.readouterr().out == ("called MessageBox.question with args"
                                           " `Delete row from table` `Are you sure?` `3` `1`\n"
                                           "called Table.currentRow\n"
                                           "called Table.removeRow with arg '2'\n")

    def test_on_cancel(self, monkeypatch, capsys):
        """unittest for GridDialog.on_cancel
        """
        def mock_reject(self):
            print('called Dialog.reject')
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mock_reject)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_cancel()
        assert capsys.readouterr().out == ("called Dialog.reject\n")

    def test_on_ok(self, monkeypatch, capsys):
        """unittest for GridDialog.on_ok
        """
        def get_item(x, y):
            if y == 1:
                return None
            return mockqtw.MockTableItem()
        def get_item_2(x, y):
            if y == 0:
                return None
            return mockqtw.MockTableItem()
        def get_item_3(x, y):
            return mockqtw.MockTableItem(f'item{x}{y}')
        def mock_accept(self):
            print('called Dialog.accept')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent = types.SimpleNamespace(dialog_data='')
        testobj.attr_table = mockqtw.MockTable(testobj)
        testobj.attr_table.setRowCount(2)
        testobj.attr_table.item = get_item
        assert capsys.readouterr().out == (f"called Table.__init__ with args ({testobj},)\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n"
                                           "called Table.setRowCount with arg '2'\n")
        testobj.on_ok()
        assert testobj._parent.dialog_data == ''
        assert capsys.readouterr().out == (
                "called Table.rowCount\n"
                "called TableItem.__init__ with arg ''\n"
                f"called MessageBox.information with args `{testobj}`"
                " `Can't continue` `Not all values are entered and confirmed`\n")
        testobj.attr_table.item = get_item_2
        testobj.on_ok()
        assert testobj._parent.dialog_data == ''
        assert capsys.readouterr().out == (
                "called Table.rowCount\n"
                "called TableItem.__init__ with arg ''\n"
                f"called MessageBox.information with args `{testobj}`"
                " `Can't continue` `Not all values are entered and confirmed`\n")
        testobj.attr_table.item = get_item_3
        testobj.on_ok()
        assert testobj._parent.dialog_data == [('item00', 'item01'), ('item10', 'item11')]
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called TableItem.__init__ with arg 'item00'\n"
                                           "called TableItem.__init__ with arg 'item01'\n"
                                           "called TableItem.text\n"
                                           "called TableItem.text\n"
                                           "called TableItem.__init__ with arg 'item10'\n"
                                           "called TableItem.__init__ with arg 'item11'\n"
                                           "called TableItem.text\n"
                                           "called TableItem.text\n"
                                           "called Dialog.accept\n")


class TestListDialog:
    """unittest for gui_qt.ListDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.ListDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ListDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ListDialog, '__init__', mock_init)
        parent = types.SimpleNamespace()
        testobj = testee.ListDialog(parent)
        testobj._parent = parent
        testobj.list = mockqtw.MockListBox()
        assert capsys.readouterr().out == (f'called ListDialog.__init__ with args ({parent},)\n'
                                           'called List.__init__\n')
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for ListDialog.__init__
        """
        def mock_get_itemtext(arg):
            print(f"called Tree.get_itemtext with arg '{arg}'")
            return arg
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        parent = types.SimpleNamespace(tree=types.SimpleNamespace(get_itemtext=mock_get_itemtext))
        testobj = testee.ListDialog(parent)
        assert testobj.parent == parent
        assert not testobj.is_rules_node
        assert isinstance(testobj.list, testee.qtw.QListWidget)
        title = ''
        assert capsys.readouterr().out == expected_output['listdialog'].format(testee=testee,
                                                                               parent=parent,
                                                                               title=title,
                                                                               testobj=testobj)
        title = "xxx'rules'xx"
        testobj = testee.ListDialog(parent, title, ['yyy', 'zzz'])
        assert testobj.parent == parent
        assert testobj.is_rules_node
        assert isinstance(testobj.list, testee.qtw.QListWidget)
        assert capsys.readouterr().out == expected_output['listdialog2'].format(testee=testee,
                                                                                parent=parent,
                                                                                title=title,
                                                                                testobj=testobj)

    def test_on_add(self, monkeypatch, capsys):
        """unittest for ListDialog.on_add
        """
        def mock_get_item(*args, **kwargs):
            print('called InputDialog.getItem with args', args, kwargs)
            return 'zzz', True
        def mock_get_text(*args, **kwargs):
            print('called InputDialog.getText with args', args, kwargs)
            return 'zzz', True
        monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
        monkeypatch.setattr(testee, 'RTYPES', {'a': ['x', 1], 'b': ['y', 0]})
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent.app_title = 'app title'
        testobj.is_rules_node = True
        testobj.on_add()
        assert capsys.readouterr().out == (
                f"called InputDialog.getItem with args {testobj}"
                " ('app title', 'Choose type for this rule', ['x', 'y']) {'editable': False}\n")
        testobj.is_rules_node = False
        testobj.on_add()
        assert capsys.readouterr().out == (
                f"called InputDialog.getText with args {testobj}"
                " ('Add item to list', 'Enter text for this item') {}\n")
        testobj.is_rules_node = True
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_get_item)
        testobj.on_add()
        assert capsys.readouterr().out == (
                f"called InputDialog.getItem with args ({testobj},"
                " 'app title', 'Choose type for this rule', ['x', 'y']) {'editable': False}\n"
                "called List.addItem with arg `zzz`\n")
        testobj.is_rules_node = False
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_get_text)
        testobj.on_add()
        assert capsys.readouterr().out == (
                f"called InputDialog.getText with args ({testobj},"
                " 'Add item to list', 'Enter text for this item') {}\n"
                "called List.addItem with arg `zzz`\n")

    def test_on_edit(self, monkeypatch, capsys):
        """unittest for ListDialog.on_edit
        """
        def mock_get_item(*args, **kwargs):
            print('called InputDialog.getItem with args', args, kwargs)
            return 'yy', True
        def mock_get_item_2(*args, **kwargs):
            print('called InputDialog.getItem with args', args, kwargs)
            return '', True
        def mock_get_text(*args, **kwargs):
            print('called InputDialog.getText with args', args, kwargs)
            return 'yy', True
        def mock_get_text_2(*args, **kwargs):
            print('called InputDialog.getText with args', args, kwargs)
            return '', True
        def mock_current():
            result = mockqtw.MockListItem('yy')
            assert capsys.readouterr().out == ("called ListItem.__init__ with args ('yy',)\n")
            print('called List.currentItem')
            return result
        monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
        monkeypatch.setattr(testee, 'RTYPES', {'a': ['yy', 'qq'], 'b': ['xx', 'rr']})
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._parent.app_title = 'app title'
        testobj.list.currentItem = mock_current
        testobj.is_rules_node = True
        testobj.on_edit()
        assert capsys.readouterr().out == (
                "called List.currentItem\n"
                "called ListItem.text\n"
                f"called InputDialog.getItem with args {testobj}"
                " ('app title', 'Choose type for this rule', ['xx', 'yy'], 1) {'editable': False}\n")
        testobj.is_rules_node = False
        testobj.on_edit()
        assert capsys.readouterr().out == (
                "called List.currentItem\n"
                "called ListItem.text\n"
                f"called InputDialog.getText with args {testobj}"
                " ('Edit list item', 'Enter text for this item:') {'text': 'yy'}\n")
        testobj.is_rules_node = True
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_get_item)
        testobj.on_edit()
        assert capsys.readouterr().out == (
                "called List.currentItem\n"
                "called ListItem.text\n"
                f"called InputDialog.getItem with args ({testobj},"
                " 'app title', 'Choose type for this rule', ['xx', 'yy'], 1) {'editable': False}\n")
        testobj.is_rules_node = False
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_get_text)
        testobj.on_edit()
        assert capsys.readouterr().out == (
                "called List.currentItem\n"
                "called ListItem.text\n"
                f"called InputDialog.getText with args ({testobj},"
                " 'Edit list item', 'Enter text for this item:') {'text': 'yy'}\n")
        testobj.is_rules_node = True
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_get_item_2)
        testobj.on_edit()
        assert capsys.readouterr().out == (
                "called List.currentItem\n"
                "called ListItem.text\n"
                f"called InputDialog.getItem with args ({testobj},"
                " 'app title', 'Choose type for this rule', ['xx', 'yy'], 1) {'editable': False}\n"
                "called ListItem.setText with arg ''\n")
        testobj.is_rules_node = False
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_get_text_2)
        testobj.on_edit()
        assert capsys.readouterr().out == (
                "called List.currentItem\n"
                "called ListItem.text\n"
                f"called InputDialog.getText with args ({testobj},"
                " 'Edit list item', 'Enter text for this item:') {'text': 'yy'}\n"
                "called ListItem.setText with arg ''\n")

    def test_on_del(self, monkeypatch, capsys):
        """unittest for ListDialog.on_del
        """
        def mock_question(parent, caption, message, buttons, default):
            print('called MessageBox.question with args'
                  f' `{caption}` `{message}` `{buttons}` `{default}`')
            return testee.qtw.QMessageBox.Cancel
        def mock_question_2(parent, caption, message, buttons, default):
            print('called MessageBox.question with args'
                  f' `{caption}` `{message}` `{buttons}` `{default}`')
            return testee.qtw.QMessageBox.Ok
        monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_question)
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_del()
        assert capsys.readouterr().out == ("called MessageBox.question with args"
                                           " `Delete item from list` `Are you sure?` `3` `1`\n")
        monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_question_2)
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_del()
        assert capsys.readouterr().out == ("called MessageBox.question with args"
                                           " `Delete item from list` `Are you sure?` `3` `1`\n"
                                           "called List.currentRow\n"
                                           "called List.takeItem with arg `current row`\n")

    def test_on_cancel(self, monkeypatch, capsys):
        """unittest for ListDialog.on_cancel
        """
        def mock_reject(self):
            print('called Dialog.reject')
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mock_reject)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_cancel()
        assert capsys.readouterr().out == ("called Dialog.reject\n")

    def test_on_ok(self, monkeypatch, capsys):
        """unittest for ListDialog.on_ok
        """
        def mock_accept(self):
            print('called Dialog.accept')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        x = mockqtw.MockListItem('xxx')
        testobj.list.addItem(x)
        y = mockqtw.MockListItem('yyy')
        testobj.list.addItem(y)
        assert capsys.readouterr().out == ("called ListItem.__init__ with args ('xxx',)\n"
                                           f"called List.addItem with arg `{x}`\n"
                                           "called ListItem.__init__ with args ('yyy',)\n"
                                           f"called List.addItem with arg `{y}`\n")
        testobj._parent.dialog_data = []
        testobj.on_ok()
        assert testobj._parent.dialog_data == ['xxx', 'yyy']
        assert capsys.readouterr().out == ("called List.count\n"
                                           "called ListItem.text\n"
                                           "called ListItem.text\n"
                                           "called Dialog.accept\n")
