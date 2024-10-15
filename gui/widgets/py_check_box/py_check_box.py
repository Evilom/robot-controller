# IMPORT QT CORE
from qt_core import *

# STYLE
checkbox_style = '''
QCheckBox {{
    color: {_color};
    background-color: {_bg_color};
    border-radius: {_radius};
    padding: {_padding};
}}
QCheckBox::indicator {{
    width: {_indicator_size};
    height: {_indicator_size};
}}
'''

# PY CHECK BOX
class PyCheckBox(QCheckBox):
    def __init__(
        self,
        text="",
        radius="5px",
        color="black",
        bg_color="transparent",
        padding="5px",
        indicator_size="15px",
        parent=None,
    ):
        super().__init__()

        # SET PARAMETERS
        self.setText(text)
        if parent is not None:
            self.setParent(parent)

        # SET STYLESHEET
        custom_style = checkbox_style.format(
            _color=color,
            _radius=radius,
            _bg_color=bg_color,
            _padding=padding,
            _indicator_size=indicator_size
        )
        self.setStyleSheet(custom_style)
