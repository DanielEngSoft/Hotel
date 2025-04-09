from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QHBoxLayout,QHeaderView, QLabel,
    QSpacerItem, QSizePolicy, QFrame, QLineEdit, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem
)


class JanelaHospedagem(QWidget):
    def __init__(self, hospedagem, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Hospedagem - Quarto {getattr(hospedagem.quarto, 'numero', 'Desconhecido')}")
        # Centralizando na tela
        screen_geometry = self.screen().geometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.setGeometry(x, y, 800, 600)  # Tamanho inicial da janela centralizado
        self.setMaximumSize(800, 600)  # Tamanho máximo da janela

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        font_title = QFont()
        font_title.setPointSize(14)
        font_content = QFont()
        font_content.setPointSize(10)

        # Layout principal
        main_layout = QVBoxLayout(self)

        # GroupBox
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
        self.input_descricao.setPlaceholderText("Descrição")
        input_layout.addWidget(self.input_descricao)

        self.input_quantidade = QSpinBox()
        self.input_quantidade.setFont(font_content)
        self.input_quantidade.setMinimum(1)
        input_layout.addWidget(self.input_quantidade)

        self.btn_adicionar = QPushButton("Adicionar")
        self.btn_adicionar.setFont(font_content)
        input_layout.addWidget(self.btn_adicionar)

        group_layout.addLayout(input_layout)

        # Tabela de despesas
        self.tabela = QTableWidget(0, 5)
        self.tabela.setHorizontalHeaderLabels(["Data", "Descrição", "QTD", "Valor", "TOTAL"])

        # Redimensionamento das colunas
        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Data
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # Descrição (preenche o espaço)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # QTD
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Valor
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # TOTAL

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
