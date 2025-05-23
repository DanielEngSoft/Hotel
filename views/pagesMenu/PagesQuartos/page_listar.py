# Importações do PySide6 para criação de interfaces gráficas
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel,
    QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QFont

# Importações auxiliares
from functools import partial

# Importações das operações para buscar dados
from operations.Ui.quartos_operations import listar_quartos
from operations.Ui.hospedagem_operations import hospedagens_ativas

# Importação da janela de ficha de hospedagem
from views.PagesMenu.PagesHospedagem.page_hospedagem import Ui_page_hospedagem
from operations.Ui.quartos_operations import qtd_disponiveis, qtd_ocupados
from styles.styles import btn_quarto_livre, btn_quarto_ocupado


class Ui_page_listar_quarto(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.janelas_abertas = []
        # self.page_listar_instance = None # Removido se não usado

        # ========== LAYOUT PRINCIPAL ==========
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(15)

        # ========== TÍTULO DA PÁGINA ==========
        self.label_titulo = QLabel()
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.label_titulo.setMaximumHeight(40)
        self.layout_principal.addWidget(self.label_titulo)

        # ========== ÁREA DE SCROLL ==========
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True) # Muito importante!
        
        self.grid = QGridLayout(self.scroll_area) # Adiciona o grid ao scroll_content
        
        self.layout_principal.addWidget(self.scroll_area)
        # self.setLayout(self.layout_principal) # Definido no final do __init__ ou não necessário se já é o layout do self

        self.atualizar_dados() # Chamada inicial

        # Timer para atualizar automaticamente a cada 2 segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_dados)
        self.timer.start(2000)

        # Certifique-se que o layout principal é definido para o QWidget
        self.setLayout(self.layout_principal)


    def showEvent(self, event):
        super().showEvent(event)
        self.atualizar_dados() # Atualiza os dados quando a página é mostrada

    def atualizar_dados(self):
        self.disponiveis = qtd_disponiveis()
        self.ocupados = qtd_ocupados()
        self.label_titulo.setText(f"🟩 Disponíveis[{self.disponiveis}] | 🟥 Ocupados[{self.ocupados}]")

        quartos = listar_quartos()
        hospedagens = hospedagens_ativas()
        hospedagens_por_quarto = {h.id_quarto: h for h in hospedagens}

        # 1. Limpar todos os widgets do grid antes de adicionar os novos/atualizados
        while self.grid.count():
            item = self.grid.takeAt(0) # Pega o item na primeira posição
            widget = item.widget()
            if widget is not None:
                widget.deleteLater() # Marca o widget para deleção segura

        # 2. Recriar e adicionar todos os botões ao grid
        for i, quarto in enumerate(quartos):
            btn = QPushButton(f"{quarto.numero}\n{quarto.tipo}")
            btn.setMinimumSize(QSize(120, 100))
            btn.setFont(QFont("Segoe UI", 10))

            if quarto.disponivel:
                btn.setStyleSheet(btn_quarto_livre()) # Adicionado color para melhor leitura
                # Depois adicionar uma ação para quartos disponíveis, se necessário

            else:
                btn.setStyleSheet(btn_quarto_ocupado()) # Adicionado color
                hospedagem_quarto = hospedagens_por_quarto.get(quarto.numero) # Assumindo que quarto.numero é o id_quarto
                if hospedagem_quarto:
                    btn.clicked.connect(partial(self.abrir_janela_hospedagem, hospedagem_quarto))
            
            self.grid.addWidget(btn, i // 6, i % 6) # Adiciona o botão ao grid

        self.scroll_area.updateGeometry() # Atualiza a geometria do scroll_area

    def abrir_janela_hospedagem(self, hospedagem):
        try:
            janela = Ui_page_hospedagem(hospedagem) # Passa o objeto hospedagem
            janela.setAttribute(Qt.WA_DeleteOnClose) # Garante que a janela seja deletada ao fechar
            
            # Adiciona à lista ANTES de conectar ao destroyed, para evitar problemas se a janela fechar rapidamente
            self.janelas_abertas.append(janela)
            
            janela.setWindowModality(Qt.ApplicationModal) # Ou NonModal, dependendo do comportamento desejado
            janela.show()
            janela.raise_() 
            janela.activateWindow()

            # Conecta ao destroyed para remover a janela da lista quando fechar
            janela.destroyed.connect(lambda: self.remover_janela_da_lista(janela))

        except Exception as e:
            print(f"Erro ao abrir ficha de hospedagem: {e}")

    def remover_janela_da_lista(self, janela_destruida):
        if janela_destruida in self.janelas_abertas:
            self.janelas_abertas.remove(janela_destruida)