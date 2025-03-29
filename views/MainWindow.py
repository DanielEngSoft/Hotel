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
from styles.styles import data_menu_superior, hora_menu_superior, nome_menu_superior, style_label_menu_lateral
from views.pages.hospedagem import PageHospedagem
from views.pages.relatorios import PageRelatorios
from views.pages.reservas import PageReservas
from views.pages.quartos import PageQuartos
from views.pages.hospedes import PageHospedes

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Configuração inicial da janela ----------------------------------------
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1108, 706)
        MainWindow.setWindowTitle("Horizonte Prime")
        # -----------------------------------------------------------------------
    
        # Widget central---------------------------------------------------------
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        # -----------------------------------------------------------------------

        # Layout principal vertical ---------------------------------------------
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        # -----------------------------------------------------------------------
    
        # Frame superior ---------------------------------------------------------
        self.frame_superior = QFrame(self.centralwidget)
        self.frame_superior.setObjectName("frame_superior")
        self.frame_superior.setMinimumSize(QSize(0, 50))
        self.frame_superior.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_superior.setFrameShadow(QFrame.Shadow.Raised)
    
        # Layout horizontal do frame superior
        self.layout_frame_superior = QHBoxLayout(self.frame_superior)
        self.layout_frame_superior.setObjectName("layout_frame_superior")
    
        # Elementos do frame superior
        self.label_horizonte_prime = QLabel(self.frame_superior)
        self.label_horizonte_prime.setObjectName("label_horizonte_prime")
        self.label_horizonte_prime.setText("Horizonte Prime")
        self.label_horizonte_prime.setStyleSheet(nome_menu_superior())
        self.label_horizonte_prime.setMaximumHeight(45)
        self.layout_frame_superior.addWidget(self.label_horizonte_prime)    
        # Espaçador horizontal
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout_frame_superior.addItem(self.horizontalSpacer)

        # Label com data e hora

            # Cria os labels
        self.label_data = QLabel()
        self.label_hora = QLabel()
        
        # Estilização
        self.label_data.setStyleSheet(data_menu_superior())
        self.label_hora.setStyleSheet(data_menu_superior())
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_data)
        layout.addWidget(self.label_hora)
        
        # Configura o timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_relogio)
        self.timer.start(1000)  # Atualiza a cada 1 segundo
        
        # Atualiza imediatamente
        self.atualizar_relogio()


        self.layout_frame_superior.addWidget(self.label_data)
        self.layout_frame_superior.addWidget(self.label_hora)
    
        self.button_sair = QPushButton(self.frame_superior)
        self.button_sair.setObjectName("button_sair")
        self.button_sair.setText("Sair")
        self.button_sair.setMinimumSize(QSize(0, 45))
        self.button_sair.setMaximumSize(QSize(50, 16777215))
        self.button_sair.clicked.connect(QApplication.instance().quit)
        self.layout_frame_superior.addWidget(self.button_sair)    
        self.verticalLayout.addWidget(self.frame_superior)
        # -----------------------------------------------------------------------
    
        # Layout principal horizontal[menu lateral | stacked] ---------------------------------------------
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
    
        # Menu lateral
        self.MenuLateral = QListWidget(self.centralwidget)
        self.MenuLateral.setObjectName("MenuLateral")
        self.MenuLateral.setMinimumSize(QSize(0, 50))
        self.MenuLateral.setMaximumSize(QSize(200, 1900))
    
        self.MenuLateral.setStyleSheet(style_label_menu_lateral())

        # Configurações adicionais do menu
        self.MenuLateral.setSpacing(15)
    
        # Adiciona itens ao menu
        for _ in range(5):
            QListWidgetItem(self.MenuLateral)
            
        # Adiciona texto aos itens do menu
        menu_items = ["Hospedagem", "Reservas", "Quartos", "Hospedes", "Relatorios"]
        for i, text in enumerate(menu_items):
            self.MenuLateral.item(i).setText(text)
        self.MenuLateral.currentRowChanged.connect(self.mudar_pagina)
        
        self.horizontalLayout.addWidget(self.MenuLateral)
    
        # Widget empilhado (páginas)
        self.pages = QStackedWidget(self.centralwidget)
        self.pages.setObjectName("pages")
    
        # Página 1 - Hospedagem
        self.pages.addWidget(PageHospedagem())
    
        # Página 2 - Reservas
        self.pages.addWidget(PageReservas())
    
        # Página 3 - Quartos
        self.pages.addWidget(PageQuartos())
    
        # Página 4 - Hóspedes
        self.pages.addWidget(PageHospedes())
    
        # Página 5 - Relatórios
        self.pages.addWidget(PageRelatorios())

        # Adiciona o stackedWidget ao horizontalLayout      
        self.horizontalLayout.addWidget(self.pages)

        # Definindo a página inicial do stackedWidget
        self.pages.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

        self.verticalLayout.addLayout(self.horizontalLayout)
        
    def atualizar_relogio(self):
        agora = QDateTime.currentDateTime()
        
        # Formata a data (ex: "Segunda-Feira 15/01/2024")
        data_formatada = agora.toString("dddd '-' d'/'MM'/'yyyy").replace("Monday", "Segunda-feira").replace("Tuesday", "Terça-feira").replace("Wednesday", "Quarta-feira").replace("Thursday", "Quinta-feira").replace("Friday", "Sexta-feira").replace("Saturday", "Sábado").replace("Sunday", "Domingo")
        data_formatada = data_formatada[0].upper() + data_formatada[1:]  # Capitaliza o dia da semana
        
        # Formata a hora (ex: "14:30:45")
        hora_formatada = agora.toString("HH:mm:ss")
        
        self.label_data.setText(data_formatada)
        self.label_hora.setText(hora_formatada)
    
    def mudar_pagina(self, index):
        self.pages.setCurrentIndex(index)