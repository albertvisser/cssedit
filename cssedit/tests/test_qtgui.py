"""unittests for ./cssedit/editor/gui_qt.py
"""
from cssedit.editor import gui_qt as testee


class _TestMainGui:
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
        testobj = testee.MainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for MainGui.__init__
        """
        testobj = testee.MainGui(master, app, title='', pos=(0, 0), size=(800, 500))
        assert capsys.readouterr().out == ("")

    def _test_create_menu(self, monkeypatch, capsys):
        """unittest for MainGui.create_menu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_menu(menudata) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_just_show(self, monkeypatch, capsys):
        """unittest for MainGui.just_show
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.just_show() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_modality_and_show(self, monkeypatch, capsys):
        """unittest for MainGui.set_modality_and_show
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_modality_and_show(modal) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_message(self, monkeypatch, capsys):
        """unittest for MainGui.show_message
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_message(text, title="") == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_statusmessage(self, monkeypatch, capsys):
        """unittest for MainGui.show_statusmessage
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_statusmessage(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_close(self, monkeypatch, capsys):
        """unittest for MainGui.close
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.close() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_window_title(self, monkeypatch, capsys):
        """unittest for MainGui.set_window_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_window_title(title='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_waitcursor(self, monkeypatch, capsys):
        """unittest for MainGui.set_waitcursor
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_waitcursor(on) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_save_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_save_dialog
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_save_dialog(start, filter) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_open_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_open_dialog
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_open_dialog(start, filter) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_input_text(self, monkeypatch, capsys):
        """unittest for MainGui.get_input_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_input_text(prompt) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_input_choice(self, monkeypatch, capsys):
        """unittest for MainGui.get_input_choice
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_input_choice(prompt, choices, editable=False) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_dialog(self, monkeypatch, capsys):
        """unittest for MainGui.show_dialog
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_dialog(cls, *args) == "expected_result"
        assert capsys.readouterr().out == ("")


class _TestTreePanel:
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
        testobj = testee.TreePanel()
        assert capsys.readouterr().out == 'called TreePanel.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for TreePanel.__init__
        """
        testobj = testee.TreePanel(parent)
        assert capsys.readouterr().out == ("")

    def _test_selectionChanged(self, monkeypatch, capsys):
        """unittest for TreePanel.selectionChanged
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.selectionChanged(newsel, oldsel) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_dropEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.dropEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.dropEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_mousePressEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mousePressEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.mousePressEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_mouseReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.mouseReleaseEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.mouseReleaseEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_keyReleaseEvent(self, monkeypatch, capsys):
        """unittest for TreePanel.keyReleaseEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.keyReleaseEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_create_popupmenu(self, monkeypatch, capsys):
        """unittest for TreePanel.create_popupmenu
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.create_popupmenu(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_root(self, monkeypatch, capsys):
        """unittest for TreePanel.remove_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_root() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_init_root(self, monkeypatch, capsys):
        """unittest for TreePanel.init_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.init_root() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_root_text(self, monkeypatch, capsys):
        """unittest for TreePanel.set_root_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_root_text(text) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_root(self, monkeypatch, capsys):
        """unittest for TreePanel.get_root
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_root() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_activate_rootitem(self, monkeypatch, capsys):
        """unittest for TreePanel.activate_rootitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.activate_rootitem() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_activeitem(self, monkeypatch, capsys):
        """unittest for TreePanel.set_activeitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_activeitem(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_focus(self, monkeypatch, capsys):
        """unittest for TreePanel.set_focus
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_focus() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_to_parent(self, monkeypatch, capsys):
        """unittest for TreePanel.add_to_parent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_to_parent(titel, parent, pos=-1) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_setcurrent(self, monkeypatch, capsys):
        """unittest for TreePanel.setcurrent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.setcurrent(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_getcurrent(self, monkeypatch, capsys):
        """unittest for TreePanel.getcurrent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getcurrent() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_new_treeitem(self, monkeypatch, capsys):
        """unittest for TreePanel.new_treeitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.new_treeitem(itemtext) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_subitem(self, monkeypatch, capsys):
        """unittest for TreePanel.add_subitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_subitem(parent, child, ix=-1) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_subitem(self, monkeypatch, capsys):
        """unittest for TreePanel.remove_subitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_subitem(parent, ix) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_subitems(self, monkeypatch, capsys):
        """unittest for TreePanel.get_subitems
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_subitems(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_itemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.set_itemtext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_itemtext(item, itemtext) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_itemtext(self, monkeypatch, capsys):
        """unittest for TreePanel.get_itemtext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_itemtext(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_getitemparentpos(self, monkeypatch, capsys):
        """unittest for TreePanel.getitemparentpos
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.getitemparentpos(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_expand_item(self, monkeypatch, capsys):
        """unittest for TreePanel.expand_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.expand_item(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_collapse_item(self, monkeypatch, capsys):
        """unittest for TreePanel.collapse_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.collapse_item(item) == "expected_result"
        assert capsys.readouterr().out == ("")


class _TestLogDialog:
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
        testobj = testee.LogDialog()
        assert capsys.readouterr().out == 'called LogDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for LogDialog.__init__
        """
        testobj = testee.LogDialog(parent, log)
        assert capsys.readouterr().out == ("")

    def _test_itemDoubleClicked(self, monkeypatch, capsys):
        """unittest for LogDialog.itemDoubleClicked
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.itemDoubleClicked(item) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_show_context(self, monkeypatch, capsys):
        """unittest for LogDialog.show_context
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.show_context(item=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_done(self, monkeypatch, capsys):
        """unittest for LogDialog.done
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.done(arg=None) == "expected_result"
        assert capsys.readouterr().out == ("")


class _TestTextDialog:
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
        testobj = testee.TextDialog()
        assert capsys.readouterr().out == 'called TextDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for TextDialog.__init__
        """
        testobj = testee.TextDialog(parent, title='', text=''):  # , comment=False)
        assert capsys.readouterr().out == ("")

    def _test_on_cancel(self, monkeypatch, capsys):
        """unittest for TextDialog.on_cancel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_cancel() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_ok(self, monkeypatch, capsys):
        """unittest for TextDialog.on_ok
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_ok() == "expected_result"
        assert capsys.readouterr().out == ("")


class _TestGridDialog:
    """unittest for gui_qt.GridDialog
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
        testobj = testee.GridDialog()
        assert capsys.readouterr().out == 'called GridDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for GridDialog.__init__
        """
        testobj = testee.GridDialog(parent, title='', itemlist=None):  # , comment=False)
        assert capsys.readouterr().out == ("")

    def _test_on_add(self, monkeypatch, capsys):
        """unittest for GridDialog.on_add
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_add() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_del(self, monkeypatch, capsys):
        """unittest for GridDialog.on_del
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_del() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_cancel(self, monkeypatch, capsys):
        """unittest for GridDialog.on_cancel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_cancel() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_ok(self, monkeypatch, capsys):
        """unittest for GridDialog.on_ok
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_ok() == "expected_result"
        assert capsys.readouterr().out == ("")


class _TestListDialog:
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
        testobj = testee.ListDialog()
        assert capsys.readouterr().out == 'called ListDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ListDialog.__init__
        """
        testobj = testee.ListDialog(parent, title='', itemlist=None):  # , comment=False)
        assert capsys.readouterr().out == ("")

    def _test_on_add(self, monkeypatch, capsys):
        """unittest for ListDialog.on_add
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_add() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_edit(self, monkeypatch, capsys):
        """unittest for ListDialog.on_edit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_edit() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_del(self, monkeypatch, capsys):
        """unittest for ListDialog.on_del
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_del() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_cancel(self, monkeypatch, capsys):
        """unittest for ListDialog.on_cancel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_cancel() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_ok(self, monkeypatch, capsys):
        """unittest for ListDialog.on_ok
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_ok() == "expected_result"
        assert capsys.readouterr().out == ("")
