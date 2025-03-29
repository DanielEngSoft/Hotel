from PySide6.QtCore import (
        QCoreApplication, QDate, QDateTime, QLocale,
        QMetaObject, QObject, QPoint, QRect,
        QSize, QTime, QUrl, Qt
)
from PySide6.QtGui import (
        QBrush, QColor, QConicalGradient, QCursor,
        QFont, QFontDatabase, QGradient, QIcon,
        QImage, QKeySequence, QLinearGradient, QPainter,
        QPalette, QPixmap, QRadialGradient, QTransform
)
from PySide6.QtWidgets import (
        QApplication, QFrame, QHBoxLayout, QLabel,
        QListView, QListWidget, QListWidgetItem, QMainWindow,
        QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
        QVBoxLayout, QWidget
)

class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            # Configuração inicial da janela
            if not MainWindow.objectName():
                MainWindow.setObjectName("MainWindow")
            MainWindow.resize(1108, 706)
        
            # Widget central
            self.centralwidget = QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
        
            # Layout principal vertical
            self.verticalLayout = QVBoxLayout(self.centralwidget)
            self.verticalLayout.setObjectName("verticalLayout")
        
            # Frame superior
            self.frame = QFrame(self.centralwidget)
            self.frame.setObjectName("frame")
            self.frame.setMinimumSize(QSize(0, 50))
            self.frame.setFrameShape(QFrame.Shape.StyledPanel)
            self.frame.setFrameShadow(QFrame.Shadow.Raised)
        
            # Layout horizontal do frame superior
            self.horizontalLayout_2 = QHBoxLayout(self.frame)
            self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
            # Elementos do frame superior
            self.label = QLabel(self.frame)
            self.label.setObjectName("label")
            self.horizontalLayout_2.addWidget(self.label)
        
            self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            self.horizontalLayout_2.addItem(self.horizontalSpacer)
        
            self.label_2 = QLabel(self.frame)
            self.label_2.setObjectName("label_2")
            self.horizontalLayout_2.addWidget(self.label_2)
        
            self.pushButton = QPushButton(self.frame)
            self.pushButton.setObjectName("pushButton")
            self.pushButton.setMinimumSize(QSize(0, 45))
            self.pushButton.setMaximumSize(QSize(50, 16777215))
            self.horizontalLayout_2.addWidget(self.pushButton)
        
            self.verticalLayout.addWidget(self.frame)
        
            # Layout principal horizontal
            self.horizontalLayout = QHBoxLayout()
            self.horizontalLayout.setObjectName("horizontalLayout")
        
            # Menu lateral
            self.MenuLateral = QListWidget(self.centralwidget)
            self.MenuLateral.setObjectName("MenuLateral")
            self.MenuLateral.setMinimumSize(QSize(0, 50))
            self.MenuLateral.setMaximumSize(QSize(200, 16777215))
        
            # Configuração da fonte do menu
            font = QFont()
            font.setFamilies(["Consolas"])
            font.setPointSize(14)
            font.setUnderline(False)
            font.setStrikeOut(False)
            font.setKerning(True)
            self.MenuLateral.setFont(font)
        
            # Configurações adicionais do menu
            self.MenuLateral.viewport().setProperty("cursor", QCursor(Qt.CursorShape.PointingHandCursor))
            self.MenuLateral.setLayoutMode(QListView.LayoutMode.SinglePass)
            self.MenuLateral.setSpacing(15)
        
            # Adiciona itens ao menu
            for _ in range(5):
                QListWidgetItem(self.MenuLateral)
            
            self.horizontalLayout.addWidget(self.MenuLateral)
        
            # Widget empilhado (páginas)
            self.stackedWidget = QStackedWidget(self.centralwidget)
            self.stackedWidget.setObjectName("stackedWidget")
        
            # Página 1 - Hospedagem
            self.page = QWidget()
            self.page.setObjectName("page")
            self.label_3 = QLabel(self.page)
            self.label_3.setObjectName("label_3")
            self.label_3.setGeometry(QRect(20, 20, 111, 31))
            self.stackedWidget.addWidget(self.page)
        
            # Página 2 - Reservas
            self.page_2 = QWidget()
            self.page_2.setObjectName("page_2")
            self.label_4 = QLabel(self.page_2)
            self.label_4.setObjectName("label_4")
            self.label_4.setGeometry(QRect(20, 70, 111, 31))
            self.stackedWidget.addWidget(self.page_2)
        
            # Página 3 - Quartos
            self.page_3 = QWidget()
            self.page_3.setObjectName("page_3")
            self.label_5 = QLabel(self.page_3)
            self.label_5.setObjectName("label_5")
            self.label_5.setGeometry(QRect(20, 120, 111, 31))
            self.stackedWidget.addWidget(self.page_3)
        
            # Página 4 - Hóspedes
            self.page_4 = QWidget()
            self.page_4.setObjectName("page_4")
            self.label_6 = QLabel(self.page_4)
            self.label_6.setObjectName("label_6")
            self.label_6.setGeometry(QRect(20, 180, 111, 31))
            self.stackedWidget.addWidget(self.page_4)
        
            # Página 5 - Relatórios
            self.page_5 = QWidget()
            self.page_5.setObjectName("page_5")
            self.label_7 = QLabel(self.page_5)
            self.label_7.setObjectName("label_7")
            self.label_7.setGeometry(QRect(20, 230, 111, 31))
            self.stackedWidget.addWidget(self.page_5)
        
            self.horizontalLayout.addWidget(self.stackedWidget)
            self.verticalLayout.addLayout(self.horizontalLayout)
        
            MainWindow.setCentralWidget(self.centralwidget)
            self.retranslateUi(MainWindow)
            self.stackedWidget.setCurrentIndex(0)
            QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            # Textos da interface
            MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
            self.label.setText(QCoreApplication.translate("MainWindow", "Horizonte Prime", None))
            self.label_2.setText(QCoreApplication.translate("MainWindow", "29/03/2025 12:24", None))
            self.pushButton.setText(QCoreApplication.translate("MainWindow", "Sair", None))
        
            # Textos do menu lateral
            __sortingEnabled = self.MenuLateral.isSortingEnabled()
            self.MenuLateral.setSortingEnabled(False)
        
            menu_items = ["Hospedagem", "Reservas", "Quartos", "Hospedes", "Relatorios"]
            for i, text in enumerate(menu_items):
                self.MenuLateral.item(i).setText(QCoreApplication.translate("MainWindow", text, None))
            
            self.MenuLateral.setSortingEnabled(__sortingEnabled)
        
            # Textos das páginas
            self.label_3.setText(QCoreApplication.translate("MainWindow", "Hospedagem", None))
            self.label_4.setText(QCoreApplication.translate("MainWindow", "Reservas", None))
            self.label_5.setText(QCoreApplication.translate("MainWindow", "Quartos", None))
            self.label_6.setText(QCoreApplication.translate("MainWindow", "Hospedes", None))
            self.label_7.setText(QCoreApplication.translate("MainWindow", "Relatorios", None))