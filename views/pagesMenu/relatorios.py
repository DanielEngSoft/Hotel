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

class PageRelatorios(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setupUi(self)

        def setupUi(self, Form):
            if not Form.objectName():
                Form.setObjectName(u"Form")

            # Definindo o layout principal
            self.layout_principal = QVBoxLayout(Form)
            self.layout_principal.setObjectName(u"layout_principal")

            # Criando e configurando o frame superior
            self.menu_superior_page_hospedagem = QFrame(Form)
            self.menu_superior_page_hospedagem.setObjectName(u"menu_superior_page_hospedagem")
            self.menu_superior_page_hospedagem.setMinimumSize(QSize(600, 0))
            self.menu_superior_page_hospedagem.setMaximumSize(QSize(1800, 1200))
            self.menu_superior_page_hospedagem.setFrameShape(QFrame.Shape.StyledPanel)
            self.menu_superior_page_hospedagem.setFrameShadow(QFrame.Shadow.Raised)

            # Criando o layout horizontal para o menu superior
            self.horizontalLayout = QHBoxLayout(self.menu_superior_page_hospedagem)
            self.horizontalLayout.setObjectName(u"horizontalLayout")

            # Adicionando um espaçador horizontal
            self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            self.horizontalLayout.addItem(self.horizontalSpacer)
            
            # Criando o botão abrir
            self.button_geral = QPushButton(self.menu_superior_page_hospedagem)
            self.button_geral.setObjectName(u"button_geral")
            self.button_geral.setText("Geral")
            self.button_geral.setMinimumSize(QSize(100, 50))
            self.button_geral.setMaximumSize(QSize(200, 70))
            self.button_geral.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.button_geral.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_geral))
            
            self.horizontalLayout.addWidget(self.button_geral)

            # Criando o botão listar
            self.button_hospede = QPushButton(self.menu_superior_page_hospedagem)
            self.button_hospede.setObjectName(u"button_hospede")
            self.button_hospede.setText("Hospede")
            self.button_hospede.setMinimumSize(QSize(100, 50))
            self.button_hospede.setMaximumSize(QSize(200, 70))
            self.button_hospede.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.button_hospede.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_hospede))

            self.horizontalLayout.addWidget(self.button_hospede)

            # Criando o botão fechar
            self.button_data = QPushButton(self.menu_superior_page_hospedagem)
            self.button_data.setObjectName(u"button_data")
            self.button_data.setText("Data")
            self.button_data.setMinimumSize(QSize(100, 50))
            self.button_data.setMaximumSize(QSize(200, 70))
            self.button_data.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.button_data.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_data))

            self.horizontalLayout.addWidget(self.button_data)

            # Adicionando um espaçador horizontal
            self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            self.horizontalLayout.addItem(self.horizontalSpacer_2)

            # Adicionando o menu superior ao layout principal
            self.layout_principal.addWidget(self.menu_superior_page_hospedagem)

            # Criando o QStackedWidget para as páginas
            self.pages = QStackedWidget(Form)
            self.pages.setObjectName(u"pages")

            # Criando as páginas
            self.page_geral = QWidget()
            self.page_geral.setObjectName(u"page_abrir")
            self.pages.addWidget(self.page_geral)
            self.page_hospede = QWidget()
            self.page_hospede.setObjectName(u"page_listar")
            self.pages.addWidget(self.page_hospede)
            self.page_data = QWidget()
            self.page_data.setObjectName(u"page_fechar")
            self.pages.addWidget(self.page_data)

            # Adicionando o QStackedWidget ao layout principal
            self.layout_principal.addWidget(self.pages)
            # Definindo a página inicial do QStackedWidget
            self.pages.setCurrentIndex(0)


            QMetaObject.connectSlotsByName(Form)