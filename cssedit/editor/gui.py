"import gui functions to use: rederection to real imports depending on toolkit setting"
from .toolkit import toolkit
if toolkit == 'qt':
    from .gui_qt import MainGui, TextDialog, ListDialog, GridDialog, LogDialog
else:
    raise Importerror('Incorrect GUI toolkit specified')
