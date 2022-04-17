import sys
from Qt import QtWidgets
from taskprocessor.ui.windows import ContextSelectWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    cs = ContextSelectWindow()
    cs.show()
    sys.exit(app.exec_())
