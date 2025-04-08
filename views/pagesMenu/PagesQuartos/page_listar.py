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
        # Janelas abertas para evitar múltiplas instâncias
        self.janelas_abertas = []

        # Criando e configurando layout principal --------------------------------------------------------------|
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20) # Ajusta as margens
        layout_principal.setSpacing(15) # Ajusta o espaçamento entre os widgets

        # Label de título --------------------------------------------------------------------------------
        label_titulo = QLabel("Quartos")
        label_titulo.setAlignment(Qt.AlignCenter) # Centraliza o texto
        label_titulo.setFont(QFont("Segoe UI", 14, QFont.Bold)) # Define a fonte e o tamanho do título

        # Adiciona o título ao layout principal
        layout_principal.addWidget(label_titulo)

        # Scroll area onde os botões dos quartos serão exibidos -------------------------------------------|
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True) # Permite que o conteúdo do scroll redimensione com a janela

        # Criando a área de conteúdo do scroll ------------------------------------------------------------|
        scroll_content = QWidget()
        grid = QGridLayout(scroll_content) # Layout em grade para organizar os botões dos quartos
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)

        quartos = listar_quartos() # Obtém a lista de quartos disponíveis
        hospedagens = listar_hospedagens() # Obtém a lista de hospedagens ativas

        # Cria um dicionário para acesso rápido das hospedagens por id_quarto
        hospedagens_por_quarto = {h.id_quarto: h for h in hospedagens}

        # Cria os botões para cada quarto e adiciona ao layout em grade ----------------------------------|
        for i, quarto in enumerate(quartos):
            btn = QPushButton(f"{quarto.numero}\n{quarto.tipo}")
            btn.setMinimumSize(QSize(120, 60))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setFont(QFont("Segoe UI", 10))
            btn.setToolTip("Disponível" if quarto.disponivel else "Ocupado")

            # Linha e coluna para o botão na grade
            row = i // 6
            col = i % 6
            grid.addWidget(btn, row, col)

            # Altera o estilo do botão dependendo da disponibilidade do quarto
            if quarto.disponivel:
                btn.setStyleSheet("background-color: green;")
            else:
                btn.setStyleSheet("background-color: red;")
                # Procura hospedagem ativa relacionada a esse quarto do laço for
                hospedagem_quarto = hospedagens_por_quarto.get(quarto.numero)
                # Se houver uma hospedagem ativa, conecta o botão à função de abrir a ficha
                if hospedagem_quarto:
                    btn.clicked.connect(partial(self.abrir_janela_hospedagem, hospedagem_quarto))

        # Adiciona o layout em grade ao conteúdo do scroll ------------------------------------------|
        scroll_area.setWidget(scroll_content)
        layout_principal.addWidget(scroll_area)

        # Definindo o layout principal --------------------------------------------------------------|
        self.setLayout(layout_principal)

    def abrir_janela_hospedagem(self, hospedagem):
        try:
            janela = JanelaHospedagem(hospedagem)
            self.janelas_abertas.append(janela)
            janela.setWindowModality(Qt.ApplicationModal)
            janela.raise_()
            janela.activateWindow()
            janela.show()
        except Exception as e:
            print("Erro ao abrir ficha:", e)

