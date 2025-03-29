from PySide6.QtCore import (
        QCoreApplication, QDate, QDateTime, QLocale,
        QMetaObject, QObject, QPoint, QRect,
        QSize, QTime, QUrl, Qt,
        QTimer, QDateTime
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
        MainWindow.setWindowTitle("Horizonte Prime")
    
        # Widget central
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
    
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
        self.label_horizonte_prime = QLabel(self.frame)
        self.label_horizonte_prime.setObjectName("label_horizonte_prime")
        self.label_horizonte_prime.setText("Horizonte Prime")
        self.label_horizonte_prime.setMaximumHeight(45)
        self.horizontalLayout_2.addWidget(self.label_horizonte_prime)    
        # Espaçador horizontal
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        # Label com data e hora

            # Cria os labels
        self.label_data = QLabel()
        self.label_hora = QLabel()
        
        # Estilização
        self.label_data.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            qproperty-alignment: AlignCenter;
            min-height: 45px;
            max-height: 45px;
        """)
        
        self.label_hora.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            qproperty-alignment: AlignCenter;
            min-height: 45px;
            max-height: 45px;
        """)        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_data)
        layout.addWidget(self.label_hora)
        self.setLayout(layout)
        
        # Configura o timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_relogio)
        self.timer.start(1000)  # Atualiza a cada 1 segundo
        
        # Atualiza imediatamente
        self.atualizar_relogio()


        self.horizontalLayout_2.addWidget(self.label_data)
        self.horizontalLayout_2.addWidget(self.label_hora)
    
        self.button_sair = QPushButton(self.frame)
        self.button_sair.setObjectName("button_sair")
        self.button_sair.setText("Sair")
        self.button_sair.setMinimumSize(QSize(0, 45))
        self.button_sair.setMaximumSize(QSize(50, 16777215))
        self.horizontalLayout_2.addWidget(self.button_sair)
    
        self.verticalLayout.addWidget(self.frame)
    
        # Layout principal horizontal
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
    
        # Menu lateral
        self.MenuLateral = QListWidget(self.centralwidget)
        self.MenuLateral.setObjectName("MenuLateral")
        self.MenuLateral.setMinimumSize(QSize(0, 50))
        self.MenuLateral.setMaximumSize(QSize(200, 1900))
    
        # Configuração da fonte do menu
        font = QFont()
        font.setFamilies(["Consolas"])
        font.setPointSize(14)
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
        self.page_hospedagem = QWidget()
        self.page_hospedagem.setObjectName("page_hospedagem")
        self.label_hospedagem = QLabel(self.page_hospedagem)
        self.label_hospedagem.setObjectName("label_hospedagem")
        self.label_hospedagem.text = "Hospedagem"
        self.label_hospedagem.setGeometry(QRect(20, 20, 111, 31))
        self.stackedWidget.addWidget(self.page_hospedagem)
    
        # Página 2 - Reservas
        self.page_reservas = QWidget()
        self.page_reservas.setObjectName("page_reservas")
        self.label_reservas = QLabel(self.page_reservas)
        self.label_reservas.setObjectName("label_reservas")
        self.label_reservas.text = "Reservas"
        self.label_reservas.setGeometry(QRect(20, 20, 111, 31))
        self.stackedWidget.addWidget(self.page_reservas)
    
        # Página 3 - Quartos
        self.page_quartos = QWidget()
        self.page_quartos.setObjectName("page_quartos")
        self.label_quartos = QLabel(self.page_quartos)
        self.label_quartos.setObjectName("label_quartos")
        self.label_quartos.text = "Quartos"
        self.label_quartos.setGeometry(QRect(20, 20, 111, 31))
        self.stackedWidget.addWidget(self.page_quartos)
    
        # Página 4 - Hóspedes
        self.page_hospedes = QWidget()
        self.page_hospedes.setObjectName("page_hospedes")
        self.label_hospedes = QLabel(self.page_hospedes)
        self.label_hospedes.setObjectName("label_hospedes")
        self.label_hospedes.text = "Hóspedes"
        self.label_hospedes.setGeometry(QRect(20, 20, 111, 31))
        self.stackedWidget.addWidget(self.page_hospedes)
    
        # Página 5 - Relatórios
        self.page_relatorios = QWidget()
        self.page_relatorios.setObjectName("page_relatorios")
        self.label_relatorios = QLabel(self.page_relatorios)
        self.label_relatorios.setObjectName("label_relatorios")
        self.label_relatorios.text = "Relatórios"
        self.label_relatorios.setGeometry(QRect(20, 20, 111, 31))
        self.stackedWidget.addWidget(self.page_relatorios)        
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
    
        self.stackedWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

    
        # Textos do menu lateral
        __sortingEnabled = self.MenuLateral.isSortingEnabled()
        self.MenuLateral.setSortingEnabled(False)
    
        menu_items = ["Hospedagem", "Reservas", "Quartos", "Hospedes", "Relatorios"]
        for i, text in enumerate(menu_items):
            self.MenuLateral.item(i).setText(QCoreApplication.translate("MainWindow", text, None))
        
        self.MenuLateral.setSortingEnabled(__sortingEnabled)
        
    def atualizar_relogio(self):
        agora = QDateTime.currentDateTime()
        
        # Formata a data (ex: "Segunda-feira, 15 de Janeiro de 2024")
        data_formatada = agora.toString("d'/'M'/'yyyy")
        data_formatada = data_formatada[0].upper() + data_formatada[1:]  # Capitaliza o dia da semana
        
        # Formata a hora (ex: "14:30:45")
        hora_formatada = agora.toString("HH:mm:ss")
        
        self.label_data.setText(data_formatada)
        self.label_hora.setText(hora_formatada)