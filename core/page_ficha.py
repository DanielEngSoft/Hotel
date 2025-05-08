from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Qt
from datetime import datetime

from views.PagesMenu.PagesHospedagem.page_ficha import Ui_page_ficha_hospedagem

from operations.Ui.produtos_operations import buscar_produto_por_nome
from operations.Ui.despesas_operations import create_despesa


class Core_page_ficha(QWidget):
    def __init__(self, hospedagem):
        super().__init__()
        self.ui= Ui_page_ficha_hospedagem()
        self.ui.setupUi(self.ui)
        
        self.hospedagem = hospedagem
        self.setWindowTitle(f"Hospedagem de {self.hospedagem.hospede.nome}")
        self.ui.label_nome.setText(self.ui.hospedagem.hospede.nome)
        self.ui.label_quarto.setText(f"Quarto: {self.hospedagem.quarto.numero}")

        self.ui.btn_adicionar.clicked.connect(self.ui.adicionar_despesa)
        self.ui.input_descricao.textChanged.connect(self.sugerir_produtos)
        self.ui.lista_sugestoes.itemClicked.connect(self.preencher_descricao)

        self.carregar_despesas()

    def carregar_despesas(self):
        self.tabela.setRowCount(0)
        total_despesas = 0

        for despesa in self.hospedagem.despesas:
            data = despesa.data.strftime("%d/%m/%Y")
            descricao = despesa.descricao
            qtd = despesa.quantidade
            valor = despesa.valor
            total = qtd * valor
            total_despesas += total

            row = self.tabela.rowCount()
            self.tabela.insertRow(row)

            self.tabela.setItem(row, 0, self._item(data))
            self.tabela.setItem(row, 1, self._item(descricao))
            self.tabela.setItem(row, 2, self._item(str(qtd), Qt.AlignCenter))
            self.tabela.setItem(row, 3, self._item(f"R$ {valor:.2f}", Qt.AlignRight))
            self.tabela.setItem(row, 4, self._item(f"R$ {total:.2f}", Qt.AlignRight))

        total_diarias = self.hospedagem.total_diarias()
        total_geral = total_diarias + total_despesas

        self.label_diarias.setText(f"  Diárias: R$ {total_diarias:.2f}")
        self.label_despesas.setText(f"Despesas: R$ {total_despesas:.2f}")
        self.label_total.setText(f"Total: R$ {total_geral:.2f}  ")

    def _item(self, texto, align=Qt.AlignLeft):
        from PySide6.QtWidgets import QTableWidgetItem
        item = QTableWidgetItem(texto)
        item.setTextAlignment(align | Qt.AlignVCenter)
        return item

    def adicionar_despesa(self):
        descricao = self.input_descricao.text().strip()
        valor = self.input_valor.get_valor_float()
        quantidade = self.input_quantidade.value()

        if not descricao or valor <= 0 or quantidade <= 0:
            QMessageBox.warning(self, "Dados inválidos", "Preencha todos os campos corretamente.")
            return

        create_despesa(self.hospedagem, descricao, valor, quantidade)
        self.input_descricao.clear()
        self.input_valor.setText("R$ 0,00")
        self.input_quantidade.setValue(1)
        self.lista_sugestoes.clear()
        self.lista_sugestoes.setVisible(False)

        self.carregar_despesas()

    def sugerir_produtos(self, texto):
        self.lista_sugestoes.clear()

        if not texto:
            self.lista_sugestoes.setVisible(False)
            return

        produtos = buscar_produto_por_nome(texto)
        if produtos:
            self.lista_sugestoes.addItems([p.descricao for p in produtos])
            self.lista_sugestoes.setVisible(True)
        else:
            self.lista_sugestoes.setVisible(False)

    def preencher_descricao(self, item):
        self.input_descricao.setText(item.text())
        self.lista_sugestoes.setVisible(False)

#--------------------------------------- page ficha---------------------------------------------
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QFont
# from PySide6.QtWidgets import (
#     QAbstractItemView, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel,
#     QSpacerItem, QSizePolicy, QFrame, QLineEdit, QSpinBox,
#     QPushButton, QTableWidget, QListWidget
# )

# VALOR_ZERO = "R$ 0,00"

# class LineEditMonetario(QLineEdit):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setAlignment(Qt.AlignmentFlag.AlignRight)
#         self.setText(VALOR_ZERO)
#         self.valor_cents = 0
#         self.textEdited.connect(self.formatar_valor_monetario)

#     def focusInEvent(self, event):
#         super().focusInEvent(event)
#         QTimer.singleShot(0, lambda: self.setCursorPosition(len(self.text())))

#     def formatar_valor_monetario(self, _):
#         texto = self.text()
#         apenas_numeros = ''.join(filter(str.isdigit, texto))
#         self.valor_cents = int(apenas_numeros) if apenas_numeros else 0

#         reais = self.valor_cents // 100
#         centavos = self.valor_cents % 100
#         texto_formatado = f"R$ {reais},{centavos:02d}"

#         self.blockSignals(True)
#         self.setText(texto_formatado)
#         self.blockSignals(False)
#         self.setCursorPosition(len(texto_formatado))

#     def get_valor_float(self):
#         return self.valor_cents / 100.0

# class Ui_page_ficha(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setGeometry(100, 100, 800, 600)
#         self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

#         font_title = QFont()
#         font_title.setPointSize(14)
#         font_content = QFont()
#         font_content.setPointSize(10)

#         self.main_layout = QVBoxLayout(self)

#         self.group_box = QGroupBox("Ficha da Hospedagem")
#         self.group_box.setFont(font_content)
#         self.group_layout = QVBoxLayout(self.group_box)

#         self.header_layout = QHBoxLayout()
#         self.label_nome = QLabel("Nome do Hóspede")
#         self.label_nome.setFont(font_title)
#         self.header_layout.addWidget(self.label_nome)

#         self.header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

#         self.label_quarto = QLabel("Quarto: ?")
#         self.label_quarto.setFont(font_title)
#         self.header_layout.addWidget(self.label_quarto)
#         self.group_layout.addLayout(self.header_layout)

#         self.line = QFrame()
#         self.line.setFrameShape(QFrame.HLine)
#         self.line.setFrameShadow(QFrame.Sunken)
#         self.group_layout.addWidget(self.line)

#         self.input_layout = QHBoxLayout()
#         self.input_descricao = QLineEdit()
#         self.input_descricao.setPlaceholderText("Descrição do produto")
#         self.input_layout.addWidget(self.input_descricao)

#         self.input_valor = LineEditMonetario()
#         self.input_valor.setMaximumWidth(100)
#         self.input_layout.addWidget(self.input_valor)

#         self.input_quantidade = QSpinBox()
#         self.input_quantidade.setMinimum(1)
#         self.input_layout.addWidget(self.input_quantidade)

#         self.btn_adicionar = QPushButton("Adicionar")
#         self.input_layout.addWidget(self.btn_adicionar)
#         self.group_layout.addLayout(self.input_layout)

#         self.lista_sugestoes = QListWidget()
#         self.lista_sugestoes.setMaximumHeight(100)
#         self.lista_sugestoes.setVisible(False)
#         self.group_layout.addWidget(self.lista_sugestoes)

#         self.tabela = QTableWidget(0, 5)
#         self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
#         self.tabela.setAlternatingRowColors(True)
#         self.tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
#         self.tabela.setHorizontalHeaderLabels(["Data", "Descrição", "QTD", "Valor", "TOTAL"])

#         header = self.tabela.horizontalHeader()
#         header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
#         header.setSectionResizeMode(1, QHeaderView.Stretch)
#         header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
#         header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
#         header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
#         self.group_layout.addWidget(self.tabela)

#         self.totals_layout = QHBoxLayout()
#         self.label_diarias = QLabel("  Diárias: R$0,00")
#         self.label_diarias.setAlignment(Qt.AlignmentFlag.AlignLeft)
#         self.label_diarias.setFont(font_title)
#         self.totals_layout.addWidget(self.label_diarias)

#         self.label_despesas = QLabel("Despesas: R$0,00")
#         self.label_despesas.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.label_despesas.setFont(font_title)
#         self.totals_layout.addWidget(self.label_despesas)

#         self.label_total = QLabel("Total: R$0,00  ")
#         self.label_total.setAlignment(Qt.AlignmentFlag.AlignRight)
#         self.label_total.setFont(font_title)
#         self.totals_layout.addWidget(self.label_total)

#         self.group_layout.addLayout(self.totals_layout)
#         self.main_layout.addWidget(self.group_box)

#         self.label_atalhos = QLabel("[ + ] aumenta [ - ] diminui [Del] Exclui [F5] Encerra")
#         self.label_atalhos.setAlignment(Qt.AlignCenter)
#         self.main_layout.addWidget(self.label_atalhos)
#------------------------------------------ page listar-------------------------------------------
# from core.page_ficha import Core_page_ficha
    # def abrir_janela_hospedagem(self, hospedagem):
    #     """Abre a janela de ficha da hospedagem"""
    #     try:
    #         janela = Core_page_ficha(hospedagem)
    #         self.janelas_abertas.append(janela)
    #         janela.setWindowModality(Qt.ApplicationModal) # Para bloquear a janela principal
    #         janela.raise_()
    #         janela.activateWindow()
    #         janela.show()
    #     except Exception as e:
    #         print("Erro ao abrir ficha:", e)