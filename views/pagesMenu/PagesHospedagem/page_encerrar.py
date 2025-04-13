from PySide6.QtWidgets import QWidget

class Ui_page_encerrar(QWidget):
    def __init__(self, hospedagem, parent=None):
        super().__init__(parent)
        self.hospedagem = hospedagem

