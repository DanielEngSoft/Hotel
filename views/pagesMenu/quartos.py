# Importações do PySide6 para criação de interfaces gráficas
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QHBoxLayout, QPushButton,
    QSpacerItem, QSizePolicy, QStackedWidget
)

# Importa as interfaces das páginas de quartos
from views.PagesMenu.PagesQuartos.page_cadastrar import Ui_page_cadastrar
from views.PagesMenu.PagesQuartos.page_listar import Ui_page_listar


class PageQuartos(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # Inicializa a superclasse QWidget
        self.setupUi()  # Chama o método para configurar a interface

    def setupUi(self):
        self.setObjectName("PageQuartos")  # Nome do objeto (útil para QSS ou debug)

        # ========== LAYOUT PRINCIPAL ==========
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # ========== MENU SUPERIOR ==========
        self.menu_superior = QFrame(self)
        self.menu_superior.setMinimumSize(QSize(600, 0))
        self.menu_superior.setMaximumSize(QSize(1800, 1200))
        self.menu_superior.setFrameShape(QFrame.Shape.StyledPanel)

        # Layout horizontal do menu
        self.horizontalLayout = QHBoxLayout(self.menu_superior)
        self.horizontalLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botão "Listar"
        self.button_listar = QPushButton("Listar", self.menu_superior)
        self._estilizar_botao(self.button_listar)
        self.horizontalLayout.addWidget(self.button_listar)

        # Botão "Ocupados"
        self.button_ocupados = QPushButton("Ocupados", self.menu_superior)
        self._estilizar_botao(self.button_ocupados)
        self.horizontalLayout.addWidget(self.button_ocupados)

        # Botão "Cadastrar"
        self.button_cadastrar = QPushButton("Cadastrar", self.menu_superior)
        self._estilizar_botao(self.button_cadastrar)
        self.horizontalLayout.addWidget(self.button_cadastrar)

        # Adiciona o menu superior ao layout principal
        self.layout_principal.addWidget(self.menu_superior)

        # ========== ÁREA DAS PÁGINAS ==========
        self.pages = QStackedWidget(self)

        # Página "Listar"
        self.page_listar = Ui_page_listar()
        self.pages.addWidget(self.page_listar)

        # Página "Ocupados" (placeholder)
        self.page_ocupados = QWidget()
        self.page_ocupados.setLayout(QVBoxLayout())
        self.page_ocupados.layout().addWidget(QPushButton("Quartos Ocupados"))
        self.pages.addWidget(self.page_ocupados)

        # Página "Cadastrar"
        self.page_cadastrar = Ui_page_cadastrar()
        self.pages.addWidget(self.page_cadastrar)

        # Adiciona o QStackedWidget ao layout principal
        self.layout_principal.addWidget(self.pages)

        # ========== CONEXÕES DOS BOTÕES ==========
        self.button_listar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_listar))
        self.button_ocupados.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_ocupados))
        self.button_cadastrar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_cadastrar))

        # Define a página inicial
        self.pages.setCurrentWidget(self.page_listar)

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
