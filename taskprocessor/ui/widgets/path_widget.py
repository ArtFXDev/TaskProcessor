from Qt import QtCore, QtWidgets
from NodeGraphQt import NodeBaseWidget
from NodeGraphQt.constants import VIEWER_GRID_COLOR
from pathlib import Path

current_dir = Path.home().resolve().as_posix()


class PathWidget(NodeBaseWidget):
    def __init__(self, parent=None, name='', label='', text='', ext_filter='*'):
        super(PathWidget, self).__init__(parent, name, label)
        self.ext_filter = ext_filter

        plt = self.palette()
        bg_color = plt.alternateBase().color().toTuple()
        btn_color = plt.button().color().toTuple()
        btn_txt_color = plt.buttonText().color().toTuple()
        text_color = plt.text().color().toTuple()
        text_sel_color = plt.highlightedText().color().toTuple()
        style_dict = {
            'QLineEdit': {
                'background': 'rgba({0},{1},{2},20)'.format(*bg_color),
                'border': '1px solid rgb({0},{1},{2})'.format(*VIEWER_GRID_COLOR),
                'border-radius': '3px',
                'color': 'rgba({0},{1},{2},150)'.format(*text_color),
                'selection-background-color': 'rgba({0},{1},{2},100)'.format(*text_sel_color),
            },
            'QPushButton': {
                'background-color': 'rgba({0},{1},{2},20)'.format(*btn_color),
                'border': '1px solid rgb({0},{1},{2})'.format(*VIEWER_GRID_COLOR),
                'border-radius': '3px',
                'color': 'rgba({0},{1},{2},150)'.format(*btn_txt_color),
                'selection-background-color': 'rgba({0},{1},{2},100)'.format(*text_sel_color),
                'width': 36
            }
        }
        stylesheet = ''
        for css_class, css in style_dict.items():
            style = '{} {{\n'.format(css_class)
            for elm_name, elm_val in css.items():
                style += '  {}:{};\n'.format(elm_name, elm_val)
            style += '}\n'
            stylesheet += style

        self.layout = QtWidgets.QHBoxLayout()

        self.l_edit = QtWidgets.QLineEdit()
        self.l_edit.setText(text)
        self.l_edit.setStyleSheet(stylesheet)
        self.l_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.l_edit.editingFinished.connect(self.on_value_changed)
        self.l_edit.clearFocus()

        self.file_browser_button = QtWidgets.QPushButton("...")
        self.file_browser_button.setStyleSheet(stylesheet)
        self.file_browser_button.clicked.connect(self.on_file_browser_clicked)

        self.layout.addWidget(self.l_edit)
        self.layout.addWidget(self.file_browser_button)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)

        self.set_custom_widget(widget)
        self.l_edit.setMaximumWidth(200)

    @property
    def type_(self):
        return 'PathNodeWidget'

    def get_value(self):
        return str(self.l_edit.text())

    def set_value(self, text=''):
        if text != self.get_value():
            self.l_edit.setText(text)
            self.on_value_changed()

    def on_file_browser_clicked(self):
        global current_dir
        file_out = QtWidgets.QFileDialog.getOpenFileName(caption=self.get_label(),
                                                         dir=current_dir,
                                                         filter=self.ext_filter)
        file = file_out[0] or None
        if file is not None:
            current_dir = file
            self.set_value(file)
