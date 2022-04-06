from Qt import QtGui
from NodeGraphQt.widgets.node_widgets import NodeLineEdit


class IntWidget(NodeLineEdit):

    def __init__(self, parent=None, name='', label='', value=0):
        super(IntWidget, self).__init__(parent, name, label, str(value))
        validator = QtGui.QIntValidator(parent=self.get_custom_widget())
        self.get_custom_widget().setValidator(validator)

    def get_value(self):
        return int(self.get_custom_widget().text())

    def set_value(self, value=0):
        if value != self.get_value():
            self.get_custom_widget().setText(str(value))
            self.on_value_changed()
