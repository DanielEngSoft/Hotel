from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout,QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

class PageHospedagem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, Form):
        # Verifica se o objeto tem nome, caso não tenha, define um nome
        if not Form.objectName():
            Form.setObjectName(u"Form")

        # Cria um layout vertical
        self.layout_principal = QVBoxLayout(Form)
        self.layout_principal.setObjectName(u"verticalLayout_2")

        # Cria um frame para o menu superior
        self.menu_superior_page_hospedagem = QFrame(Form)
        self.menu_superior_page_hospedagem.setObjectName(u"menu_superior_page_hospedagem")
        self.menu_superior_page_hospedagem.setMinimumSize(QSize(600, 0))
        self.menu_superior_page_hospedagem.setMaximumSize(QSize(1800, 1200))
        self.menu_superior_page_hospedagem.setFrameShape(QFrame.Shape.StyledPanel)
        self.menu_superior_page_hospedagem.setFrameShadow(QFrame.Shadow.Raised)

        # Cria um layout horizontal para o menu superior
        self.horizontalLayout = QHBoxLayout(self.menu_superior_page_hospedagem)
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        # Adiciona um espaçador horizontal
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        # Cria o botão abrir
        self.button_abrir = QPushButton(self.menu_superior_page_hospedagem)
        self.button_abrir.setObjectName(u"button_abrir")
        self.button_abrir.setText("Abrir")
        self.button_abrir.setMinimumSize(QSize(100, 50))
        self.button_abrir.setMaximumSize(QSize(200, 70))
        self.button_abrir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_abrir.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_abrir))

        self.horizontalLayout.addWidget(self.button_abrir)

        # Cria o botão listar
        self.button_listar = QPushButton(self.menu_superior_page_hospedagem)
        self.button_listar.setObjectName(u"button_listar")
        self.button_listar.setText("Listar")
        self.button_listar.setMinimumSize(QSize(100, 50))
        self.button_listar.setMaximumSize(QSize(200, 70))
        self.button_listar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_listar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_listar))

        self.horizontalLayout.addWidget(self.button_listar)

        # Cria o botão fechar
        self.button_fechar = QPushButton(self.menu_superior_page_hospedagem)
        self.button_fechar.setObjectName(u"button_fechar")
        self.button_fechar.setText("Fechar")
        self.button_fechar.setMinimumSize(QSize(100, 50))
        self.button_fechar.setMaximumSize(QSize(200, 70))
        self.button_fechar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_fechar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_fechar))

        self.horizontalLayout.addWidget(self.button_fechar)

        # Adiciona outro espaçador horizontal
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        # Adiciona o menu superior ao layout principal
        self.layout_principal.addWidget(self.menu_superior_page_hospedagem)

        # Cria um sta'cked widget para as páginas
        self.pages = QStackedWidget(Form)
        self.pages.setObjectName(u"pages")

        # Cria a página abrir
        self.page_abrir = QWidget()
        self.page_abrir.setObjectName(u"page_abrir")
        self.label_abrir = QLabel(self.page_abrir)
        self.label_abrir.setObjectName(u"label_abrir")
        self.label_abrir.setText("<h1>Abrir Hospedagem</h1>")
        self.pages.addWidget(self.page_abrir)

        # Cria a página listar
        self.page_listar = QWidget()
        self.page_listar.setObjectName(u"page_listar")
        self.label_listar = QLabel(self.page_listar)
        self.label_listar.setObjectName(u"label_listar")
        self.label_listar.setText("<h1>Listar Hospedagem</h1>")
        self.pages.addWidget(self.page_listar)

        # Cria a página fechar
        self.page_fechar = QWidget()
        self.page_fechar.setObjectName(u"page_fechar")
        self.label_fechar = QLabel(self.page_fechar)
        self.label_fechar.setObjectName(u"label_fechar")
        self.label_fechar.setText("<h1>Fechar Hospedagem</h1>")
        self.pages.addWidget(self.page_fechar)

        # Adiciona o stacked widget ao layout principal
        self.layout_principal.addWidget(self.pages)

        # Define a página inicial do stacked widget das páginas
        self.pages.setCurrentIndex(0)

        # Configura a interface
        # QMetaObject.connectSlotsByName(Form) # faz conectar os slots com os nomes dos objetos. Slots