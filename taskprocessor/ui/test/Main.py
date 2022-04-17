from PySide2 import QtWidgets

from taskprocessor.ui.windows import context_select_window

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    cs = ContextSelect.ContextSelectWindow()
    cs.show()
    app.exec_()
