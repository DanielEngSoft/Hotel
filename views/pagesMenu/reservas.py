# ========== IMPORTAÇÕES ==========

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QHBoxLayout, QPushButton,
    QSpacerItem, QSizePolicy, QStackedWidget
)


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

        # ========== MENU SUPERIOR ==========
        self.menu_superior = QFrame(self)
        self.menu_superior.setMinimumSize(QSize(600, 0))
        self.menu_superior.setMaximumSize(QSize(1800, 1200))
        self.menu_superior.setFrameShape(QFrame.Shape.StyledPanel)

        self.layout_menu = QHBoxLayout(self.menu_superior)
        self.layout_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botão "Abrir"
        self.button_abrir = QPushButton("Abrir", self.menu_superior)
        self._estilizar_botao(self.button_abrir)
        self.layout_menu.addWidget(self.button_abrir)

        # Botão "Listar"
        self.button_listar = QPushButton("Listar", self.menu_superior)
        self._estilizar_botao(self.button_listar)
        self.layout_menu.addWidget(self.button_listar)

        # Botão "Fechar"
        self.button_fechar = QPushButton("Fechar", self.menu_superior)
        self._estilizar_botao(self.button_fechar)
        self.layout_menu.addWidget(self.button_fechar)

        # Adiciona o menu ao layout principal
        self.layout_principal.addWidget(self.menu_superior)

        # ========== ÁREA DAS PÁGINAS ==========
        self.pages = QStackedWidget(self)

        self.page_abrir = QWidget()
        self.pages.addWidget(self.page_abrir)

        self.page_listar = QWidget()
        self.pages.addWidget(self.page_listar)

        self.page_fechar = QWidget()
        self.pages.addWidget(self.page_fechar)

        self.layout_principal.addWidget(self.pages)

        # ========== CONEXÕES DOS BOTÕES ==========
        self.button_abrir.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_abrir))
        self.button_listar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_listar))
        self.button_fechar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_fechar))

        # Página inicial
        self.pages.setCurrentWidget(self.page_abrir)

    # ========== MÉTODO AUXILIAR ==========
    def _estilizar_botao(self, botao):
        """
        Aplica estilo padrão aos botões:
        - Define tamanho mínimo e máximo
        - Altera o cursor para o formato de mão ao passar por cima
        """
        botao.setMinimumSize(QSize(100, 50))
        botao.setMaximumSize(QSize(200, 70))
        botao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
