from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

class PageQuartos(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
            
        # Criando o layout principal
        self.layout_principal = QVBoxLayout(Form)
        self.layout_principal.setObjectName(u"layout_principal")

        # Criando o frame superior
        self.menu_superior_page_hospedagem = QFrame(Form)
        self.menu_superior_page_hospedagem.setObjectName(u"menu_superior_page_hospedagem")
        self.menu_superior_page_hospedagem.setMinimumSize(QSize(600, 0))
        self.menu_superior_page_hospedagem.setMaximumSize(QSize(1800, 1200))
        self.menu_superior_page_hospedagem.setFrameShape(QFrame.Shape.StyledPanel)
        self.menu_superior_page_hospedagem.setFrameShadow(QFrame.Shadow.Raised)

        # Criando um layout horizontal para o menu superior
        self.horizontalLayout = QHBoxLayout(self.menu_superior_page_hospedagem)
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        # Adicionando um espaçador horizontal
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        # Criando o botão cadastrar
        self.button_listar = QPushButton(self.menu_superior_page_hospedagem)
        self.button_listar.setObjectName(u"button_listar")
        self.button_listar.setText("Listar")
        self.button_listar.setMinimumSize(QSize(100, 50))
        self.button_listar.setMaximumSize(QSize(200, 70))
        self.button_listar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_listar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_listar))

        self.horizontalLayout.addWidget(self.button_listar)

        # Criando o botão ocupados
        self.button_ocupados = QPushButton(self.menu_superior_page_hospedagem)
        self.button_ocupados.setObjectName(u"button_ocupados")
        self.button_ocupados.setText("Ocupados")
        self.button_ocupados.setMinimumSize(QSize(100, 50))
        self.button_ocupados.setMaximumSize(QSize(200, 70))
        self.button_ocupados.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_ocupados.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_ocupados))

        self.horizontalLayout.addWidget(self.button_ocupados)

        # Criando o botão desocupados
        self.button_desocupados = QPushButton(self.menu_superior_page_hospedagem)
        self.button_desocupados.setObjectName(u"button_desocupados")
        self.button_desocupados.setText("Desocupados")
        self.button_desocupados.setMinimumSize(QSize(100, 50))
        self.button_desocupados.setMaximumSize(QSize(200, 70))
        self.button_desocupados.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_desocupados.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_desocupados))

        self.horizontalLayout.addWidget(self.button_desocupados)

        # Adicionando um espaçador horizontal
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        # Adicionando o menu superior ao layout principal
        self.layout_principal.addWidget(self.menu_superior_page_hospedagem)

        # Criando o stackwidget para as páginas
        self.pages = QStackedWidget(Form)
        self.pages.setObjectName(u"pages")

        # Adicionando a page listar
        self.page_listar = QWidget()
        self.page_listar.setObjectName(u"page_listar")
        self.pages.addWidget(self.page_listar)

        # Adicionando a page ocupados
        self.page_ocupados = QWidget()
        self.page_ocupados.setObjectName(u"page_ocupados")
        self.pages.addWidget(self.page_ocupados)

        # Adicionando a page desocupados
        self.page_desocupados = QWidget()
        self.page_desocupados.setObjectName(u"page_desocupados")
        self.pages.addWidget(self.page_desocupados)

        # Adicionando o stackwidget ao layout principal
        self.layout_principal.addWidget(self.pages)

        # Definindo o índice inicial do stackwidget
        self.pages.setCurrentIndex(0)

        # QMetaObject.connectSlotsByName(Form)