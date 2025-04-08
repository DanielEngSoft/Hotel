from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel,
    QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from functools import partial

from operations.Ui.quartos_operations import listar_quartos
from operations.Ui.hospedagem_operations import listar_hospedagens
from views.PagesMenu.PagesHospedagem.ficha import JanelaHospedagem


class Ui_page_listar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.janelas_abertas = []

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)

        titulo = QLabel("Quartos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout_principal.addWidget(titulo)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        grid = QGridLayout(scroll_content)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        quartos = listar_quartos()
        hospedagens = listar_hospedagens()

        # Cria um dicionário para acesso rápido das hospedagens por id_quarto
        hospedagens_por_quarto = {h.id_quarto: h for h in hospedagens}

        for i, quarto in enumerate(quartos):
            btn = QPushButton(f"{quarto.numero}\n{quarto.tipo}")
            btn.setMinimumSize(QSize(120, 60))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setFont(QFont("Segoe UI", 10))
            btn.setToolTip("Disponível" if quarto.disponivel else "Ocupado")

            row = i // 6
            col = i % 6
            grid.addWidget(btn, row, col)

            if quarto.disponivel:
                btn.setStyleSheet("background-color: green;")
            else:
                btn.setStyleSheet("background-color: red;")

                # Procura hospedagem ativa relacionada a esse quarto
                hospedagem_quarto = hospedagens_por_quarto.get(quarto.numero)
                if hospedagem_quarto:
                    btn.clicked.connect(partial(self.abrir_janela_hospedagem, hospedagem_quarto))


        scroll_area.setWidget(scroll_content)
        layout_principal.addWidget(scroll_area)

        self.setLayout(layout_principal)

    def abrir_janela_hospedagem(self, hospedagem):
        try:
            print(f"Abrindo ficha para hospedagem: {hospedagem.id}")
            janela = JanelaHospedagem(hospedagem)
            self.janelas_abertas.append(janela)
            janela.setWindowModality(Qt.ApplicationModal)
            janela.raise_()
            janela.activateWindow()
            janela.show()
        except Exception as e:
            print("Erro ao abrir ficha:", e)

