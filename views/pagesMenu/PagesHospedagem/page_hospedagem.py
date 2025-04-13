from PySide6.QtWidgets import (
    QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel
)
from PySide6.QtCore import Qt

from page_ficha import Ui_page_ficha


class Ui_page_hospedagem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hospedagem Completa")
        self.setMinimumSize(800, 600)

        # Widget central e layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # QStackedWidget com duas páginas
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Página ficha (a ser modificada por você depois)
        self.page_ficha = Ui_page_ficha(self)  # ou apenas Ui_page_ficha() se ela não precisar de parent
        self.stacked_widget.addWidget(self.page_ficha)

        # Página encerrar
        self.page_encerrar = QWidget()
        self.page_encerrar_layout = QVBoxLayout(self.page_encerrar)
        self.page_encerrar_layout.addWidget(QLabel("Página Encerrar - Em construção"))
        self.stacked_widget.addWidget(self.page_encerrar)

        # Botões de navegação para exemplo
        self.btn_ir_para_ficha = QPushButton("Ir para Ficha")
        self.btn_ir_para_encerrar = QPushButton("Ir para Encerrar")
        layout.addWidget(self.btn_ir_para_ficha)
        layout.addWidget(self.btn_ir_para_encerrar)

        self.btn_ir_para_ficha.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_ficha))
        self.btn_ir_para_encerrar.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_encerrar))


# Execução de teste
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = Ui_page_hospedagem()
    window.show()
    sys.exit(app.exec())
