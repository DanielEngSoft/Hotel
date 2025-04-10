# Importações do PySide6 para criação de interfaces gráficas
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QHBoxLayout, QPushButton,
    QStackedWidget, QLabel
)

# Importações das páginas específicas de hospedagem
from views.PagesMenu.PagesHospedagem.page_listar import Ui_page_listar
from views.PagesMenu.PagesHospedagem.page_abrir import Ui_page_abrir


class PageHospedagem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # Inicializa a superclasse QWidget
        self.setupUi()  # Chama o método para configurar a interface

    def setupUi(self):
        self.setObjectName("PageHospedagem")  # Define o nome do objeto (opcional, útil para QSS ou debug)

        # Cria o layout principal da página (vertical)
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # ========== ÁREA DAS PÁGINAS ==========
        # Cria o QStackedWidget que vai conter as páginas
        self.pages = QStackedWidget(self)
        self.pages.setObjectName("pages")

        # Cria a página "Abrir" (importada de outro módulo)
        self.page_abrir = Ui_page_abrir()
        self.pages.addWidget(self.page_abrir)

        # Cria a página "Listar" (importada de outro módulo)
        self.page_listar = Ui_page_listar()
        self.pages.addWidget(self.page_listar)

        # Cria a página "Fechar" (temporária com QLabel)
        self.page_fechar = QWidget()
        self.page_fechar.setObjectName("page_fechar")
        layout_fechar = QVBoxLayout(self.page_fechar)
        layout_fechar.addWidget(QLabel("Página Fechar"))
        self.pages.addWidget(self.page_fechar)

        # Adiciona o QStackedWidget ao layout principal
        self.layout_principal.addWidget(self.pages)

        # ========== MENU SUPERIOR ==========
        # Cria um QFrame para conter os botões do menu superior
        self.menu_superior = QFrame(self)
        self.menu_superior.setMinimumSize(QSize(600, 0))
        self.menu_superior.setMaximumSize(QSize(1800, 1200))
        self.menu_superior.setFrameShape(QFrame.Shape.StyledPanel)

        # Layout horizontal para organizar os botões dentro do menu superior
        self.layout_menu = QHBoxLayout(self.menu_superior)
        self.layout_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Cria o botão "Abrir", aplica estilo e adiciona ao layout
        self.button_abrir = QPushButton("Abrir", self.menu_superior)
        self._estilizar_botao(self.button_abrir)
        self.layout_menu.addWidget(self.button_abrir)

        # Cria o botão "Listar", aplica estilo e adiciona ao layout
        self.button_listar = QPushButton("Listar", self.menu_superior)
        self._estilizar_botao(self.button_listar)
        self.layout_menu.addWidget(self.button_listar)

        # Cria o botão "Fechar", aplica estilo e adiciona ao layout
        self.button_fechar = QPushButton("Fechar", self.menu_superior)
        self._estilizar_botao(self.button_fechar)
        self.layout_menu.addWidget(self.button_fechar)

        # Adiciona o menu ao layout principal da tela (acima do QStackedWidget)
        self.layout_principal.insertWidget(0, self.menu_superior)

        # ========== CONEXÕES DOS BOTÕES ==========
        # Quando o botão "Abrir" é clicado, muda para a página de abertura
        self.button_abrir.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_abrir))

        # Quando o botão "Listar" é clicado, muda para a página de listagem
        self.button_listar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_listar))

        # Quando o botão "Fechar" é clicado, muda para a página de fechamento
        self.button_fechar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_fechar))

        # Pagina padrão inicial (listar)
        self.pages.setCurrentWidget(self.page_listar)

    # ========== MÉTODO AUXILIAR ==========
    def _estilizar_botao(self, botao):
        """
        Aplica um estilo visual padrão aos botões:
        - Define o tamanho mínimo e máximo
        - Altera o cursor para a "mão" quando o mouse passa por cima
        """
        botao.setMinimumSize(QSize(100, 50))
        botao.setMaximumSize(QSize(200, 70))
        botao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
