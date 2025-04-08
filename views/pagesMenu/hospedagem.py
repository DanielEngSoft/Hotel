from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QLabel
)

from views.PagesMenu.PagesHospedagem.page_listar import Ui_page_listar
from views.PagesMenu.PagesHospedagem.page_abrir import Ui_page_abrir


class PageHospedagem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        """Configura toda a interface da página de hospedagem."""

        # Layout vertical principal do widget
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setObjectName("layout_principal")

        # Garante que o menu fique colado no topo, sem espaços extras
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # Primeiro cria as páginas para depois referenciar nos botões
        self.criar_paginas()

        # Depois cria o menu superior com os botões
        self.criar_menu_superior()

        # Define a página padrão como "Listar"
        self.pages.setCurrentWidget(self.page_listar)

    def criar_menu_superior(self):
        """Cria o menu superior com os botões: Abrir, Listar, Fechar."""
        self.menu_superior = QFrame(self)
        self.menu_superior.setObjectName("menu_superior")
        self.menu_superior.setMinimumSize(QSize(600, 0))
        self.menu_superior.setFrameShape(QFrame.StyledPanel)

        self.layout_menu = QHBoxLayout(self.menu_superior)
        self.layout_menu.setObjectName("layout_menu")

        # Espaçador à esquerda
        self.layout_menu.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Botão Abrir
        self.button_abrir = self.criar_botao("Abrir", self.page_abrir)
        self.layout_menu.addWidget(self.button_abrir)

        # Botão Listar
        self.button_listar = self.criar_botao("Listar", self.page_listar)
        self.layout_menu.addWidget(self.button_listar)

        # Botão Fechar
        self.button_fechar = self.criar_botao("Fechar", self.page_fechar)
        self.layout_menu.addWidget(self.button_fechar)

        # Espaçador à direita
        self.layout_menu.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Adiciona o menu ao layout principal (antes das páginas)
        self.layout_principal.insertWidget(0, self.menu_superior) # Adiciona o menu no topo, 0 é o topo

    def criar_botao(self, texto, pagina_destino):
        """Cria um botão de menu com comportamento para trocar de página."""
        botao = QPushButton(texto)
        botao.setObjectName(f"button_{texto.lower()}")
        botao.setMinimumSize(QSize(100, 50))
        botao.setMaximumSize(QSize(200, 70))
        botao.setCursor(QCursor(Qt.PointingHandCursor))
        botao.clicked.connect(lambda: self.pages.setCurrentWidget(pagina_destino))
        return botao

    def criar_paginas(self):
        """Cria as páginas e adiciona ao QStackedWidget."""
        self.pages = QStackedWidget(self)
        self.pages.setObjectName("pages")

        # Página Abrir
        self.page_abrir = Ui_page_abrir()
        self.pages.addWidget(self.page_abrir)

        # Página Listar
        self.page_listar = Ui_page_listar()
        self.pages.addWidget(self.page_listar)

        # Página Fechar (com apenas um título por enquanto)
        self.page_fechar = QWidget()
        self.page_fechar.setObjectName("page_fechar")

        layout_fechar = QVBoxLayout(self.page_fechar)
        label_fechar = QLabel("<h1>Fechar Hospedagem</h1>")
        label_fechar.setObjectName("label_fechar")
        layout_fechar.addWidget(label_fechar)

        self.pages.addWidget(self.page_fechar)

        # Adiciona o QStackedWidget ao layout principal
        self.layout_principal.addWidget(self.pages)
