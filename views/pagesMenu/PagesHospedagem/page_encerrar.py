# Imports necessários do PySide6 e operações personalizadas
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QSpacerItem, QSizePolicy, QFrame, QLineEdit, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem
)

class Ui_page_encerrar(QWidget):
    def __init__(self, hospedagem, parent=None):
        super().__init__(parent)
        self.hospedagem = hospedagem

        main_layout = QVBoxLayout(self)

        # Fontes utilizadas
        font_title = QFont()
        font_title.setPointSize(14)
        font_content = QFont()
        font_content.setPointSize(10)

        # Container da ficha da hospedagem
        group_box = QGroupBox("Ficha da Hospedagem")
        group_box.setFont(font_content)
        group_layout = QVBoxLayout(group_box)

        # Layout com campos para adicionar nova despesa
        input_layout = QHBoxLayout()
        self.input_descricao = QLineEdit()
        self.input_descricao.setPlaceholderText("Descrição do produto")
        input_layout.addWidget(self.input_descricao)

        self.input_valor = QLineEdit('Valor a pagar')
        self.input_valor.setMaximumWidth(100)
        input_layout.addWidget(self.input_valor)

        self.input_quantidade = QSpinBox()
        self.input_quantidade.setMinimum(1)
        input_layout.addWidget(self.input_quantidade)

        self.btn_adicionar = QPushButton("Adicionar")
        input_layout.addWidget(self.btn_adicionar)

        group_layout.addLayout(input_layout)

        main_layout.addWidget(group_box)

