from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QHBoxLayout
)

from operations.Ui.produtos_operations import buscar_produto_por_nome
from styles.styles import style_botao_verde


class Ui_page_listar_produto(QWidget):
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
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)

        # Campo de busca
        layout_buscar = QHBoxLayout()
        self.lineEdit_busca = QLineEdit()
        self.lineEdit_busca.setPlaceholderText("Digite a descrição do produto")
        self.lineEdit_busca.setFont(font)
        self.lineEdit_busca.textChanged.connect(self.buscar_produtos)

        layout_buscar.addWidget(self.lineEdit_busca)

        # Tabela de hóspedes
        self.table_hospedes = QTableWidget()
        self.table_hospedes.setAlternatingRowColors(True)
        self.table_hospedes.setColumnCount(2)
        self.table_hospedes.setHorizontalHeaderLabels([ "Valor", "Descrição"])
        self.table_hospedes.horizontalHeader().setStretchLastSection(True)
        self.table_hospedes.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_hospedes.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_hospedes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_hospedes.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_hospedes.setFont(font)
        # Mensagem de erro ou info
        self.label_info = QLabel("")
        self.label_info.setFont(font)
        self.label_info.setStyleSheet("color: red;")

        # Adiciona widgets ao layout principal
        layout_principal.addLayout(layout_buscar)
        layout_principal.addWidget(self.table_hospedes)
        layout_principal.addWidget(self.label_info)


        # Mostrar todos os hóspedes ao carregar
        self.buscar_produtos(todos=True)

    def buscar_produtos(self, todos=False):
        termo = self.lineEdit_busca.text().strip().lower()
        self.label_info.setText("")
        self.table_hospedes.setRowCount(0)

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
        self.table_hospedes.setRowCount(len(resultados))
        for row, produto in enumerate(resultados):
            self.table_hospedes.setItem(row, 0, QTableWidgetItem(str(produto.valor)))
            self.table_hospedes.setItem(row, 1, QTableWidgetItem(produto.descricao))