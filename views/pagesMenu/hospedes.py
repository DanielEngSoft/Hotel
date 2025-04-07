from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QLabel
)

from views.PagesMenu.PagesHospedes.page_cadastrar import Ui_page_cadastrar


class PageHospedes(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")

        self.layout_principal = QVBoxLayout(Form)
        self.layout_principal.setObjectName(u"layout_principal")

        # MENU SUPERIOR
        self.menu_superior_page_hospedagem = QFrame(Form)
        self.menu_superior_page_hospedagem.setMinimumSize(QSize(600, 0))
        self.menu_superior_page_hospedagem.setMaximumSize(QSize(1800, 1200))
        self.menu_superior_page_hospedagem.setFrameShape(QFrame.Shape.StyledPanel)

        self.horizontalLayout = QHBoxLayout(self.menu_superior_page_hospedagem)

        self.horizontalLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.button_cadastrar = QPushButton("Cadastrar", self.menu_superior_page_hospedagem)
        self.button_cadastrar.setMinimumSize(QSize(100, 50))
        self.button_cadastrar.setMaximumSize(QSize(200, 70))
        self.button_cadastrar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.horizontalLayout.addWidget(self.button_cadastrar)

        self.button_listar = QPushButton("Listar", self.menu_superior_page_hospedagem)
        self.button_listar.setMinimumSize(QSize(100, 50))
        self.button_listar.setMaximumSize(QSize(200, 70))
        self.button_listar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.horizontalLayout.addWidget(self.button_listar)

        self.button_alterar = QPushButton("Alterar", self.menu_superior_page_hospedagem)
        self.button_alterar.setMinimumSize(QSize(100, 50))
        self.button_alterar.setMaximumSize(QSize(200, 70))
        self.button_alterar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.horizontalLayout.addWidget(self.button_alterar)

        self.horizontalLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.layout_principal.addWidget(self.menu_superior_page_hospedagem)

        # CONTEÚDO COM AS PÁGINAS
        self.pages = QStackedWidget(Form)

        self.page_cadastrar = Ui_page_cadastrar()
        self.pages.addWidget(self.page_cadastrar)

        # Placeholders para as outras páginas
        self.page_listar = QWidget()
        self.page_listar.setObjectName("page_listar")
        self.page_listar.setLayout(QVBoxLayout())
        self.page_listar.layout().addWidget(QLabel("Página Listar"))

        self.alterar = QWidget()
        self.alterar.setObjectName("alterar")
        self.alterar.setLayout(QVBoxLayout())
        self.alterar.layout().addWidget(QLabel("Página Alterar"))

        self.pages.addWidget(self.page_listar)
        self.pages.addWidget(self.alterar)

        self.layout_principal.addWidget(self.pages)

        # Conectar os botões com as páginas
        self.button_cadastrar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_cadastrar))
        self.button_listar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_listar))
        self.button_alterar.clicked.connect(lambda: self.pages.setCurrentWidget(self.alterar))
