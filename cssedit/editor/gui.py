"import gui functions to use: rederection to real imports depending on toolkit setting"
from .toolkit import toolkit
if toolkit == 'qt':
    from .gui_qt import MainGui, TextDialogGui, ListDialogGui, GridDialogGui, LogDialogGui
else:
    raise ImportError('Incorrect GUI toolkit specified')
