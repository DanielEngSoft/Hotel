from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QHBoxLayout
)

from operations.Ui.produtos_operations import buscar_produto_por_nome
from styles.styles import style_botao_verde


class Ui_page_listar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, page_listar):
        if not page_listar.objectName():
            page_listar.setObjectName("page_listar")

        # Fonte padrão
        font = QFont()
        font.setPointSize(14)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Campo de busca
        busca_layout = QHBoxLayout()
        self.lineEdit_busca = QLineEdit()
        self.lineEdit_busca.setPlaceholderText("Digite a descrição do produto")
        self.lineEdit_busca.setFont(font)
        self.lineEdit_busca.textChanged.connect(self.buscar_produtos)

        busca_layout.addWidget(self.lineEdit_busca)

        # Tabela de hóspedes
        self.tableWidget = QTableWidget()
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels([ "Valor", "Descrição"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.setFont(font)
        # Mensagem de erro ou info
        self.label_info = QLabel("")
        self.label_info.setFont(font)
        self.label_info.setStyleSheet("color: red;")

        # Adiciona widgets ao layout principal
        layout.addLayout(busca_layout)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.label_info)


        # Mostrar todos os hóspedes ao carregar
        self.buscar_produtos(todos=True)

    def buscar_produtos(self, todos=False):
        termo = self.lineEdit_busca.text().strip().lower()
        self.label_info.setText("")
        self.tableWidget.setRowCount(0)

        # Busca inicial traz todos os produtos
        resultados = buscar_produto_por_nome("")

        # Filtra por descrição
        if termo:
            resultados = [
                p for p in resultados
                if termo in p.descricao.lower()
            ]

        if not resultados:
            self.label_info.setStyleSheet("color: gray;")
            self.label_info.setText("Nenhum produto encontrado.")
            return

        # Popular tabela
        self.tableWidget.setRowCount(len(resultados))
        for row, produto in enumerate(resultados):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(produto.valor)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(produto.descricao))