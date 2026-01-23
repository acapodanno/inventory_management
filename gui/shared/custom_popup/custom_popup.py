from PySide6.QtWidgets import (
    QDialog,QDialogButtonBox,QVBoxLayout,QLabel
)
class CustomPopup(QDialog):
    """ Custom popup dialog for displaying messages. """
    def __init__(self,title,label,parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(label))
        btn_pk= QDialogButtonBox(QDialogButtonBox.Ok)
        btn_pk.accepted.connect(self.accept)
        layout.addWidget(btn_pk)
