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
from operations.Ui.hospedagem_operations import listar_hospedagens

# Importação da janela de ficha de hospedagem
from views.PagesMenu.PagesHospedagem.page_ficha import JanelaHospedagem


class Ui_page_listar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # Inicializa a superclasse QWidget
        self.janelas_abertas = []  # Armazena janelas de hospedagens já abertas

        # ========== LAYOUT PRINCIPAL ==========
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(15)

        # ========== TÍTULO DA PÁGINA ==========
        label_titulo = QLabel("Quartos")
        label_titulo.setAlignment(Qt.AlignCenter)
        label_titulo.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.layout_principal.addWidget(label_titulo)

        # ========== ÁREA DE SCROLL ==========
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Conteúdo dentro da área de scroll
        self.scroll_content = QWidget()
        self.grid = QGridLayout(self.scroll_content)
        self.grid.setContentsMargins(10, 10, 10, 10)
        self.grid.setHorizontalSpacing(10)
        self.grid.setVerticalSpacing(10)

        # Adiciona o conteúdo ao scroll e o scroll ao layout principal
        self.scroll_area.setWidget(self.scroll_content)
        self.layout_principal.addWidget(self.scroll_area)

        # Define o layout principal como o layout do widget
        self.setLayout(self.layout_principal)

        # Chama o método para preencher os dados inicialmente
        self.atualizar_dados()

    def showEvent(self, event):
        """
        Método chamado automaticamente quando a página é exibida.
        Garante que os dados estejam atualizados sempre que a aba for mostrada.
        """
        super().showEvent(event)
        self.atualizar_dados()

    def atualizar_dados(self):
        """
        Atualiza o grid de botões com os dados dos quartos.
        Mostra se o quarto está ocupado ou disponível,
        e conecta o clique dos quartos ocupados à janela de hospedagem.
        """
        # Limpa os widgets existentes no grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Busca os dados de quartos e hospedagens
        quartos = listar_quartos()
        hospedagens = listar_hospedagens()
        hospedagens_por_quarto = {h.id_quarto: h for h in hospedagens}

        # Cria um botão para cada quarto
        for i, quarto in enumerate(quartos):
            btn = QPushButton(f"{quarto.numero}\n{quarto.tipo}")
            btn.setMinimumSize(QSize(120, 60))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setFont(QFont("Segoe UI", 10))
            btn.setToolTip("Disponível" if quarto.disponivel else "Ocupado")

            # Define a posição no grid (6 por linha)
            row = i // 6
            col = i % 6
            self.grid.addWidget(btn, row, col)

            # Aplica o estilo conforme disponibilidade
            if quarto.disponivel:
                btn.setStyleSheet("background-color: #2c3e50;")
            else:
                btn.setStyleSheet("background-color: #A52A2A;")
                # Conecta o botão à janela da hospedagem correspondente
                hospedagem_quarto = hospedagens_por_quarto.get(quarto.numero)
                if hospedagem_quarto:
                    btn.clicked.connect(partial(self.abrir_janela_hospedagem, hospedagem_quarto))

    def abrir_janela_hospedagem(self, hospedagem):
        """
        Abre a janela de detalhes da hospedagem do quarto selecionado.
        Janela é modal e fica em destaque.
        """
        try:
            janela = JanelaHospedagem(hospedagem)
            self.janelas_abertas.append(janela)
            janela.setWindowModality(Qt.ApplicationModal)
            janela.raise_()
            janela.activateWindow()
            janela.show()
        except Exception as e:
            print("Erro ao abrir ficha:", e)
