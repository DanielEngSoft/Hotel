# Importações do PySide6 para criação de interfaces gráficas
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QHBoxLayout, QPushButton,
    QSpacerItem, QSizePolicy, QStackedWidget
)


class PageRelatorios(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # Inicializa o QWidget
        self.setupUi()  # Configura a interface

    def setupUi(self):
        self.setObjectName("PageRelatorios")

        # ========== LAYOUT PRINCIPAL ==========
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)

        # ========== MENU SUPERIOR ==========
        self.menu_superior = QFrame(self)
        self.menu_superior.setMinimumSize(QSize(600, 0))
        self.menu_superior.setMaximumSize(QSize(1800, 1200))
        self.menu_superior.setFrameShape(QFrame.Shape.StyledPanel)

        self.horizontalLayout = QHBoxLayout(self.menu_superior)
        self.horizontalLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botão "Geral"
        self.button_geral = QPushButton("Geral", self.menu_superior)
        self._estilizar_botao(self.button_geral)
        self.horizontalLayout.addWidget(self.button_geral)

        # Botão "Hóspede"
        self.button_hospede = QPushButton("Hospede", self.menu_superior)
        self._estilizar_botao(self.button_hospede)
        self.horizontalLayout.addWidget(self.button_hospede)

        # Botão "Data"
        self.button_data = QPushButton("Data", self.menu_superior)
        self._estilizar_botao(self.button_data)
        self.horizontalLayout.addWidget(self.button_data)

        # Adiciona o menu superior ao layout principal
        self.layout_principal.addWidget(self.menu_superior)

        # ========== ÁREA DAS PÁGINAS ==========
        self.pages = QStackedWidget(self)

        self.page_geral = QWidget()
        self.pages.addWidget(self.page_geral)

        self.page_hospede = QWidget()
        self.pages.addWidget(self.page_hospede)

        self.page_data = QWidget()
        self.pages.addWidget(self.page_data)

        self.layout_principal.addWidget(self.pages)

        # ========== CONEXÕES DOS BOTÕES ==========
        self.button_geral.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_geral))
        self.button_hospede.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_hospede))
        self.button_data.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_data))

        # Página inicial
        self.pages.setCurrentWidget(self.page_geral)

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
