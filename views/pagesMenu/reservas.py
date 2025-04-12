# ========== IMPORTAÇÕES ==========

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QListWidget, QListWidgetItem, # Adicionado QListWidget, QListWidgetItem
    QStackedWidget, QSizePolicy # Adicionado QSizePolicy
)
from styles.styles import menu_superior_pages

class PageReservas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("PageReservas")

        # ========== LAYOUT PRINCIPAL ==========
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # ========== MENU SUPERIOR (QListWidget) ==========
        self.menu_superior = QFrame(self)
        # Ajustado para altura fixa consistente com o QListWidget
        self.menu_superior.setMinimumSize(QSize(600, 45))
        self.menu_superior.setMaximumSize(QSize(1800, 45))
        self.menu_superior.setFrameShape(QFrame.Shape.StyledPanel)
        # self.menu_superior.setFrameShadow(QFrame.Raised) # Removido ou ajustado conforme necessário

        # Removido layout antigo de botões: self.layout_menu = QHBoxLayout(self.menu_superior)

        # Novo QListWidget para o menu
        self.lista_menu = QListWidget(self.menu_superior)
        self.lista_menu.setFlow(QListWidget.LeftToRight) # Itens fluem da esquerda para a direita
        self.lista_menu.setWrapping(False) # Impede que os itens quebrem linha
        self.lista_menu.setSpacing(10) # Espaçamento entre os itens
        self.lista_menu.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # Sem barra de rolagem horizontal
        self.lista_menu.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # Sem barra de rolagem vertical
        self.lista_menu.setFixedHeight(45) # Altura fixa para a lista
        self.lista_menu.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)) # Cursor de mão
        self.lista_menu.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed) # Expande horizontalmente

        # Aplica o estilo importado (ou o placeholder)
        self.lista_menu.setStyleSheet(menu_superior_pages())

        # Adiciona os itens (substituindo os botões)
        self.lista_menu.addItem("Abrir")
        self.lista_menu.addItem("Listar")
        self.lista_menu.addItem("Fechar")

        # Removidos botões antigos: self.button_abrir, self.button_listar, self.button_fechar
        # Removida função auxiliar: _estilizar_botao

        # Adiciona o menu (frame) ao layout principal
        self.layout_principal.addWidget(self.menu_superior)

        # Layout para organizar o QListWidget dentro do QFrame menu_superior
        menu_layout = QVBoxLayout(self.menu_superior) # Usar QVBoxLayout para que o ListWidget preencha o frame
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.addWidget(self.lista_menu) # Adiciona a lista ao layout do frame

        # ========== ÁREA DAS PÁGINAS ==========
        self.pages = QStackedWidget(self)

        # As páginas continuam as mesmas
        self.page_abrir = QWidget()
        # Adicione aqui os widgets da página "Abrir"
        self.pages.addWidget(self.page_abrir)

        self.page_listar = QWidget()
        # Adicione aqui os widgets da página "Listar"
        self.pages.addWidget(self.page_listar)

        self.page_fechar = QWidget()
        # Adicione aqui os widgets da página "Fechar"
        self.pages.addWidget(self.page_fechar)

        self.layout_principal.addWidget(self.pages)

        # ========== CONEXÃO ENTRE ITENS E PÁGINAS ==========
        # Removidas conexões antigas dos botões
        # Nova conexão: mudar a página no QStackedWidget quando o item selecionado na lista mudar
        self.lista_menu.currentRowChanged.connect(self.pages.setCurrentIndex)

        # Seleciona a primeira página por padrão ("Abrir")
        # Removido: self.pages.setCurrentWidget(self.page_abrir)
        self.lista_menu.setCurrentRow(0) # Seleciona o primeiro item ("Abrir") na lista
