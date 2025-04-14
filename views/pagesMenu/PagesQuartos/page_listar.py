# Importações do PySide6 para criação de interfaces gráficas
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel,
    QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont

# Importações auxiliares
from functools import partial

# Importações das operações para buscar dados
from operations.Ui.quartos_operations import listar_quartos
from operations.Ui.hospedagem_operations import hospedagens_ativas

# Importação da janela de ficha de hospedagem
from views.PagesMenu.PagesHospedagem.page_hospedagem import Ui_page_hospedagem
from operations.Ui.quartos_operations import qtd_disponiveis, qtd_ocupados


class Ui_page_listar(QWidget):
    COR_DISPONIVEL = "#05452f"
    COR_OCUPADO = "#A52A2A"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.janelas_abertas = []

        # ========== LAYOUT PRINCIPAL ==========
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(15)

        self.disponiveis = qtd_disponiveis()
        self.ocupados = qtd_ocupados()

        # ========== TÍTULO DA PÁGINA ==========
        label_titulo = QLabel(f"🟩 Disponíveis[{self.disponiveis}] | 🟥 Ocupados[{self.ocupados}]")
        label_titulo.setAlignment(Qt.AlignCenter)
        label_titulo.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.layout_principal.addWidget(label_titulo)

        # ========== ÁREA DE SCROLL ==========
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.grid = QGridLayout(self.scroll_content)
        self.grid.setContentsMargins(10, 10, 10, 10)
        self.grid.setHorizontalSpacing(10)
        self.grid.setVerticalSpacing(10)

        self.scroll_area.setWidget(self.scroll_content)
        self.layout_principal.addWidget(self.scroll_area)

        self.setLayout(self.layout_principal)
        self.atualizar_dados()

    def showEvent(self, event):
        super().showEvent(event)
        self.atualizar_dados()

    def atualizar_dados(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        quartos = listar_quartos()
        hospedagens = hospedagens_ativas()
        hospedagens_por_quarto = {h.id_quarto: h for h in hospedagens}

        for i, quarto in enumerate(quartos):
            btn = QPushButton(f"{quarto.numero}\n{quarto.tipo}")
            btn.setMaximumHeight(80)
            btn.setMinimumSize(QSize(120, 60))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setFont(QFont("Segoe UI", 10))

            row = i // 6
            col = i % 6
            self.grid.addWidget(btn, row, col)

            if quarto.disponivel:
                btn.setStyleSheet(f"background-color: {self.COR_DISPONIVEL};")
            else:
                btn.setStyleSheet(f"background-color: {self.COR_OCUPADO};")
                hospedagem_quarto = hospedagens_por_quarto.get(quarto.numero)
                if hospedagem_quarto:
                    btn.clicked.connect(partial(self.abrir_janela_hospedagem, hospedagem_quarto))

    def abrir_janela_hospedagem(self, hospedagem):
        for janela in self.janelas_abertas:
            if janela.hospedagem.id == hospedagem.id:
                janela.raise_()
                janela.activateWindow()
                return

        try:
            janela = Ui_page_hospedagem(hospedagem)
            self.janelas_abertas.append(janela)
            janela.setAttribute(Qt.WA_DeleteOnClose)
            janela.destroyed.connect(lambda: self.janelas_abertas.remove(janela))
            janela.setWindowModality(Qt.ApplicationModal)
            janela.raise_()
            janela.activateWindow()
            janela.show()
        except Exception as e:
            print("Erro ao abrir ficha:", e)
