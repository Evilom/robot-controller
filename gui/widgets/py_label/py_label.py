# ///////////////////////////////////////////////////////////////
# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# STYLE
# ///////////////////////////////////////////////////////////////
label_style = '''
QLabel {{
    color: {_color};
    background-color: {_bg_color};
    border-radius: {_radius};
    padding: {_padding};
}}
'''

# PY LABEL
# ///////////////////////////////////////////////////////////////
class PyLabel(QLabel):
    def __init__(
        self,
        text = "",
        radius = 8,
        color = "#FFF",
        bg_color = "#333",
        padding="5px",
        parent = None,
    ):
        super().__init__()

        # SET PARAMETERS
        self.setText(text)
        if parent != None:
            self.setParent(parent)

        # SET STYLESHEET
        custom_style = label_style.format(
            _color = color,
            _radius = radius,
            _bg_color = bg_color,
            _padding = padding
        )
        self.setStyleSheet(custom_style)