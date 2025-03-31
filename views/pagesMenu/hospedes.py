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

class PageHospedes(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        
        # Criando o layout principal
        self.layout_principal = QVBoxLayout(Form)
        self.layout_principal.setObjectName(u"verticalLayout_2")

        # Criando e configurando o frame para o menu superior
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
        self.button_cadastrar = QPushButton(self.menu_superior_page_hospedagem)
        self.button_cadastrar.setObjectName(u"button_cadastrar")
        self.button_cadastrar.setText("Cadastrar")
        self.button_cadastrar.setMinimumSize(QSize(100, 50))
        self.button_cadastrar.setMaximumSize(QSize(200, 70))
        self.button_cadastrar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_cadastrar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_cadastrar))

        self.horizontalLayout.addWidget(self.button_cadastrar)

        # Criando o botão listar
        self.button_listar = QPushButton(self.menu_superior_page_hospedagem)
        self.button_listar.setObjectName(u"button_listar")
        self.button_listar.setMinimumSize(QSize(100, 50))
        self.button_listar.setMaximumSize(QSize(200, 70))
        self.button_listar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_listar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_listar))

        self.horizontalLayout.addWidget(self.button_listar)

        # Criando o botão alterar
        self.button_alterar = QPushButton(self.menu_superior_page_hospedagem)
        self.button_alterar.setObjectName(u"button_alterar")
        self.button_alterar.setText("Alterar")
        self.button_alterar.setMinimumSize(QSize(100, 50))
        self.button_alterar.setMaximumSize(QSize(200, 70))
        self.button_alterar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_alterar.clicked.connect(lambda: self.pages.setCurrentWidget(self.alterar))

        self.horizontalLayout.addWidget(self.button_alterar)

        # Adicionando um espaçador horizontal
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        # Adicionando o menu superior ao layout principal
        self.layout_principal.addWidget(self.menu_superior_page_hospedagem)

        # Criando um stackedwidget para as páginas
        self.pages = QStackedWidget(Form)
        self.pages.setObjectName(u"pages")

        # Criando pagina cadastrar
        self.page_cadastrar = QWidget()
        self.page_cadastrar.setObjectName(u"page_cadastrar")
        self.pages.addWidget(self.page_cadastrar)
        
        self.page_listar = QWidget()
        self.page_listar.setObjectName(u"page_listar")
        self.pages.addWidget(self.page_listar)
        self.alterar = QWidget()
        self.alterar.setObjectName(u"page_alterar")
        self.pages.addWidget(self.alterar)

        self.layout_principal.addWidget(self.pages)

        self.retranslateUi(Form)
        self.pages.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.button_cadastrar.setText(QCoreApplication.translate("Form", u"Abrir", None))
        self.button_listar.setText(QCoreApplication.translate("Form", u"Listar", None))
        self.button_alterar.setText(QCoreApplication.translate("Form", u"Fechar", None))