from PySide2 import QtWidgets, QtGui, QtCore
from Qt import QtCompat

import PebblesUI

from pathlib import Path
from taskprocessor.ui import ui_manager

ui_path = Path(__file__).parent / 'qt' / 'contextselect.ui'


class ContextSelect(QtWidgets.QDialog):
    def __init__(self):
        super(ContextSelect, self).__init__()
        QtCompat.loadUi(str(ui_path), self)

        self.mayaButton.clicked.connect(self.set_context)

    def set_context(self):
        print("Maya context selected!")
        # send message to core about what context has been chosen
        ui_manager.set_engine("maya")

        main_window = PebblesUI.PebblesWindow()
        self.hide()
        main_window.display_window()
