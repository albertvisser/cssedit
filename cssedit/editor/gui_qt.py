"""cssedit: PyQt specific stuff
"""
import sys
import os
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
HERE = os.path.dirname(__file__)


class MainGui(qtw.QMainWindow):
    """Hoofdscherm van de applicatie
    """
    def __init__(self, master, app, title='', pos=(0, 0), size=(800, 500)):
        self.master = master
        if not app:
            # selfcontained = True
            self.app = qtw.QApplication(sys.argv)
        else:
            self.app = app
        # print('in csseditor.maingui, app=', self.app)
        super().__init__()
        self.set_window_title(title)
        if self.master.app_iconame:
            self.appicon = gui.QIcon(self.master.app_iconame)
            self.setWindowIcon(self.appicon)
        offset = 40 if os.name != 'posix' else 10
        self.move(pos[0] + offset, pos[1] + offset)
        self.resize(size[0], size[1])
        self.statusbar = self.statusBar()
        self.output_options = []
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
                if not menudef or not menudef[0]:
                    menu.addSeparator()
                    continue
                if menudef[0] == self.master.format_option:
                    self.define_format_submenu(menu, menudef)
                    continue
                label, handler, shortcut, info = menudef
                action = gui.QAction(label, self)
                if shortcut:
                    action.setShortcuts(shortcut.split(","))
                if info:
                    action.setStatusTip(info)
                action.triggered.connect(handler)
                # action.triggered.connect(handler) werkt hier niet
                menu.addAction(action)
                self.master.actiondict[label] = action

    def define_format_submenu(self, menu, menudef):
        "add format options to the application menu"
        submenu = menu.addMenu(menudef[0])
        for subitem in menudef[1]:
            action = submenu.addAction(subitem[0], subitem[1])
            action.setCheckable(True)
            # action.triggered.connect(subitem[1])
            self.output_options.append(action)
        self.output_options[0].setChecked(True)
        submenu.setStatusTip(menudef[-1])

    def check_format_option(self, value):
        "make the chosen output format visible in the menu"
        for seq in range(4):
            self.output_options[seq].setChecked(False)
        self.output_options[value].setChecked(True)

    def just_show(self):
        """standalone aansturen
        """
        self.show()
        sys.exit(self.app.exec())

    def set_modality_and_show(self, modal):
        """blokkerend gedrag instellen als aangestuurd vanuit bv. Htmledit
        """
        # print('in csseditorgui.set_modality_and_show, modal is', modal)
        modality = (core.Qt.WindowModality.ApplicationModal if modal
                    else core.Qt.WindowModality.NonModal)
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
            self.app.setOverrideCursor(gui.QCursor(core.Qt.CursorShape.WaitCursor))
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
        edt = cls(self, *args).exec()
        if edt == qtw.QDialog.DialogCode.Accepted:
            return True, self.dialog_data
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
        self.setSelectionMode(self.SelectionMode.SingleSelection)
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
        # menu.exec(self.mapToGlobal(self.visualItemRect(item).center()))
        # if item == self.parent.root:
        #     for action in self.parent.notemenu.actions():
        #         if item == self.parent.root and action.text() in ('&Add', '&Delete',
        #                 '&Forward', '&Back'):
        #             action.setEnabled(True)
        #     for action in self.parent.treemenu.actions():
        #         action.setEnabled(True)

    def remove_root(self):
        "clear the tree"
        self.takeTopLevelItem(0)

    def init_root(self):
        "start a new tree"
        self.root = qtw.QTreeWidgetItem()
        self.root.setText(0, "(untitled)")
        self.addTopLevelItem(self.root)

    def set_root_text(self, text):
        "text for root element"
        self.root.setText(0, text)

    def get_root(self):
        "return root element"
        return self.root

    def activate_rootitem(self):
        "start working with root element"
        self.setCurrentItem(self.root)

    def set_activeitem(self, item):
        "start working with an element"
        self.activeitem = item

    def set_focus(self):
        "bring focus to the tree"
        self.setFocus()

    def add_to_parent(self, titel, parent, pos=-1):
        """shortcut for new_treeitem + add_subitem
        """
        titel = titel.rstrip()
        new = self.new_treeitem(titel)
        self.add_subitem(parent, new, pos)
        return new

    def setcurrent(self, item):
        "start working with an element"
        self.setCurrentItem(item)

    def getcurrent(self):
        "return the selected element"
        return self.currentItem()

    @classmethod
    def new_treeitem(cls, itemtext):
        """build new item for tree
        """
        item = qtw.QTreeWidgetItem()
        item.setText(0, itemtext)
        item.setToolTip(0, itemtext)
        return item

    @classmethod
    def add_subitem(cls, parent, child, ix=-1):
        "add a subnode to a node. If ix is provided, it should indicate a position"
        if ix == -1:
            parent.addChild(child)
        else:
            parent.insertChild(ix, child)

    @classmethod
    def remove_subitem(cls, parent, ix):
        "remove a subnode from a node. Ix indicates the position beneath the parent"
        parent.takeChild(ix)

    @classmethod
    def get_subitems(cls, item):
        "returns a list of a tree item's children"
        return [item.child(i) for i in range(item.childCount())]

    @classmethod
    def set_itemtext(cls, item, itemtext):
        "sets the text of a tree item"
        item.setText(0, itemtext)
        item.setToolTip(0, itemtext)

    @classmethod
    def get_itemtext(cls, item):
        "returns the text of a tree item"
        return item.text(0)

    @classmethod
    def getitemparentpos(cls, item):
        "return parent of current item and sequential position under it"
        root = item.parent()
        pos = root.indexOfChild(item) if root else -1
        return root, pos

    @classmethod
    def expand_item(cls, item):
        "show the item's subitems"
        item.setExpanded(True)

    @classmethod
    def collapse_item(cls, item):
        "hide the item's subitems"
        item.setExpanded(False)


class LogDialogGui(qtw.QDialog):
    "Simple Log display"
    def __init__(self, mathter, parent, title, size):
        self.mathter = mathter
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.appicon)
        self.resize(size[0], size[1])
        self.vbox = qtw.QVBoxLayout()

    def add_label(self, labeltext):
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(labeltext))
        self.vbox.addLayout(hbox)

    def add_listbox(self, data, callback):
        hbox = qtw.QHBoxLayout()
        lijst = qtw.QListWidget(self)
        # lijst.setSelectionMode(gui.QAbstractItemView.SingleSelection)
        lijst.addItems(data)
        lijst.itemDoubleClicked.connect(callback)   # in plaats van het signal herdefiniëren?
        hbox.addWidget(lijst)
        self.vbox.addLayout(hbox)
        return lijst

    def add_buttons(self, buttondefs):
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        for text, callback in buttondefs:
            btn = qtw.QPushButton(text, self)
            btn.clicked.connect(callback)
            hbox.addWidget(btn)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

    def finish_dialog(self):
        self.setLayout(self.vbox)
        self.exec()

    def itemDoubleClicked(self, item):
        """handler for doubleclicking over a line
        """
        self.show_context(item)

    def get_selection(self, listbox):
        return listbox.currentItem()

    def get_listitem_text(self, item):
        return item.text()

    def meld(self, title, text):
        qtw.QMessageBox.information(self, title, text)

    def done(self, arg=None):
        """finish dialog
        """
        super().done(0)


class EditDialogGui(qtw.QDialog):
    """base class for dialogs to edit css properties
    """
    def __init__(self, mathter, parent, title, size):
        self.mathter = mathter
        self._parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.appicon)
        self.resize(size[0], size[1])
        self.vbox = qtw.QVBoxLayout()

    def add_outline(self):
        sbox = qtw.QFrame()
        sbox.setFrameStyle(qtw.QFrame.Shape.Box)
        box = qtw.QVBoxLayout()
        self.sbox.setLayout(box)
        self.vbox.addWidget(sbox)
        return box

    def add_label_to_outline(self, box, labeltext):
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(qtw.QLabel(labeltext))
        hbox.addStretch()
        box.addLayout(hbox)

    def add_buttons_to_outline(self, box, buttondefs):
        hbox = qtw.QHBoxLayout()
        hbox.addSpacing(50)
        for text, callback in buttondefs:
            btn = qtw.QPushButton(text, self)
            btn.clicked.connect(callback)
            hbox.addWidget(btn)
        hbox.addSpacing(50)
        box.addLayout(hbox)

    def add_okcancel_buttons(self, oktext):
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton(oktext, self)
        btn.clicked.connect(self.accept)
        btn.setDefault(True)
        hbox.addWidget(btn)
        btn = qtw.QPushButton('&Cancel', self)
        btn.clicked.connect(self.reject)
        hbox.addWidget(btn)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

    def finalize_dialog(self, focusfield):
        self.setLayout(self.vbox)
        focusfield.setFocus()

    def meld(self, title, text):
        qtw.QMessageBox.information(self, title, text)

    def ask_question(self, title, message):
        """attribuut verwijderen
        """
        ok = qtw.QMessageBox.question(self, title, message,
                                      qtw.QMessageBox.StandardButton.Ok
                                      | qtw.QMessageBox.StandardButton.Cancel,
                                      qtw.QMessageBox.StandardButton.Ok)
        return ok == qtw.QMessageBox.StandardButton.Ok

    def accept(self):
        """reimplemented
        """
        self.mathter.confirm()
        super().accept()


class TextDialogGui(EditDialogGui):
    """dialoog om een ongedefinieerde tekst (bv. van een commentaar) weer te geven
    d.m.v. een multiline tekst box
    """

    def add_textfield(self, text):
        hbox = qtw.QHBoxLayout()
        field = qtw.QTextEdit(self)
        # self.data_text.resize(440, 280)
        hbox.addSpacing(50)
        field.setText(text)
        hbox.addWidget(field)
        hbox.addSpacing(50)
        self.vbox.addLayout(hbox)
        return field

    def get_textfield_text(self, field):
        return field.toPlainText()


class GridDialogGui(EditDialogGui):
    """dialoog om stijl definities voor een (groep van) selector(s) op te voeren
    of te wijzigen
    """

    def add_table_to_outline(self, box, headers, widths, itemlist):
        hbox = qtw.QHBoxLayout()
        table = qtw.QTableWidget(self)
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        hdr = table.horizontalHeader()
        for column, width in enumerate(widths):
            hdr.resizeSection(column, width)
        hdr.setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        table.setTabKeyNavigation(False)
        if itemlist is not None:
            for attr, value in itemlist:
                idx = self.attr_table.rowCount()
                table.insertRow(idx)
                item = qtw.QTableWidgetItem(attr)
                table.setItem(idx, 0, item)
                item = qtw.QTableWidgetItem(value)
                table.setItem(idx, 1, item)
        else:
            self.row = -1
        hbox.addWidget(table)
        box.addLayout(hbox)
        return table

    def getroecount(self, table):
        return table.rowCount()

    def get_tableitem(self, table, row, column):
        return table.item(row, column)

    def get_item_text(self, tableitem):
        return tableitem.text()

    def add_row_to_table(self, table):
        """property toevoegen:
        in dit geval hoef ik alleen maar een lege regel aan de tabel toe te voegen
        """
        num = table.rowCount()
        table.setRowCount(num + 1)

    def delete_row_from_table(self, table):
        table.removeRow(currentRow())


class ListDialogGui(EditDialogGui):
    """dialoog om een list type property toe te voegen of te wijzigen
    """

    def select_item(self, title, caption, choices, current_index=0, editable=False):
        text, ok = qtw.QInputDialog.getItem(self, title, caption , options, current_index,
                                            editable)
        return text, ok

    def add_list_to_outline(self, box, items):
        hbox = qtw.QHBoxLayout()
        hbox.addSpacing(50)
        lbox = qtw.QListWidget(self)
        if items:
            lbox.addItems(items)
        hbox.addWidget(lbox)
        hbox.addSpacing(50)
        box.addLayout(hbox)
        return lbox

    def ask_for_text(self, title, caption, text=''):
        text, ok = qtw.QInputDialog.getText(self, title, caption, text=text)
        return text, ok

    def add_row_to_list(self, lbox, itemtext):
        "item toevoegen"
        lbox.addItem(itemtext)

    def get_listitem(self, lbox, row=-1):
        if listitem == -1:
            return lbox.currentItem()
        else:
            return lbox.item(row)

    def get_itemtext(self, item):
        return item.text()

    def set_itemtext(self, item, text):
        item.setText(text)

    def delete_row_from_table(self, lbox):
        "item verwijderen"
        list.takeItem(list.currentRow())

    def get_list_length(self, lbox):
        return lbox.count()
