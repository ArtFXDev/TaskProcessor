from PySide2 import QtWidgets, QtGui, QtCore

import PebblesUI, ContextSelect, NodeGraph

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    cs = ContextSelect.ContextSelect()
    cs.show()
    app.exec_()
