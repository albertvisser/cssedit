import os
import sys

import PyQt4.QtGui as gui
import PyQt4.QtCore as core

try:
    import cssedit.editor.cssedit as ed
except ImportError as e:
    try:
        import editor.cssedit as ed
    except ImportError as e:
        import cssedit as ed

RTYPES, CTYPES = [], set()
for ruletype, components in ed.RTYPES.items():
    RTYPES.append(components[0])
    CTYPES.update([x for x in components[1]])

def newitem(text, data=None):
    text = str(text)
    # if data = None:
        # data = text
    item = gui.QTreeWidgetItem()
    item.setText(0, text)
    # item.setData(0, data, core.Qt.UserRole)
    item.setToolTip(0, text)
    return item

def _addsubitems(parent, item):
    for idx in range(item.childCount()):
        child = item.child(idx)
        subitem = newitem(child.text(0)) # , item.data(0)
        parent.addChild(subitem)
        _addsubitems(subitem, child)

def _paste(item, parent, ix=-1):
    new = newitem(item.text(0)) # , item.data(0)
    if ix == -1:
        parent.addChild(new)
    else:
        parent.insertChild(ix, new)
    _addsubitems(new, item)

def read_rules(data):
    "recursive structure to read rules"
    rules = []
    for rltype, rldata in data:
        ruletypeitem = newitem(rltype)
        for key in sorted(rldata):
            if key == 'seqnum': continue
            value = rldata[key]
            ruletopitem = newitem(key)
            if key in ('text', 'data'):
                rulekeyitem = newitem(value)
                ruletopitem.addChild(rulekeyitem)
            elif key == 'rules':
                for rulekeyitem in read_rules(value):
                    ruletopitem.addChild(rulekeyitem)
            else:
                for it in sorted(value):
                    rulekeyitem = newitem(it)
                    try:
                        rulevalueitem = newitem(str(value[it]))
                        rulekeyitem.addChild(rulevalueitem)
                    except TypeError:
                        pass
                    ruletopitem.addChild(rulekeyitem)
            ruletypeitem.addChild(ruletopitem)
        rules.append(ruletypeitem)
    return rules

class LogDialog(gui.QDialog):
    "Simple Log display"

    text = "css definition that triggers this message:\n\n"

    def __init__(self, parent, log):
        self.parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(self.parent.app_title + " - show log for current file")
        ## self.setWindowIcon(self.parent.app_icon)
        txt = gui.QLabel("Dubbelklik op een regel om de context "
            "(definitie in de css ) te bekijken")
        self.lijst = gui.QListWidget(self)
        ## self.lijst.setSelectionMode(gui.QAbstractItemView.SingleSelection)
        self.lijst.addItems(log)
        b1 = gui.QPushButton("&Toon Context", self)
        b1.clicked.connect(self.show_context)
        b2 = gui.QPushButton("&Klaar", self)
        b2.clicked.connect(self.done)

        vbox = gui.QVBoxLayout()

        hbox = gui.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.lijst)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addWidget(b1)
        hbox.addWidget(b2)
        hbox.insertStretch(0, 1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.resize(600, 480)
        self.exec_()


    def itemDoubleClicked(self, item):
        self.show_context(item)

    def show_context(self, item=None):
        """show full logline (in case it's been chopped off)
        and the definition that triggered it
        """
        # determine selected line in the list and get associated data
        selected = item or self.lijst.currentItem()
        y = ed.parse_log_line(selected.text())
        context = ed.get_definition_from_file(self.parent.project_file, y.line,
            y.pos)
        # pop up a box to show the data
        title = self.parent.app_title + " - show context for log message"
        popup = gui.QMessageBox.information(self, title, self.text + context)

    def done(self, arg=None):
        """finish dialog
        """
        gui.QDialog.done(self, 0)


class TextDialog(gui.QDialog):
    """dialoog om een ongedefinieerde tekst (bv. van een commentaar) weer te geven
    d.m.v. een multiline tekst box
    """
    def __init__(self, parent, title='', text='', comment=False):
        self._parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.resize(440, 280)
        vbox = gui.QVBoxLayout()

        hbox = gui.QHBoxLayout()
        self.data_text = gui.QTextEdit(self)
        ## self.data_text.resize(440, 280)
        hbox.addSpacing(50)
        self.data_text.setText(text)
        hbox.addWidget(self.data_text)
        hbox.addSpacing(50)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        btn = gui.QPushButton('&Save', self)
        btn.clicked.connect(self.on_ok)
        btn.setDefault(True)
        hbox.addWidget(btn)
        btn = gui.QPushButton('&Cancel', self)
        btn.clicked.connect(self.on_cancel)
        hbox.addWidget(btn)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.data_text.setFocus()

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        self._parent.dialog_data = str(self.data_text.toPlainText())
        gui.QDialog.done(self, gui.QDialog.Accepted)

class GridDialog(gui.QDialog):
    """dialoog om stijl definities voor een (groep van) selector(s) op te voeren
    of te wijzigen
    """
    def __init__(self, parent, title='', itemlist=None, comment=False):
        self._parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        ## self.setWindowIcon(gui.QIcon(os.path.join(PPATH,"ashe.ico")))
        vbox = gui.QVBoxLayout()

        sbox = gui.QFrame()
        sbox.setFrameStyle(gui.QFrame.Box)
        box = gui.QVBoxLayout()

        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(gui.QLabel("Items in table:", self))
        hbox.addStretch()
        box.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        self.attr_table = gui.QTableWidget(self)
        ## self.attr_table.resize(540, 340)
        self.attr_table.setColumnCount(2)
        self.attr_table.setHorizontalHeaderLabels(['property', 'value']) # alleen zo te wijzigen
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
                item = gui.QTableWidgetItem(attr)
                self.attr_table.setItem(idx, 0, item)
                item = gui.QTableWidgetItem(value)
                self.attr_table.setItem(idx, 1, item)
        else:
            self.row = -1
        ## hbox.addStretch()
        hbox.addWidget(self.attr_table)
        ## hbox.addStretch()
        box.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addSpacing(50)
        btn = gui.QPushButton('&Add Item', self)
        btn.clicked.connect(self.on_add)
        hbox.addWidget(btn)
        btn = gui.QPushButton('&Delete Selected', self)
        btn.clicked.connect(self.on_del)
        hbox.addWidget(btn)
        hbox.addSpacing(50)
        box.addLayout(hbox)

        sbox.setLayout(box)
        vbox.addWidget(sbox)

        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        btn = gui.QPushButton('&Save', self)
        btn.clicked.connect(self.on_ok)
        btn.setDefault(True)
        hbox.addWidget(btn)
        btn = gui.QPushButton('&Cancel', self)
        btn.clicked.connect(self.on_cancel)
        hbox.addWidget(btn)
        vbox.addLayout(hbox)
        hbox.addStretch()

        self.setLayout(vbox)

    ## def on_resize(self, evt=None):
        ## self.attr_table.SetColSize(1, self.attr_table.GetSize()[0] - 162) # 178) # 160)
        ## self.attr_table.ForceRefresh()

    def on_add(self, evt=None):
        """property toevoegen:
        in dit geval hoef ik alleen maar een lege regel aan de tabel toe te voegen
        """
        ## self.attr_table.setFocus()
        num = self.attr_table.rowCount()
        self.attr_table.setRowCount(num + 1)
        ## self.attr_table.insertRow(idx) # waarom niet addRow?
        ## self.attr_table.setCurrentCell(idx, 0)

    def on_del(self, evt=None):
        "attribuut verwijderen"
        ok = gui.QMessageBox.question(self, 'Delete row from table',
            'Are you sure?', gui.QMessageBox.Ok | gui.QMessageBox.Cancel,
            gui.QMessageBox.Ok)
        if ok == gui.QMessageBox.Ok:
            self.attr_table.removeRow(self.attr_table.currentRow())

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        "controle bij OK aanklikken"
        proplist = []
        for i in range(self.attr_table.rowCount()):
            name = str(self.attr_table.item(i, 0).text())
            value = str(self.attr_table.item(i, 1).text())
            proplist.append((name, value))
        self._parent.dialog_data = proplist
        gui.QDialog.done(self, gui.QDialog.Accepted)

class ListDialog(gui.QDialog):
    'dialoog om een list toe te voegen'

    def __init__(self, parent, title='', itemlist=None, comment=False):
        self._parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.is_rules_node = "'rules'" in title
        vbox = gui.QVBoxLayout()

        sbox = gui.QFrame()
        sbox.setFrameStyle(gui.QFrame.Box)
        box = gui.QVBoxLayout()

        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(gui.QLabel("Items in list:", self))
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.list = gui.QListWidget(self)
        if itemlist is not None:
            self.list.addItems(itemlist)
        hbox = gui.QHBoxLayout()
        hbox.addSpacing(50)
        hbox.addWidget(self.list)
        hbox.addSpacing(50)
        box.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        btn = gui.QPushButton('&Add Item', self)
        btn.clicked.connect(self.on_add)
        hbox.addWidget(btn)
        btn = gui.QPushButton('&Edit Selected', self)
        btn.clicked.connect(self.on_edit)
        hbox.addWidget(btn)
        btn = gui.QPushButton('&Delete Selected', self)
        btn.clicked.connect(self.on_del)
        hbox.addWidget(btn)
        hbox.addStretch()
        box.addLayout(hbox)

        sbox.setLayout(box)
        vbox.addWidget(sbox)

        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        btn = gui.QPushButton('&Save', self)
        btn.clicked.connect(self.on_ok)
        btn.setDefault(True)
        hbox.addWidget(btn)
        btn = gui.QPushButton('&Cancel', self)
        btn.clicked.connect(self.on_cancel)
        hbox.addWidget(btn)
        vbox.addLayout(hbox)
        hbox.addStretch()

        self.setLayout(vbox)

    def on_add(self, evt=None):
        "item toevoegen"
        if self.is_rules_node:
            ruletypes = sorted([(x, y[0]) for x, y in ed.RTYPES.items()],
                key = lambda item: item[1])
            options = [x[1] for x in ruletypes]
            text, ok = gui.QInputDialog.getItem(self, self._parent.app_title,
                "Choose type for this rule", options, editable=False)
        else:
            text, ok = gui.QInputDialog.getText(self, 'Add item to list',
                'Enter text for this item')
        self.list.addItem(text)

    def on_edit(self, evt=None):
        "item wijzigen"
        current = self.list.currentItem()
        oldtext = current.text()
        if self.is_rules_node:
            ruletypes = sorted([(x, y[0]) for x, y in ed.RTYPES.items()],
                key = lambda item: item[1])
            options = [x[1] for x in ruletypes]
            current_index = options.index(oldtext) if oldtext else 0
            text, ok = gui.QInputDialog.getItem(self, self._parent.app_title,
                "Choose type for this rule", options, current_index, editable=False)
        else:
            text, ok = gui.QInputDialog.getText(self, 'Edit list item',
                'Enter text for this item:', text=oldtext)
        if ok and text != oldtext:
            current.setText(text)

    def on_del(self, evt=None):
        "item verwijderen"
        ok = gui.QMessageBox.question(self, 'Delete item from list',
            'Are you sure?', gui.QMessageBox.Ok | gui.QMessageBox.Cancel,
            gui.QMessageBox.Ok)
        if ok == gui.QMessageBox.Ok:
            self.list.takeItem(self.list.currentRow())

    def on_cancel(self):
        gui.QDialog.done(self, gui.QDialog.Rejected)

    def on_ok(self):
        """bij OK: de opgebouwde list via self.dialog_data doorgeven
        aan het mainwindow
        """
        list_data = []
        for row in range(self.list.count()):
            list_data.append(str(self.list.item(row).text()))
        self._parent.dialog_data = list_data
        gui.QDialog.done(self, gui.QDialog.Accepted)

class TreePanel(gui.QTreeWidget):
    "Tree structure"
    def __init__(self, parent):
        self.parent = parent
        gui.QTreeWidget.__init__(self)
        self.setColumnCount(2)
        self.hideColumn(1)
        self.setItemHidden(self.headerItem(), True)
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
        ## self.parent.check_active()
        ## h = self.currentItem()
        ## self.parent.activate_item(h)

    def dropEvent(self, event):
        """wordt aangeroepen als een versleept item (dragitem) losgelaten wordt over
        een ander (dropitem)
        Het komt er altijd *onder* te hangen als laatste item
        deze methode breidt de Treewidget methode uit met wat visuele zaken
        """
        ## dragitem = self.selectedItems()[0]
        ## dragparent = dragitem.parent()
        ## dropitem = self.itemAt(event.pos())
        ## if not dropitem:
            ## # ## event.ignore()
            ## return
        ## gui.QTreeWidget.dropEvent(self, event)
        ## count = self.topLevelItemCount()
        ## if count > 1:
            ## for ix in range(count):
                ## if self.topLevelItem(ix) == dragitem:
                    ## self.takeTopLevelItem(ix)
                    ## self.oldparent.insertChild(self.oldpos, dragitem)
                    ## self.setCurrentItem(dragitem)
                    ## break
            ## return
        ## self.parent.set_project_dirty(True)
        ## self.setCurrentItem(dragitem)
        ## dropitem.setExpanded(True)

    def mousePressEvent(self, event):
        """remember the current parent in preparation for "canceling" a dragmove
        """
        ## xc, yc = event.x(), event.y()
        ## item = self.itemAt(xc, yc)
        ## if item:
            ## self.oldparent, self.oldpos = self._getitemparentpos(item)
        gui.QTreeWidget.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        "for showing a context menu"
        ## if event.button() == core.Qt.RightButton:
            ## xc, yc = event.x(), event.y()
            ## item = self.itemAt(xc, yc)
            ## if item:
                ## self.create_popupmenu(item)
                ## return
        gui.QTreeWidget.mouseReleaseEvent(self, event)

    def keyReleaseEvent(self, event):
        "also for showing a context menu"
        ## if event.key() == core.Qt.Key_Menu:
            ## item = self.currentItem()
            ## self.create_popupmenu(item)
            ## return
        gui.QTreeWidget.keyReleaseEvent(self, event)

    def create_popupmenu(self, item):
        """create a menu in the right place"""
        ## menu = gui.QMenu()
        ## for action in self.parent.notemenu.actions():
            ## act = menu.addAction(action)
            ## if item == self.parent.root and action.text() in ('&Add', '&Delete',
                    ## '&Forward', '&Back'):
                ## action.setEnabled(False)
        ## menu.addSeparator()
        ## for action in self.parent.treemenu.actions():
            ## menu.addAction(action)
            ## if item == self.parent.root:
                ## action.setEnabled(False)
        ## menu.exec_(self.mapToGlobal(self.visualItemRect(item).center()))
        ## if item == self.parent.root:
            ## for action in self.parent.notemenu.actions():
                ## if item == self.parent.root and action.text() in ('&Add', '&Delete',
                        ## '&Forward', '&Back'):
                    ## action.setEnabled(True)
            ## for action in self.parent.treemenu.actions():
                ## action.setEnabled(True)

    def add_to_parent(self, titel, parent, pos=-1):
        """
        """
        new = gui.QTreeWidgetItem()
        new.setText(0, titel.rstrip())
        new.setToolTip(0, titel.rstrip())
        if pos == -1:
            parent.addChild(new)
        else:
            parent.insertChild(pos, new)
        return new

    def add_to_parent_2(self, item, parent, pos=-1):
        """
        """
        if pos == -1:
            parent.addChild(item)
        else:
            parent.insertChild(pos, item)
        ## return item

    def _getitemdata(self, item):
        return item.text(0), str(item.text(1)) # kan integer zijn

    def _getitemtitle(self, item):
        "titel in de visual tree ophalen"
        return item.text(0)

    def _getitemkey(self, item):
        "sleutel voor de itemdict ophalen"
        value = item.text(1)
        try:
            value = int(value)
        except ValueError: # root item heeft tekst in plaats van itemdict key
            pass
        return value

    def _setitemtitle(self, item, title):
        item.setText(0, title)
        item.setToolTip(0, title)

    def _setitemtext(self, item, text):
        """Meant to set the text for the root item (goes in same place as the keys
        for the other items)
        """
        item.setText(1, text)

    def _getitemkids(self, item):
        return [item.child(num) for num in range(item.childCount())]

    def _getitemparentpos(self, item):
        root = item.parent()
        if root:
            pos = root.indexOfChild(item)
        else:
            pos = -1
        return root, pos

    def _getselecteditem(self):
        return self.selectedItems()[0] # gui-dependent

    def _removeitem(self, item, cut_from_itemdict):
        "removes current treeitem and returns the previous one"
        log('in _removeitem {} {}'.format(item, cut_from_itemdict))
        parent = item.parent()               # gui-dependent
        pos = parent.indexOfChild(item)
        oldloc = (parent, pos)
        if pos - 1 >= 0:
            prev = parent.child(pos - 1)
        else:
            prev = parent
            if prev == self.parent.root:
                prev = parent.child(pos + 1)
        self.parent._popitems(item, cut_from_itemdict)
        ## parent.takeChild(pos)
        # bij een undo van een add moeten met " \ " toegevoegde items ook verwijderd worden
        to_remove = [(parent, pos)]
        while True:
            log('{} {} {}'.format(item, item.childCount(), item.child(0)))
            if item.childCount() == 0:
                break
            to_remove.append((item, 0)) # er is er altijd maar één
            item = item.child(0)
        for parent, pos in reversed(to_remove):
            parent.takeChild(pos)
        #
        return oldloc, prev


class MainWindow(gui.QMainWindow):
    """Hoofdscherm van de applicatie"""
    # TODO: zoeken/filteren in tags (vgl hoe dit in hotkeys is gedaan) - ook in properties voor bekijken gelijksoortige stijlen

    def __init__(self, parent=None):
        print("incoming parent:", parent)
        self.parent = parent
        gui.QMainWindow.__init__(self)
        offset = 40 if os.name != 'posix' else 10
        self.move(offset, offset)
        self.app_title = 'CSSEdit'
        self.app_icon = gui.QIcon('/home/albert/cssfile_1.xpm')

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        self.resize(800, 500)
        self.setWindowTitle(self.app_title)
        self.setWindowIcon(self.app_icon)

        self.tree = TreePanel(self)
        self.setCentralWidget(self.tree)

        self.actiondict = {}
        menubar = self.menuBar()
        self.create_menu(menubar, (
            ('&Application', (
                ('Set output &Format', (
                    ('&Compressed (no linefeeds)',), # TODO: these options
                    ('&Short',),        # should be checkable and remembered;
                    ('&Medium',),       # or would an options dialog be a better idea?
                    ('&Long',),         # see Trac wiki
                    ), '', '', 'Indicate how output should be saved'),
                ('E&xit', self.exit, 'Ctrl+Q', '', 'Quit the application' ),
                ),),
            ('&File', (
                ('&New', self.newfile, 'Ctrl+Insert', '', 'Start a new css file'),
                ('&Open', self.openfile, 'Ctrl+O', '', 'Open a css file'),
                ('&Reload', self.reopenfile, 'Ctrl+R', '',
                    'Discard all changes and reopen the current css file'),
                ('&Save', self.savefile, 'Ctrl+S', '', 'Save the current css file'),
                ('Save &As', self.savefileas, 'Ctrl+Shift+S', '',
                    'Save the current css file under a different name'),
                (),
                ('Show &Log', self.show_log, 'Ctrl+Shift+L', '',
                    'Show messages from parsing this file'),
                ),),
            ('&View', (
                ## ('&Show level', self.show_level, '', '',
                    ## 'Show number of levels under root'),
                ## ('Expand', self.expand_item, 'Alt+Plus', '', 'Expand tree item'),
                ## ('Collapse', self.collapse_item, 'Alt+Minus', '', 'Collapse tree item'),
                ('&Expand all', self.expand_all, 'Ctrl++', '',
                    'Expand all subitems'),
                ('&Collapse all', self.collapse_all, 'Ctrl+-', '',
                    'Collapse all subitems'),
                ),),
            ('&Rule', (
                ('Add under root', self.add, 'Ctrl+N', '',
                    'Add a new top level CSS rule at the end'),
                ('Insert after', self.add_after, 'Ctrl+Shift+N', '',
                    'Add a new rule after the current one'),
                ('Insert before', self.add_before, 'Ctrl+Alt+N', '',
                    'Add a new rule before the current one'),
                ('Add under "rules" node', self.add_under, 'Alt+Shift+N', '',
                    'Add a new CSS rule at the end ("rules" node only)'),
                ('Delete', self.delete, 'Del,Ctrl+D', '', 'Delete the current rule'),
                ('Cut', self.cut, 'Ctrl+X', '',
                    'Cut (copy and delete) the current rule'),
                ('Copy', self.copy, 'Ctrl+C', '', 'Copy the current rule'),
                ('Paste after', self.paste_after, 'Ctrl+V', '',
                    'Insert the copied rule after the current one'),
                ('Paste before', self.paste_before, 'Shift+Ctrl+V', '',
                    'Insert the copied rule before the current one'),
                ('Paste under "rules" node', self.paste_under, 'Ctrl+Alt+V', '',
                    'Insert the copied rule beneath the current node ("rules" only)'),
                ),),
            ('Rule &Component', (
                ('Edit', self.edit, 'F2,Ctrl+E', '', 'Edit a rule component'),
                ),),
            ))
        ## self.undo_stack = UndoRedoStack(self)
        self.css = None
        self.cut_item, self.cutlevel = None, 0
        self.newfile()

    def create_menu(self, menubar, menudata):
        """bouw het menu en de meeste toolbars op"""
        self.menus = {} # we may need this if we need to do something with specific menus later
        for item, data in menudata:
            menu = menubar.addMenu(item)
            self.menus[item] = menu
            for menudef in data:
                if not menudef:
                    menu.addSeparator()
                    continue
                label, handler, shortcut, icon, info = menudef
                if isinstance(handler, tuple): # TODO: find a nicer way
                    submenu = menu.addMenu(label)
                    for item in handler:
                        # define submenu options
                        pass
                    continue
                if icon:
                    action = gui.QAction(gui.QIcon(os.path.join(HERE, icon)), label,
                        self)
                    if not toolbar_added:
                        toolbar = self.addToolBar(item)
                        toolbar.setIconSize(core.QSize(16,16))
                        toolbar_added = True
                    toolbar.addAction(action)
                else:
                    action = gui.QAction(label, self)
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
                self.connect(action, core.SIGNAL('triggered()'), handler)
                # action.triggered.connect(handler) werkt hier niet
                if label:
                    menu.addAction(action)
                    self.actiondict[label] = action

    def show_message(self, text, title=""):
        title = title or self.app_title
        gui.QMessageBox.information(self, title, text)

    def show_statusmessage(self, text):
        self.statusbar.showMessage(text)

    def getfilename(self, title='', start='', save=False):
        if title == '':
            title = 'Save File' if save else 'Open File'
        if start == '':
            start = os.getcwd()
        filter = "CSS files (*.css)"
        if save:
            filename = gui.QFileDialog.getSaveFileName(self, title, start, filter)
        else:
            filename = gui.QFileDialog.getOpenFileName(self, title, start, filter)
        ok = True if filename else False
        return ok, filename

    def newfile(self, event=None):
        self.tree.takeTopLevelItem(0)
        self.project_file = ""
        self.css = ed.Editor(new=True)
        self.root = gui.QTreeWidgetItem()
        self.root.setText(0, "(untitled)")
        self.tree.addTopLevelItem(self.root)
        self.activeitem = self.root
        self.root.setExpanded(True)
        self.mark_dirty(False)

    def open(self, **kwargs):
        self.newfile()
        try:
            fname = kwargs['filename']
        except KeyError:
            self.project_file = ""
        else:
            self.project_file = os.path.abspath(fname)
        self.root.setText(0, self.project_file or "(no file)")

        self.css = ed.Editor(**kwargs)
        self.css.datatotext()
        self.texttotree()
        self.show_statusmessage(self.build_loaded_message())

        item_to_activate = self.root
        ## self.resize(*self.opts["ScreenSize"])
        ## self.root.setExpanded(True)
        self.tree.setCurrentItem(item_to_activate)
        self.tree.setFocus()

    def build_loaded_message(self):
        mld = 'file loaded'
        warn = err = misc = 0
        for line in self.css.log:
            if line.startswith('WARNING'):
                warn += 1
            elif line.startswith('ERROR'):
                err += 1
            else:
                misc += 1
        if warn + err + misc > 0:
            mld += ' with '
            if warn > 0:
                mld += '{} warnings'.format(warn)
                if err > 0 and misc > 0:
                    mld += ', '
                elif err > 0 or misc > 0:
                    mld += ' and '
            if err > 0:
                mld += '{} errors'.format(err)
                if misc > 0:
                    mld += ' and '
            if misc > 0:
                mld += '{} misc. messages'.format(misc)
        return mld

    def openfile(self, event=None):
        ok, filename = self.getfilename(title=self.app_title + ' - open file')
        if ok:
            self.open(filename=filename)

    def reopenfile(self, event=None):
        self.open(filename=self.project_file)

    def texttotree(self):
        self.visual_data = read_rules(self.css.textdata)
        for item in self.visual_data:
            self.root.addChild(item)

    def treetotext(self):
        data = []
        count = self.root.childCount()
        for ix in range(count):
            rule_item = self.root.child(ix)
            rule_type = rule_item.text(0)
            rule_data = {}
            for ix2 in range(rule_item.childCount()):
                key_item = rule_item.child(ix2)
                key_text = key_item.text(0)
                if key_text in ('text', 'data'):
                    key_data = key_item.child(0).text(0)
                elif key_text in ('selectors', 'media', 'rules'):
                    key_data = []
                    for ix3 in range(key_item.childCount()):
                        list_item = key_item.child(ix3)
                        key_data.append(list_item.text(0))
                        if key_text == 'rules':
                            # TODO: onderliggende ruledata toevoegen
                            pass
                elif key_text in ('styles'):
                    key_data = {}
                    for ix3 in range(key_item.childCount()):
                        dict_item = key_item.child(ix3)
                        dictitem_key = dict_item.text(0)
                        dictitem_value = dict_item.child(0).text(0)
                        key_data[dictitem_key] = dictitem_value
                rule_data[key_text] = key_data
            data.append((rule_type, rule_data))
        return data

    def savefile(self, event=None):
        if self.project_file:
            self.save()
        else:
            self.savefileas()

    def savefileas(self, event=None):
        ok, filename = self.getfilename(title=self.app_title + ' - save file as',
            start=self.project_file, save=True)
        if ok:
            self.project_file = filename
            self.save()
            self.root.setText(0, self.project_file)

    def save(self):
        self.css.filename = self.project_file
        self.css.textdata = self.treetotext()
        self.css.texttodata()
        self.css.return_to_source()
        self.mark_dirty(False)

    def show_log(self):
        if self.css:
            win = LogDialog(self, self.css.log)
        else:
            self.statusbar.showMessage('Load a css file first')

    def exit(self, event=None):
        self.close()

    def close(self, event=None):
        """for "embedded" use: return modified data to parent before closing
        """
        print(self.parent)
        if self.parent:
            self.css.textdata = self.treetotext()
            print("na treetotext:", self.css.textdata)
            self.css.texttodata()
            print("na texttodata:", self.css.data)
            self.css.return_to_source()
            print("na return_to_source:", self.css.data)
            self.parent.styledata = self.css.data
        gui.QMainWindow.close(self)

    def determine_level(self, item):
        if item.parent() == self.root:
            return 1
        else:
            return self.determine_level(item.parent()) + 1

    def checkselection(self):
        "controleer of er wel iets geselecteerd is (behalve de filenaam)"
        sel = True
        self.item = self.tree.currentItem()
        if self.item is not None: text = self.item.text(0) # waarom?
        self.itemlevel = 0
        if self.item is None or self.item == self.root:
            gui.QMessageBox.information(self, self.app_title,
                'You need to select an element or text first')
            sel = False
        else:
            self.itemlevel = self.determine_level(self.item) # TODO: check
        return sel

    def is_rule_parent(self, item):
        ok = False
        if item == self.root or item.text(0) == "rules": ok = True
        if not ok:
            gui.QMessageBox.information(self, self.app_title,
                "Can't add or paste rule here")
        return ok

    def is_rule_item(self, item):
        ok = True
        test = item.text(0)
        if test not in RTYPES: ok = False
        if not ok:
            gui.QMessageBox.information(self, self.app_title,
                "Can't do this; {} is not a rule item".format(test))
        return ok

    def mark_dirty(self, state):
        if state:
            self.setWindowTitle(self.app_title + ' (modified)')
        else:
            self.setWindowTitle(self.app_title)
        self.project_dirty = state

    def add(self, evt=None):
        self._add_rule(parent=self.root)

    def add_after(self, evt=None):
        if not self.checkselection(): return
        self._add_rule(after=True)

    def add_before(self, evt=None):
        if not self.checkselection(): return
        self._add_rule(after=False)

    def add_under(self, evt=None):
        if not self.checkselection(): return
        self._add_rule(parent=self.item)

    def _add_rule(self, parent=None, after=None):
        """add new rule
        "at the end" is only possible on top level - otherwise use the "rules" node
        """
        if parent is None:
            parent = self.item.parent()
        if not self.is_rule_parent(parent): return
        # collect all ruletypes, build and display choicedialog
        ruletypes = sorted([(x, y[0]) for x, y in ed.RTYPES.items()],
            key = lambda item: item[1])
        typename, ok = gui.QInputDialog.getItem(self, self.app_title,
            "Choose type for new rule", [x[1] for x in ruletypes], editable=False)
        # after selection, create he rule node and the component nodes
        # use ed.init_ruledata(ruletype) for this
        if ok:
            ruletype = None
            for rtype, name in ruletypes:
                if name == typename:
                    ruletype = rtype
                    break
            if ruletype is None: return
            newitem = gui.QTreeWidgetItem()
            newitem.setText(0, typename)
            for name in sorted([x for x in ed.init_ruledata(ruletype)]):
                subitem = gui.QTreeWidgetItem()
                subitem.setText(0, name)
                newitem.addChild(subitem)
            if after is None:
                parent.addChild(newitem)
            else:
                ix = parent.indexOfChild(self.item)
                if after:
                    ix += 1
                parent.insertChild(ix, newitem)
        self.mark_dirty(True)
        newitem.setExpanded(True)
        self.tree.setCurrentItem(newitem)

    def edit(self, evt=None):
        "start edit m.b.v. dialoog"
        if not self.checkselection(): return
        msg = ''
        modified = False
        data = str(self.item.text(0))
        ruletype = str(self.item.parent().text(0)).lower()
        title = "{} - edit '{}' node for {}".format(self.app_title, data, ruletype)
        if data in ed.RTYPES:
            msg = 'Edit rule via subordinate item'
        elif data in [x for x, y in CTYPES if y == ed.text_type]:
            modified = self._edit_text_node(title)
        elif data in [x for x, y in CTYPES if y == ed.list_type]:
            modified = self._edit_list_node(title) # rules, selectors
        elif data in [x for x, y in CTYPES if y == ed.table_type]:
            modified = self._edit_grid_node(title) #styles
        else:
            msg = "You can't edit this type of node"
        if msg:
            gui.QMessageBox.information(self, self.app_title, msg)
        elif modified:
            self.item.setExpanded(True)
            self.mark_dirty(True)

    def _edit_text_node(self, title):
        textnode = self.item.child(0)
        self.data = ()
        if textnode:
            data = textnode.text(0) # or textnode.data(0, core.Qt.UserRole)
        else:
            data = ''
        modified = False
        edt = TextDialog(self, title, data).exec_()
        if edt == gui.QDialog.Accepted:
            newdata = self.dialog_data
            if newdata != data:
                modified = True
                if not textnode:
                    textnode = gui.QTreeWidgetItem()
                    self.item.addChild(textnode)
                textnode.setText(0, newdata)
                ## textnode.setData(0, newdata, core.Qt.UserRole
        return modified

    def _edit_list_node(self, title):
        count = self.item.childCount()
        itemlist = [self.item.child(i).text(0) for i in range(count)]
        ## datalist = [self.item.child(i).data(0, core.Qt.UserRole)
            ## for i in range(count)]
        ## print(datalist)
        maxlen = len(itemlist)
        modified = False
        edt = ListDialog(self, title, itemlist).exec_()
        if edt == gui.QDialog.Accepted:
            newitemlist = self.dialog_data
            for ix, item in enumerate(newitemlist):
                if ix < maxlen:
                    if item != itemlist[ix]:
                        modified = True
                        node = self.item.child(ix)
                        node.setText(0, item)
                        node.setData(0, core.Qt.UserRole, item)
                else:
                    modified = True
                    newnode = gui.QTreeWidgetItem()
                    newnode.setText(0, item)
                    newnode.setData(0, core.Qt.UserRole, item)
                    self.item.addChild(newnode)
                    if self.item.text(0) == 'rules':
                        ruletype = None
                        for rtype, name in [(x, y[0]) for x, y in ed.RTYPES.items()]:
                            if name == item:
                                ruletype = rtype
                                break
                        if ruletype is None: continue
                        for name in sorted([x for x in ed.init_ruledata(ruletype)]):
                            subnode = gui.QTreeWidgetItem()
                            subnode.setText(0, name)
                            newnode.addChild(subnode)

            test = len(newitemlist)
            if test < maxlen:
                modified = True
                for ix in range(maxlen - 1, test, -1):
                    self.item.removeChild(ix)
        return modified

    def _edit_grid_node(self, title):
        count = self.item.childCount()
        itemlist = [(self.item.child(i).text(0), self.item.child(i).child(0).text(0))
            for i in range(count)]
        ## datalist = [(
                ## self.item.child(i).data(0, core.Qt.UserRole),
                ## self.item.child(i).child(0).data(0, core.Qt.UserRole))
            ## for i in range(count)]
        maxlen = len(itemlist)
        modified = False
        edt = GridDialog(self, title, itemlist).exec_()
        if edt == gui.QDialog.Accepted:
            newitemlist = self.dialog_data
            for ix, item in enumerate(newitemlist):
                node = self.item.child(ix)
                if ix < maxlen:
                    if item[0] != itemlist[ix][0]:
                        modified = True
                        node.setText(0, item[0])
                        node.setData(0, core.Qt.UserRole, item[0])
                    if item[1] != itemlist[ix][1]:
                        modified = True
                        node.child(0).setText(0, item[1])
                        node.child(0).setData(0, core.Qt.UserRole, item[1])
                else:
                    modified = True
                    newnode = gui.QTreeWidgetItem()
                    newnode.setText(0, item[0])
                    newnode.setData(0, core.Qt.UserRole, item[0])
                    newsubnode = gui.QTreeWidgetItem()
                    newsubnode.setText(0, item[1])
                    newsubnode.setData(0, core.Qt.UserRole, item[1])
                    newnode.addChild(newsubnode)
                    self.item.addChild(newnode)
            test = len(newitemlist)
            if test < maxlen:
                modified = True
                for ix in range(maxlen - 1, test, -1):
                    self.item.removeChild(ix)
        return modified
    def delete(self, evt=None):
        self._copy_rule(cut=True, retain=False)

    def cut(self, evt=None):
        self._copy_rule(cut=True, retain=True)

    def copy(self, evt=None):
        self._copy_rule(cut=False, retain=True)

    def _copy_rule(self, cut=True, retain=True):
        if not self.checkselection(): return
        if not self.is_rule_item(self.item): return
        if retain:
            self.cut_item = self.item
            self.cutlevel = self.itemlevel
        if cut:
            parent = self.item.parent()
            ix = parent.indexOfChild(self.item)
            if ix > 0:
                ix -= 1
                ## prev = parent.child(ix)
            ## else:
                ## prev = parent
                ## if prev == self.root:
                    ## prev = parent.child(ix+1)
            parent.removeChild(self.item)
            self.mark_dirty(True)
            ## self.tree.setCurrentItem(prev)

    def paste_under(self, evt=None):
        self._paste_rule(under=True)

    def paste_after(self, evt=None):
        self._paste_rule()

    def paste_before(self, evt=None):
        self._paste_rule(after=False)

    def _paste_rule(self, under=False, after=True):
        if not self.checkselection(): return
        parent = self.item if under else self.item.parent()
        if not self.is_rule_parent(parent): return
        if under:
            _paste(self.cut_item, parent)
        else:
            indx = parent.indexOfChild(self.item)
            if after:
                indx += 1
                text = 'after'
            else:
                ## indx -= 1
                text = 'before'
            _paste(self.cut_item, parent, indx)
        self.mark_dirty(True)

    def expand_item(self):
        self._expand()

    def expand_all(self):
        self._expand(recursive=True)

    def _expand(self, recursive=False):
        "expandeer tree vanaf huidige item"
        def expand_all(item):
            for ix in range(item.childCount()):
                sub = item.child(ix)
                sub.setExpanded(True)
                expand_all(sub)
        item = self.tree.currentItem()
        self.tree.expandItem(item)
        if recursive:
            expand_all(item)

    def collapse_item(self):
        self._collapse()

    def collapse_all(self):
        self._collapse(recursive=True)

    def _collapse(self, recursive=False):
        "collapse huidige item en daaronder"
        def collapse_all(item):
            for ix in range(item.childCount()):
                sub = item.child(ix)
                collapse_all(sub)
                sub.setExpanded(False)
        item = self.tree.currentItem()
        if recursive:
            collapse_all(item)
        self.tree.collapseItem(item)


    # temporary methods
    def no_op(self, event=None):
        pass

    def show_level(self, event=None):
        """test method for determine_level"""
        if not self.checkselection(): return
        level = self.determine_level(self.item)
        gui.QMessageBox.information(self, self.app_title,
            'This element is at level {}'.format(level))

def main(**kwargs):
    app = gui.QApplication(sys.argv)
    main = MainWindow()
    ## app.setWindowIcon(main.nt_icon)
    main.show()
    if kwargs:
        main.open(**kwargs) # no error return, throws an exception if needed
    ## if err:
        ## gui.QMessageBox.information(main, "Error", err, gui.QMessageBox.Ok)
    app.exec_()
