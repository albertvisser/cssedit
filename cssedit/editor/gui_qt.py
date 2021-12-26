"""cssedit: PyQt specific stuff
"""
import sys
import os
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
from .cssedit import parse_log_line, get_definition_from_file


class MainGui(qtw.QMainWindow):
    """Hoofdscherm van de applicatie
    """
    def __init__(self, master, app, title='', pos=(0, 0), size=(800, 500)):
        self.master = master
        if not app:
            selfcontained = True
            self.app = qtw.QApplication(sys.argv)
        else:
            self.app = app
        print('in csseditor.maingui, app=', self.app)
        super().__init__()
        self.set_window_title()
        if self.master.app_iconame:
            self.setWindowIcon(gui.QIcon(self.master.app_iconame))
        offset = 40 if os.name != 'posix' else 10
        self.move(pos[0] + offset, pos[1] + offset)
        self.resize(size[0], size[1])
        self.statusbar = self.statusBar()

        self.tree = TreePanel(self)
        self.setCentralWidget(self.tree)

    def create_menu(self, menudata):
        """bouw het menu en de meeste toolbars op"""
        menubar = self.menuBar()
        self.menus = {}  # we may need this if we need to do something with specific menus later
        for item, data in menudata:
            menu = menubar.addMenu(item)
            self.menus[item] = menu
            for menudef in data:
                if not menudef:
                    menu.addSeparator()
                    continue
                label, handler, shortcut, icon, info = menudef
                if isinstance(handler, tuple):  # TODO: find a nicer way
                    submenu = menu.addMenu(label)
                    for item in handler:
                        # define submenu options
                        pass
                    continue
                if icon:
                    action = qtw.QAction(gui.QIcon(os.path.join(HERE, icon)), label,
                                         self)
                    ## if not toolbar_added:
                        ## toolbar = self.addToolBar(item)
                        ## toolbar.setIconSize(core.QSize(16, 16))
                        ## toolbar_added = True
                    ## toolbar.addAction(action)
                else:
                    action = qtw.QAction(label, self)
                ## if item == menudata[3][0]:
                    ## if label == '&Undo':
                        ## self.undo_item = action
                    ## elif label == '&Redo':
                        ## self.redo_item = action
                if shortcut:
                    action.setShortcuts([x for x in shortcut.split(",")])
                ## if info.startswith("Check"):
                    ## action.setCheckable(True)
                if info:
                    action.setStatusTip(info)
                action.triggered.connect(handler)
                # action.triggered.connect(handler) werkt hier niet
                if label:
                    menu.addAction(action)
                    self.master.actiondict[label] = action

    def just_show(self):
        """standalone aansturen
        """
        self.show()
        sys.exit(self.app.exec_())

    def set_modality_and_show(self, modal):
        """blokkerend gedrag instellen als aangestuurd vanuit bv. Htmledit
        """
        print('in csseditorgui.set_modality_and_show, modal is', modal)
        modality = core.Qt.ApplicationModal if modal else core.Qt.NonModal
        self.setWindowModality(modality)
        self.show()

    def show_message(self, text, title=""):
        "show a message in a box with a title"
        title = title or self.master.app_title
        qtw.QMessageBox.information(self, title, text)

    def show_statusmessage(self, text):
        "set the message at the bottom of the window"
        self.statusbar.showMessage(text)

    def close(self):
        """reimplemented method from superclass
        """
        self.master.close()
        super().close()

    def set_window_title(self, title=''):
        "set the title for the GUI window"
        title = title or self.master.app_title
        self.setWindowTitle(title)

    def set_waitcursor(self, on):
        "set cursor to clock or back to default"
        if on:
            self.app.setOverrideCursor(gui.QCursor(core.Qt.WaitCursor))
        else:
            self.app.restoreOverrideCursor()

    def show_save_dialog(self, start, filter):
        "get name of file to save"
        return qtw.QFileDialog.getSaveFileName(self, self.master.app_title, start, filter)[0]

    def show_open_dialog(self, start, filter):
        "get name of file to open"
        return qtw.QFileDialog.getOpenFileName(self, self.master.app_title, start, filter)[0]

    def get_input_text(self, prompt):
        "get text from user input"
        return qtw.QInputDialog.getText(self, self.master.app_title, prompt)

    def get_input_choice(self, prompt, choices, editable=False):
        "get user to choice from a list of options"
        return qtw.QInputDialog.getItem(self, self.master.app_title, prompt, choices, editable)

    def show_dialog(self, cls, *args):
        "show and return the results of a dialog"
        edt = cls(self, *args).exec_()
        if edt == qtw.QDialog.Accepted:
            return True, self.dialog_data
        else:
            return False, None


class TreePanel(qtw.QTreeWidget):
    "Tree structure"
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.setColumnCount(2)
        self.hideColumn(1)
        self.headerItem().setHidden(True)
        ## self.setAcceptDrops(True)
        ## self.setDragEnabled(True)
        self.setSelectionMode(self.SingleSelection)
        ## self.setDragDropMode(self.InternalMove)
        ## self.setDropIndicatorShown(True)
        self.setUniformRowHeights(True)

    def selectionChanged(self, newsel, oldsel):
        """wordt aangeroepen als de selectie gewijzigd is

        de tekst van de oude selectie wordt in de itemdict geactualiseerd
        en die van de nieuwe wordt erin opgezocht en getoond"""
        # helaas zijn newsel en oldsel niet makkelijk om te rekenen naar treeitems
        # self.parent.check_active()
        # h = self.currentItem()
        # self.parent.activate_item(h)

    def dropEvent(self, event):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item
        deze methode breidt de Treewidget methode uit met wat visuele zaken
        """
        # copied from DocTree but not implemented yet
        # dragitem = self.selectedItems()[0]
        # dragparent = dragitem.parent()
        # dropitem = self.itemAt(event.pos())
        # if not dropitem:
        #     # ## event.ignore()
        #     return
        # qtw.QTreeWidget.dropEvent(self, event)
        # count = self.topLevelItemCount()
        # if count > 1:
        #     for ix in range(count):
        #         if self.topLevelItem(ix) == dragitem:
        #             self.takeTopLevelItem(ix)
        #             self.oldparent.insertChild(self.oldpos, dragitem)
        #             self.setCurrentItem(dragitem)
        #             break
        #     return
        # self.parent.set_project_dirty(True)
        # self.setCurrentItem(dragitem)
        # dropitem.setExpanded(True)
        super().dropEvent(event)

    def mousePressEvent(self, event):
        """remember the current parent in preparation for "canceling" a dragmove
        """
        # copied from DocTree but not implemented yet
        # xc, yc = event.x(), event.y()
        # item = self.itemAt(xc, yc)
        # if item:
        #     self.oldparent, self.oldpos = self._getitemparentpos(item)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        "for showing a context menu"
        # copied from DocTree but not implemented yet
        # if event.button() == core.Qt.RightButton:
        #     xc, yc = event.x(), event.y()
        #     item = self.itemAt(xc, yc)
        #     if item:
        #         self.create_popupmenu(item)
        #         return
        super().mouseReleaseEvent(event)

    def keyReleaseEvent(self, event):
        "also for showing a context menu"
        # copied from DocTree but not implemented yet
        # if event.key() == core.Qt.Key_Menu:
        #     item = self.currentItem()
        #     self.create_popupmenu(item)
        #     return
        super().keyReleaseEvent(event)

    def create_popupmenu(self, item):
        """create a menu in the right place"""
        # copied from DocTree but not implemented yet
        # menu = qtw.QMenu()
        # for action in self.parent.notemenu.actions():
        #     act = menu.addAction(action)
        #     if item == self.parent.root and action.text() in ('&Add', '&Delete',
        #             '&Forward', '&Back'):
        #         action.setEnabled(False)
        # menu.addSeparator()
        # for action in self.parent.treemenu.actions():
        #     menu.addAction(action)
        #     if item == self.parent.root:
        #         action.setEnabled(False)
        # menu.exec_(self.mapToGlobal(self.visualItemRect(item).center()))
        # if item == self.parent.root:
        #     for action in self.parent.notemenu.actions():
        #         if item == self.parent.root and action.text() in ('&Add', '&Delete',
        #                 '&Forward', '&Back'):
        #             action.setEnabled(True)
        #     for action in self.parent.treemenu.actions():
        #         action.setEnabled(True)

    def remove_root(self):
        self.takeTopLevelItem(0)

    def init_root(self):
        self.root = qtw.QTreeWidgetItem()
        self.root.setText(0, "(untitled)")
        self.addTopLevelItem(self.root)

    def set_root_text(self, text):
        self.root.setText(0, text)

    def get_root(self):
        return self.root

    def activate_rootitem(self):
        self.setCurrentItem(self.root)

    def set_activeitem(self, item):
        self.activeitem = item

    def set_focus(self):
        self.setFocus()

    def add_to_parent(self, titel, parent, pos=-1):
        """shortcut for new_treeitem + add_subitem
        """
        titel = titel.rstrip()
        new = self.new_treeitem(titel)
        self.add_subitem(parent, new, pos)
        return new

    def setcurrent(self, item):
        self.setCurrentItem(item)

    def getcurrent(self):
        return self.currentItem()

    @classmethod
    def new_treeitem(self, itemtext):
        """build new item for tree
        """
        item = qtw.QTreeWidgetItem()
        item.setText(0, itemtext)
        item.setToolTip(0, itemtext)
        return item

    @classmethod
    def add_subitem(self, parent, child, ix=-1):
        "add a subnode to a node. If ix is provided, it should indicate a position"
        if ix == -1:
            parent.addChild(child)
        else:
            parent.insertChild(ix, child)

    @classmethod
    def remove_subitem(self, parent, ix):
        "remove a subnode from a node. If ix is provided, it should indicate a position"
        parent.takeChild(ix)

    @classmethod
    def get_subitems(self, item):
        "returns a list of a tree item's children"
        return [item.child(i) for i in range(item.childCount())]

    @classmethod
    def set_itemtext(self, item, itemtext):
        "sets the text of a tree item"
        item.setText(0, itemtext)
        item.setToolTip(0, itemtext)

    @classmethod
    def get_itemtext(self, item):
        "returns the text of a tree item"
        return item.text(0)

    @classmethod
    def getitemparentpos(self, item):
        "return parent of current item and sequential position under it"
        root = item.parent()
        if root:
            pos = root.indexOfChild(item)
        else:
            pos = -1
        return root, pos

    @classmethod
    def expand_item(self, item):
        "show the item's subitems"
        item.setExpanded(True)

    @classmethod
    def collapse_item(self, item):
        "hide the item's subitems"
        item.setExpanded(False)


class LogDialog(qtw.QDialog):
    "Simple Log display"

    text = "css definition that triggers this message:\n\n"

    def __init__(self, parent, log):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(self.parent.master.app_title + " - show log for current file")
        ## self.setWindowIcon(self.parent.app_icon)
        txt = qtw.QLabel("Dubbelklik op een regel om de context "
                         "(definitie in de css) te bekijken")
        self.lijst = qtw.QListWidget(self)
        ## self.lijst.setSelectionMode(gui.QAbstractItemView.SingleSelection)
        self.lijst.addItems(log)
        b1 = qtw.QPushButton("&Toon Context", self)
        b1.clicked.connect(self.show_context)
        b2 = qtw.QPushButton("&Klaar", self)
        b2.clicked.connect(self.done)

        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.lijst)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(b1)
        hbox.addWidget(b2)
        hbox.insertStretch(0, 1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.resize(600, 480)
        self.exec_()

    def itemDoubleClicked(self, item):
        """handler for doubleclicking over a line
        """
        self.show_context(item)

    def show_context(self, item=None):
        """show full logline (in case it's been chopped off)
        and the definition that triggered it
        """
        # determine selected line in the list and get associated data
        # import pdb; pdb.set_trace()
        selected = item or self.lijst.currentItem()
        y = parse_log_line(selected.text())
        context = get_definition_from_file(self.parent.master.project_file, y.line, y.pos)
        # pop up a box to show the data
        title = self.parent.master.app_title + " - show context for log message"
        qtw.QMessageBox.information(self, title, self.text + context)

    def done(self, arg=None):
        """finish dialog
        """
        super().done(0)


class TextDialog(qtw.QDialog):
    """dialoog om een ongedefinieerde tekst (bv. van een commentaar) weer te geven
    d.m.v. een multiline tekst box
    """
    def __init__(self, parent, title='', text=''):  # , comment=False):
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(440, 280)
        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        self.data_text = qtw.QTextEdit(self)
        ## self.data_text.resize(440, 280)
        hbox.addSpacing(50)
        self.data_text.setText(text)
        hbox.addWidget(self.data_text)
        hbox.addSpacing(50)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Save', self)
        btn.clicked.connect(self.on_ok)
        btn.setDefault(True)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Cancel', self)
        btn.clicked.connect(self.on_cancel)
        hbox.addWidget(btn)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.data_text.setFocus()

    def on_cancel(self):
        """callback for cancel button (should be replaced by connecting to reject?)
        """
        super().reject()

    def on_ok(self):
        """confirm changed text
        """
        self._parent.dialog_data = str(self.data_text.toPlainText())
        super().accept()


class GridDialog(qtw.QDialog):
    """dialoog om stijl definities voor een (groep van) selector(s) op te voeren
    of te wijzigen
    """
    def __init__(self, parent, title='', itemlist=None):  # , comment=False):
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        ## self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        vbox = qtw.QVBoxLayout()

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)
        box = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(qtw.QLabel("Items in table:", self))
        hbox.addStretch()
        box.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        self.attr_table = qtw.QTableWidget(self)
        ## self.attr_table.resize(540, 340)
        self.attr_table.setColumnCount(2)
        self.attr_table.setHorizontalHeaderLabels(['property', 'value'])  # alleen zo te wijzigen
        hdr = self.attr_table.horizontalHeader()
        ## hdr.setMinimumSectionSize(340)
        hdr.resizeSection(0, 102)
        hdr.resizeSection(1, 152)
        hdr.setStretchLastSection(True)
        self.attr_table.verticalHeader().setVisible(False)
        self.attr_table.setTabKeyNavigation(False)
        ## self.attr_table.SetColSize(1, tbl.Size[0] - 162) # 178) # 160)
        if itemlist is not None:
            for attr, value in itemlist:
                idx = self.attr_table.rowCount()
                self.attr_table.insertRow(idx)
                item = qtw.QTableWidgetItem(attr)
                self.attr_table.setItem(idx, 0, item)
                item = qtw.QTableWidgetItem(value)
                self.attr_table.setItem(idx, 1, item)
        else:
            self.row = -1
        ## hbox.addStretch()
        hbox.addWidget(self.attr_table)
        ## hbox.addStretch()
        box.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addSpacing(50)
        btn = qtw.QPushButton('&Add Item', self)
        btn.clicked.connect(self.on_add)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Delete Selected', self)
        btn.clicked.connect(self.on_del)
        hbox.addWidget(btn)
        hbox.addSpacing(50)
        box.addLayout(hbox)

        sbox.setLayout(box)
        vbox.addWidget(sbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Save', self)
        btn.clicked.connect(self.on_ok)
        btn.setDefault(True)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Cancel', self)
        btn.clicked.connect(self.on_cancel)
        hbox.addWidget(btn)
        vbox.addLayout(hbox)
        hbox.addStretch()

        self.setLayout(vbox)

    ## def on_resize(self, evt=None):
        ## self.attr_table.SetColSize(1, self.attr_table.GetSize()[0] - 162) # 178) # 160)
        ## self.attr_table.ForceRefresh()

    def on_add(self):
        """property toevoegen:
        in dit geval hoef ik alleen maar een lege regel aan de tabel toe te voegen
        """
        ## self.attr_table.setFocus()
        num = self.attr_table.rowCount()
        self.attr_table.setRowCount(num + 1)
        ## self.attr_table.insertRow(idx) # waarom niet addRow?
        ## self.attr_table.setCurrentCell(idx, 0)

    def on_del(self):
        """attribuut verwijderen
        """
        ok = qtw.QMessageBox.question(self, 'Delete row from table', 'Are you sure?',
                                      qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel,
                                      qtw.QMessageBox.Ok)
        if ok == qtw.QMessageBox.Ok:
            self.attr_table.removeRow(self.attr_table.currentRow())

    def on_cancel(self):
        """callback for cancel button (should be replaced by connecting to reject?)
        """
        ## qtw.QDialog.done(self, qtw.QDialog.Rejected)
        super().reject()

    def on_ok(self):
        """controle bij OK aanklikken
        """
        proplist = []
        for i in range(self.attr_table.rowCount()):
            name_item = self.attr_table.item(i, 0)
            value_item = self.attr_table.item(i, 1)
            if not name_item or not value_item:
                qtw.QMessageBox.information(self, "Can't continue",
                                            'Not all values are entered and confirmed')
                return
            proplist.append((str(name_item.text()), str(value_item.text())))
        self._parent.dialog_data = proplist
        ## qtw.QDialog.done(self, qtw.QDialog.Accepted)
        super().accept()


class ListDialog(qtw.QDialog):
    """dialoog om een list type property toe te voegen of te wijzigen
    """
    def __init__(self, parent, title='', itemlist=None):  # , comment=False):
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.is_rules_node = "'rules'" in title
        vbox = qtw.QVBoxLayout()

        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Box)
        box = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(qtw.QLabel("Items in list:", self))
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.list = qtw.QListWidget(self)
        if itemlist is not None:
            self.list.addItems([self._parent.tree.get_itemtext(x) for x in itemlist])
        hbox = qtw.QHBoxLayout()
        hbox.addSpacing(50)
        hbox.addWidget(self.list)
        hbox.addSpacing(50)
        box.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Add Item', self)
        btn.clicked.connect(self.on_add)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Edit Selected', self)
        btn.clicked.connect(self.on_edit)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Delete Selected', self)
        btn.clicked.connect(self.on_del)
        hbox.addWidget(btn)
        hbox.addStretch()
        box.addLayout(hbox)

        sbox.setLayout(box)
        vbox.addWidget(sbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('&Save', self)
        btn.clicked.connect(self.on_ok)
        btn.setDefault(True)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Cancel', self)
        btn.clicked.connect(self.on_cancel)
        hbox.addWidget(btn)
        vbox.addLayout(hbox)
        hbox.addStretch()

        self.setLayout(vbox)

    def on_add(self):
        "item toevoegen"
        if self.is_rules_node:
            ruletypes = sorted([(x, y[0]) for x, y in ed.RTYPES.items()],
                               key=lambda item: item[1])
            options = [x[1] for x in ruletypes]
            text, ok = qtw.QInputDialog.getItem(
                self, self._parent.app_title, "Choose type for this rule", options,
                editable=False)
        else:
            text, ok = qtw.QInputDialog.getText(
                self, 'Add item to list', 'Enter text for this item')
        self.list.addItem(text)

    def on_edit(self):
        "item wijzigen"
        current = self.list.currentItem()
        oldtext = current.text()
        if self.is_rules_node:
            ruletypes = sorted([(x, y[0]) for x, y in ed.RTYPES.items()],
                               key=lambda item: item[1])
            options = [x[1] for x in ruletypes]
            current_index = options.index(oldtext) if oldtext else 0
            text, ok = qtw.QInputDialog.getItem(
                self, self._parent.app_title, "Choose type for this rule", options,
                current_index, editable=False)
        else:
            text, ok = qtw.QInputDialog.getText(
                self, 'Edit list item', 'Enter text for this item:', text=oldtext)
        if ok and text != oldtext:
            current.setText(text)

    def on_del(self):
        "item verwijderen"
        ok = qtw.QMessageBox.question(self, 'Delete item from list', 'Are you sure?',
                                      qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel,
                                      qtw.QMessageBox.Ok)
        if ok == qtw.QMessageBox.Ok:
            self.list.takeItem(self.list.currentRow())

    def on_cancel(self):
        """callback for cancel button (should be replaced by connecting to reject?)
        """
        ## qtw.QDialog.done(self, qtw.QDialog.Rejected)
        super().reject()

    def on_ok(self):
        """bij OK: de opgebouwde list via self.dialog_data doorgeven
        aan het mainwindow
        """
        list_data = []
        for row in range(self.list.count()):
            list_data.append(str(self.list.item(row).text()))
        self._parent.dialog_data = list_data
        ## qtw.QDialog.done(self, qtw.QDialog.Accepted)
        super().accept()
