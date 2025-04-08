# Importações do PySide6 para criação de interfaces gráficas
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QHBoxLayout, QPushButton,
    QStackedWidget, QLabel
)

# Importa a interface da tela de cadastro de hóspedes
from views.PagesMenu.PagesHospedes.page_cadastrar import Ui_page_cadastrar


class PageHospedes(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # Inicializa a superclasse QWidget
        self.setupUi()  # Chama o método para configurar a interface

    def setupUi(self):
        self.setObjectName("PageHospedes")  # Define o nome do objeto (opcional, útil para QSS ou debug)

        # Cria o layout principal da página (vertical)
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # ========== MENU SUPERIOR ==========
        # Cria um QFrame para conter os botões do menu superior
        self.menu_superior = QFrame(self)
        self.menu_superior.setMinimumSize(QSize(600, 0))  # Tamanho mínimo da largura
        self.menu_superior.setMaximumSize(QSize(1800, 1200))  # Tamanho máximo
        self.menu_superior.setFrameShape(QFrame.Shape.StyledPanel)  # Define uma borda estilizada

        # Layout horizontal para organizar os botões dentro do menu superior
        self.horizontalLayout = QHBoxLayout(self.menu_superior)
        self.horizontalLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centraliza os botões

        # Cria o botão "Cadastrar", aplica estilo e adiciona ao layout
        self.button_cadastrar = QPushButton("Cadastrar", self.menu_superior)
        self._estilizar_botao(self.button_cadastrar)
        self.horizontalLayout.addWidget(self.button_cadastrar)

        # Cria o botão "Listar", aplica estilo e adiciona ao layout
        self.button_listar = QPushButton("Listar", self.menu_superior)
        self._estilizar_botao(self.button_listar)
        self.horizontalLayout.addWidget(self.button_listar)

        # Cria o botão "Alterar", aplica estilo e adiciona ao layout
        self.button_alterar = QPushButton("Alterar", self.menu_superior)
        self._estilizar_botao(self.button_alterar)
        self.horizontalLayout.addWidget(self.button_alterar)

        # Adiciona o menu superior ao layout principal da tela
        self.layout_principal.addWidget(self.menu_superior)

        # ========== ÁREA DAS PÁGINAS ==========
        # Cria o QStackedWidget que vai conter as páginas (estilo "aba invisível")
        self.pages = QStackedWidget(self)

        # Cria a página de cadastro (importada de outro módulo)
        self.page_cadastrar = Ui_page_cadastrar()
        self.pages.addWidget(self.page_cadastrar)  # Adiciona ao QStackedWidget

        # Cria a página "Listar" (temporária com QLabel)
        self.page_listar = QWidget()
        self.page_listar.setLayout(QVBoxLayout())
        self.page_listar.layout().addWidget(QLabel("Página Listar"))
        self.pages.addWidget(self.page_listar)

        # Cria a página "Alterar" (temporária com QLabel)
        self.page_alterar = QWidget()
        self.page_alterar.setLayout(QVBoxLayout())
        self.page_alterar.layout().addWidget(QLabel("Página Alterar"))
        self.pages.addWidget(self.page_alterar)

        # Adiciona o QStackedWidget ao layout principal
        self.layout_principal.addWidget(self.pages)

        # ========== CONEXÕES DOS BOTÕES ==========
        # Quando o botão "Cadastrar" é clicado, muda para a página de cadastro
        self.button_cadastrar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_cadastrar))

        # Quando o botão "Listar" é clicado, muda para a página de listagem
        self.button_listar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_listar))

        # Quando o botão "Alterar" é clicado, muda para a página de alteração
        self.button_alterar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_alterar))

    # ========== MÉTODO AUXILIAR ==========
    def _estilizar_botao(self, botao):
        """
        Aplica um estilo visual padrão aos botões:
        - Define o tamanho mínimo e máximo
        - Altera o cursor para a "mão" quando o mouse passa por cima
        """
        botao.setMinimumSize(QSize(100, 50))  # Tamanho mínimo do botão
        botao.setMaximumSize(QSize(200, 70))  # Tamanho máximo do botão
        botao.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # Cursor de apontar (mãozinha)
