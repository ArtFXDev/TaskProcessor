from PySide2 import QtWidgets
from Qt import QtCompat

from taskprocessor.ui.windows import CONTEXT_SELECT_UI_PATH, EditorWindow
from taskprocessor.ui import ui_manager


class ContextSelectWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ContextSelectWindow, self).__init__()
        QtCompat.loadUi(CONTEXT_SELECT_UI_PATH, self)

        self.mayaButton.clicked.connect(self.set_context)

    def set_context(self):
        print("Maya context selected!")
        # send message to core about what context has been chosen
        ui_manager.set_engine("maya")

        self.close()
        EditorWindow.display()
