from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QSpacerItem, QSizePolicy, QFrame, QLineEdit, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem
)
from datetime import datetime

from operations.Ui.produtos_operations import buscar_produto_por_nome
from operations.Ui.despesas_operations import buscar_despesas_por_id_hospedagem
from models.models import Produto
from operations.Ui.despesas_operations import create_despesa

class JanelaHospedagem(QWidget):
    def __init__(self, hospedagem, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Hospedagem - Quarto {getattr(hospedagem.quarto, 'numero', 'Desconhecido')}")
        self.hospedagem = hospedagem
        screen_geometry = self.screen().geometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.setGeometry(x, y, 800, 600)
        self.setMaximumSize(800, 600)

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        font_title = QFont()
        font_title.setPointSize(14)
        font_content = QFont()
        font_content.setPointSize(10)

        main_layout = QVBoxLayout(self)

        group_box = QGroupBox("Ficha da Hospedagem")
        group_layout = QVBoxLayout(group_box)

        # Header com nome e quarto
        header_layout = QHBoxLayout()
        self.label_nome = QLabel(hospedagem.hospede.nome)
        self.label_nome.setFont(font_title)
        header_layout.addWidget(self.label_nome)

        header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.label_quarto = QLabel(f"Quarto: {hospedagem.quarto.numero}")
        self.label_quarto.setFont(font_title)
        header_layout.addWidget(self.label_quarto)

        group_layout.addLayout(header_layout)

        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        group_layout.addWidget(line)

        # Campo de descrição + quantidade + botão
        input_layout = QHBoxLayout()
        self.input_descricao = QLineEdit()
        self.input_descricao.setFont(font_content)
        self.input_descricao.setPlaceholderText("Descrição do produto")
        input_layout.addWidget(self.input_descricao)

        self.input_quantidade = QSpinBox()
        self.input_quantidade.setFont(font_content)
        self.input_quantidade.setMinimum(1)
        input_layout.addWidget(self.input_quantidade)

        self.btn_adicionar = QPushButton("Adicionar")
        self.btn_adicionar.setFont(font_content)
        input_layout.addWidget(self.btn_adicionar)

        group_layout.addLayout(input_layout)

        # Lista de sugestões de produtos
        self.lista_sugestoes = QListWidget()
        self.lista_sugestoes.setMaximumHeight(100)
        self.lista_sugestoes.setFont(font_content)
        self.lista_sugestoes.setVisible(False)
        group_layout.addWidget(self.lista_sugestoes)

        # Conecta sinais
        self.produto_selecionado = None
        self.input_descricao.textChanged.connect(self.atualizar_sugestoes)
        self.lista_sugestoes.itemClicked.connect(self.selecionar_sugestao)
        self.btn_adicionar.clicked.connect(self.adicionar_despesa)

        # Tabela de despesas
        self.tabela = QTableWidget(0, 5)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)  # impede edição direta
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela.setHorizontalHeaderLabels(["Data", "Descrição", "QTD", "Valor", "TOTAL"])

        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.tabela.setFont(font_content)
        group_layout.addWidget(self.tabela)

        # Rodapé com totais
        totals_layout = QHBoxLayout()
        self.label_diarias = QLabel("  Diárias: R$0,00")
        self.label_diarias.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_diarias.setFont(font_title)
        totals_layout.addWidget(self.label_diarias)

        self.label_despesas = QLabel("Despesas: R$0,00")
        self.label_despesas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_despesas.setFont(font_title)
        totals_layout.addWidget(self.label_despesas)

        self.label_total = QLabel("Total: R$0,00  ")
        self.label_total.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.label_total.setFont(font_title)
        totals_layout.addWidget(self.label_total)

        group_layout.addLayout(totals_layout)
        main_layout.addWidget(group_box)

        # Instruções
        self.label_atalhos = QLabel("[ + ] aumenta [ - ] diminui [Del] Exclui [F5] Encerra")
        self.label_atalhos.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_atalhos)

        self.carregar_despesas()

    def atualizar_sugestoes(self, texto):
        self.lista_sugestoes.clear()

        if not texto.strip():
            self.lista_sugestoes.setVisible(False)
            return

        resultados = buscar_produto_por_nome(texto)

        if not resultados:
            self.lista_sugestoes.setVisible(False)
            return

        for produto in resultados:
            item = QListWidgetItem(f"{produto.descricao} - R${produto.valor:.2f}")
            item.setData(Qt.ItemDataRole.UserRole, produto)
            self.lista_sugestoes.addItem(item)

        self.lista_sugestoes.setVisible(True)

    def selecionar_sugestao(self, item):
        produto = item.data(Qt.ItemDataRole.UserRole)
        self.produto_selecionado = produto
        self.input_descricao.setText(produto.descricao)
        self.lista_sugestoes.setVisible(False)


    def adicionar_despesa(self):
        produto = self.produto_selecionado
        if not produto:
            return

        quantidade = self.input_quantidade.value()
        valor_unitario = produto.valor
        total = quantidade * valor_unitario
        data = datetime.now()

        # Persistência no banco
        create_despesa(
            id_hospedagem=self.hospedagem.id,
            id_produto=produto.id,
            quantidade=quantidade
        )

        # Adiciona na tabela visual
        row = self.tabela.rowCount()
        self.tabela.insertRow(row)
        self.tabela.setItem(row, 0, QTableWidgetItem(data.strftime("%d/%m/%Y")))
        self.tabela.setItem(row, 1, QTableWidgetItem(produto.descricao))
        self.tabela.setItem(row, 2, QTableWidgetItem(str(quantidade)))
        self.tabela.setItem(row, 3, QTableWidgetItem(f"R${valor_unitario:.2f}"))
        self.tabela.setItem(row, 4, QTableWidgetItem(f"R${total:.2f}"))

        # Limpa os campos
        self.input_descricao.clear()
        self.input_quantidade.setValue(1)
        self.produto_selecionado = None
        self.lista_sugestoes.setVisible(False)

        self.atualizar_totais()

    def atualizar_totais(self):
        total_despesas = 0.0
        for row in range(self.tabela.rowCount()):
            item_total = self.tabela.item(row, 4)
            if item_total:
                valor = float(item_total.text().replace("R$", "").replace(",", "."))
                total_despesas += valor

        self.label_despesas.setText(f"Despesas: R${total_despesas:.2f}")
        # Suponha que você tenha um valor de diária armazenado:
        valor_diarias = 0.0  # você pode definir isso em outra parte, como um atributo
        self.label_diarias.setText(f"  Diárias: R${valor_diarias:.2f}")
        self.label_total.setText(f"Total: R${valor_diarias + total_despesas:.2f}  ")

    def carregar_despesas(self):
        self.tabela.setRowCount(0)  # Limpa a tabela
        despesas = buscar_despesas_por_id_hospedagem(self.hospedagem.id)

        for despesa in despesas:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)

            data_formatada = despesa.data.strftime("%d/%m/%Y")
            descricao = despesa.produto.descricao  # A relação 'produto' precisa estar definida no modelo
            valor_unitario = despesa.valor / despesa.quantidade
            total = despesa.valor

            self.tabela.setItem(row, 0, QTableWidgetItem(data_formatada))
            self.tabela.setItem(row, 1, QTableWidgetItem(descricao))
            self.tabela.setItem(row, 2, QTableWidgetItem(str(despesa.quantidade)))
            self.tabela.setItem(row, 3, QTableWidgetItem(f"R${valor_unitario:.2f}"))
            self.tabela.setItem(row, 4, QTableWidgetItem(f"R${total:.2f}"))

        self.atualizar_totais()
