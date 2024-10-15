# IMPORT QT CORE
from qt_core import *

# STYLE
combobox_style = '''
QComboBox {{
    color: {_color};
    background-color: {_bg_color};
    border: {_border};
    border-radius: {_radius};
    padding: {_padding};
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px; 
    border-left-width: 1px;
    border-left-color: {_border_color};
    border-left-style: solid;
    border-top-right-radius: {_radius};
    border-bottom-right-radius: {_radius};
    background-color: {_bg_color};
}}
QComboBox QAbstractItemView {{
    background-color: {_bg_color};
    border: 1px solid {_border_color};
    selection-background-color: {_selection_bg_color};
}}
'''

# PY COMBO BOX
class PyComboBox(QComboBox):
    def __init__(
        self,
        items=None,
        radius="5px",
        color="black",
        bg_color="white",
        border="1px solid gray",
        padding="5px",
        border_color="gray",
        selection_bg_color="blue",
        parent=None,
    ):
        super().__init__()

        # SET PARAMETERS
        if items is not None:
            self.addItems(items)
        if parent is not None:
            self.setParent(parent)

        # SET STYLESHEET
        custom_style = combobox_style.format(
            _color=color,
            _radius=radius,
            _bg_color=bg_color,
            _border=border,
            _padding=padding,
            _border_color=border_color,
            _selection_bg_color=selection_bg_color
        )
        self.setStyleSheet(custom_style)