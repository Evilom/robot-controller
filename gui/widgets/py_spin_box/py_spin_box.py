# IMPORT QT CORE
from qt_core import *

# STYLE
spinbox_style = '''
QSpinBox {{
    color: {_color};
    background-color: {_bg_color};
    border: {_border};
    border-radius: {_radius};
    padding: {_padding};
}}
'''

# PY SPIN BOX
class PySpinBox(QSpinBox):
    def __init__(
        self,
        min_value=0,
        max_value=100,
        initial_value=0,
        radius="5px",
        color="black",
        bg_color="white",
        border="1px solid gray",
        padding="5px",
        parent=None,
    ):
        super().__init__()

        # SET PARAMETERS
        self.setRange(min_value, max_value)
        self.setValue(initial_value)
        if parent is not None:
            self.setParent(parent)

        # SET STYLESHEET
        custom_style = spinbox_style.format(
            _color=color,
            _radius=radius,
            _bg_color=bg_color,
            _border=border,
            _padding=padding
        )
        self.setStyleSheet(custom_style)
