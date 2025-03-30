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
            Form.resize(773, 808)
            self.verticalLayout_2 = QVBoxLayout(Form)
            self.verticalLayout_2.setObjectName(u"verticalLayout_2")
            self.menu_superior_page_hospedagem = QFrame(Form)
            self.menu_superior_page_hospedagem.setObjectName(u"menu_superior_page_hospedagem")
            self.menu_superior_page_hospedagem.setMinimumSize(QSize(600, 0))
            self.menu_superior_page_hospedagem.setMaximumSize(QSize(1800, 1200))
            self.menu_superior_page_hospedagem.setFrameShape(QFrame.Shape.StyledPanel)
            self.menu_superior_page_hospedagem.setFrameShadow(QFrame.Shadow.Raised)
            self.horizontalLayout = QHBoxLayout(self.menu_superior_page_hospedagem)
            self.horizontalLayout.setObjectName(u"horizontalLayout")
            self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

            self.horizontalLayout.addItem(self.horizontalSpacer)

            self.button_abrir = QPushButton(self.menu_superior_page_hospedagem)
            self.button_abrir.setObjectName(u"button_abrir")
            self.button_abrir.setMinimumSize(QSize(100, 50))
            self.button_abrir.setMaximumSize(QSize(200, 70))
            self.button_abrir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.button_abrir.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_abrir))

            self.horizontalLayout.addWidget(self.button_abrir)

            self.button_listar = QPushButton(self.menu_superior_page_hospedagem)
            self.button_listar.setObjectName(u"button_listar")
            self.button_listar.setMinimumSize(QSize(100, 50))
            self.button_listar.setMaximumSize(QSize(200, 70))
            self.button_listar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.button_listar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_listar))

            self.horizontalLayout.addWidget(self.button_listar)

            self.button_fechar = QPushButton(self.menu_superior_page_hospedagem)
            self.button_fechar.setObjectName(u"button_fechar")
            self.button_fechar.setMinimumSize(QSize(100, 50))
            self.button_fechar.setMaximumSize(QSize(200, 70))
            self.button_fechar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.button_fechar.clicked.connect(lambda: self.pages.setCurrentWidget(self.page_fechar))

            self.horizontalLayout.addWidget(self.button_fechar)

            self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

            self.horizontalLayout.addItem(self.horizontalSpacer_2)

            self.verticalLayout_2.addWidget(self.menu_superior_page_hospedagem)

            self.pages = QStackedWidget(Form)
            self.pages.setObjectName(u"pages")
            self.page_abrir = QWidget()
            self.page_abrir.setObjectName(u"page_abrir")
            self.pages.addWidget(self.page_abrir)
            self.page_listar = QWidget()
            self.page_listar.setObjectName(u"page_listar")
            self.pages.addWidget(self.page_listar)
            self.page_fechar = QWidget()
            self.page_fechar.setObjectName(u"page_fechar")
            self.pages.addWidget(self.page_fechar)

            self.verticalLayout_2.addWidget(self.pages)

            self.retranslateUi(Form)
            self.pages.setCurrentIndex(0)
            QMetaObject.connectSlotsByName(Form)

        def retranslateUi(self, Form):
            Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
            self.button_abrir.setText(QCoreApplication.translate("Form", u"Abrir", None))
            self.button_listar.setText(QCoreApplication.translate("Form", u"Listar", None))
            self.button_fechar.setText(QCoreApplication.translate("Form", u"Fechar", None))