from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QListWidget, QListWidgetItem,
    QStackedWidget, QSizePolicy, QLabel
)

from views.PagesMenu.PagesHospedagem.page_listar import Ui_page_listar
from views.PagesMenu.PagesHospedagem.page_abrir import Ui_page_abrir
from styles.styles import menu_superior_pages


class PageHospedagem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("PageHospedagem")

        # ========== LAYOUT PRINCIPAL ==========
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # ========== MENU SUPERIOR (QListWidget) ==========
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

        # Adiciona os itens do menu
        self.lista_menu.addItem("Listar")
        self.lista_menu.addItem("Abrir")

        # Adiciona o menu ao layout
        self.layout_principal.addWidget(self.menu_superior)
        menu_layout = QVBoxLayout(self.menu_superior)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.addWidget(self.lista_menu)

        # ========== ÁREA DAS PÁGINAS ==========
        self.pages = QStackedWidget(self)

        self.page_listar = Ui_page_listar()
        self.pages.addWidget(self.page_listar)

        self.page_abrir = Ui_page_abrir()
        self.pages.addWidget(self.page_abrir)

        self.layout_principal.addWidget(self.pages)

        # ========== CONEXÃO ENTRE ITENS E PÁGINAS ==========
        self.lista_menu.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.lista_menu.setCurrentRow(0)
