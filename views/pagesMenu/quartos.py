from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QListWidget,
    QStackedWidget, QSizePolicy, QPushButton, QVBoxLayout
)

from views.PagesMenu.PagesQuartos.page_cadastrar import Ui_page_cadastrar
from views.PagesMenu.PagesQuartos.page_listar import Ui_page_listar
from styles.styles import menu_superior_pages


class PageQuartos(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("PageQuartos")

        # ========== LAYOUT PRINCIPAL ==========
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # ========== MENU SUPERIOR ==========
        self.menu_superior = QFrame(self)
        self.menu_superior.setMinimumSize(QSize(600, 45))
        self.menu_superior.setMaximumSize(QSize(1800, 45))
        self.menu_superior.setFrameShape(QFrame.Shape.StyledPanel)

        self.lista_menu = QListWidget(self.menu_superior)
        self.lista_menu.setFlow(QListWidget.LeftToRight)
        self.lista_menu.setWrapping(False)
        self.lista_menu.setSpacing(10)
        self.lista_menu.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.lista_menu.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.lista_menu.setFixedHeight(45)
        self.lista_menu.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.lista_menu.setStyleSheet(menu_superior_pages())
        self.lista_menu.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Itens do menu
        self.lista_menu.addItem("Listar")
        self.lista_menu.addItem("Ocupados")
        self.lista_menu.addItem("Cadastrar")

        menu_layout = QVBoxLayout(self.menu_superior)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.addWidget(self.lista_menu)

        self.layout_principal.addWidget(self.menu_superior)

        # ========== ÁREA DAS PÁGINAS ==========
        self.pages = QStackedWidget(self)

        self.page_listar = Ui_page_listar()
        self.pages.addWidget(self.page_listar)

        self.page_ocupados = QWidget()
        layout_ocupados = QVBoxLayout(self.page_ocupados)
        layout_ocupados.addWidget(QPushButton("Quartos Ocupados"))  # Placeholder
        self.pages.addWidget(self.page_ocupados)

        self.page_cadastrar = Ui_page_cadastrar()
        self.pages.addWidget(self.page_cadastrar)

        self.layout_principal.addWidget(self.pages)

        # ========== CONEXÕES ==========
        self.lista_menu.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.lista_menu.setCurrentRow(0)  # Página inicial
