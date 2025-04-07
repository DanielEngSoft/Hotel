from PySide6 import QtWidgets
from PySide6.QtCore import (
    QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QSize, QTimer, Qt
)
from PySide6.QtGui import (
    QCursor, QFont, QIcon
)
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget
)

from styles.styles import (
    data_menu_superior, hora_menu_superior,
    nome_menu_superior, style_label_menu_lateral,
    style_botao_sair
)

from views.PagesMenu.hospedagem import PageHospedagem
from views.PagesMenu.hospedes import PageHospedes
from views.PagesMenu.quartos import PageQuartos
from views.PagesMenu.relatorios import PageRelatorios
from views.PagesMenu.reservas import PageReservas


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Configuração inicial da janela
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")

        MainWindow.resize(1108, 706)
        MainWindow.setWindowTitle("Horizonte Prime")
        MainWindow.setWindowIcon(QIcon("imgs/icons/hotel.png"))

        # Widget central
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Layout principal vertical
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Frame superior
        self.frame_superior = QFrame(self.centralwidget)
        self.frame_superior.setObjectName("frame_superior")
        self.frame_superior.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_superior.setFrameShadow(QFrame.Shadow.Raised)

        self.layout_frame_superior = QHBoxLayout(self.frame_superior)
        self.layout_frame_superior.setObjectName("layout_frame_superior")

        # Nome do sistema
        self.label_horizonte_prime = QLabel("Horizonte Prime", self.frame_superior)
        self.label_horizonte_prime.setObjectName("label_horizonte_prime")
        self.label_horizonte_prime.setStyleSheet(nome_menu_superior())
        self.label_horizonte_prime.setMaximumHeight(45)
        self.layout_frame_superior.addWidget(self.label_horizonte_prime)

        # Espaçador
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout_frame_superior.addItem(spacer)

        # Labels de data e hora
        self.label_data = QLabel()
        self.label_data.setStyleSheet(data_menu_superior())

        self.label_hora = QLabel()
        self.label_hora.setStyleSheet(hora_menu_superior())

        self.layout_frame_superior.addWidget(self.label_data)
        self.layout_frame_superior.addWidget(self.label_hora)

        # Botão sair
        self.button_sair = QPushButton("Sair", self.frame_superior)
        self.button_sair.setStyleSheet(style_botao_sair())
        self.button_sair.setObjectName("button_sair")
        self.button_sair.setMinimumSize(QSize(0, 40))
        self.button_sair.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_sair.setShortcut("Ctrl+Q")
        self.button_sair.clicked.connect(QApplication.instance().quit)
        self.layout_frame_superior.addWidget(self.button_sair)

        # Adiciona o frame superior ao layout principal
        self.verticalLayout.addWidget(self.frame_superior)

        # Layout horizontal principal (menu lateral + páginas)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Menu lateral
        self.MenuLateral = QListWidget(self.centralwidget)
        self.MenuLateral.setObjectName("MenuLateral")
        self.MenuLateral.setMinimumSize(QSize(0, 50))
        self.MenuLateral.setMaximumSize(QSize(220, 1900))
        self.MenuLateral.setStyleSheet(style_label_menu_lateral())
        self.MenuLateral.setSpacing(15)
        self.MenuLateral.setCursor(QCursor(Qt.PointingHandCursor))

        # Adiciona itens ao menu lateral
        menu_items = ["Hospedagem", "Reservas", "Quartos", "Hospedes", "Relatorios"]
        icons = ["🏨", "📅", "🛏️", "🧑", "📊"]  # Ou use QIcon com imagens se preferir

        for i, text in enumerate(menu_items):
            item = QListWidgetItem(f"{icons[i]}  {text}")
            self.MenuLateral.addItem(item)

        # Conecta mudança de item à função de troca de página
        self.MenuLateral.currentRowChanged.connect(self.mudar_pagina)

        self.horizontalLayout.addWidget(self.MenuLateral)

        # StackedWidget com as páginas
        self.pages = QStackedWidget(self.centralwidget)
        self.pages.setObjectName("pages")
        self.pages.addWidget(PageHospedagem())   # Index 0
        self.pages.addWidget(PageReservas())     # Index 1
        self.pages.addWidget(PageQuartos())      # Index 2
        self.pages.addWidget(PageHospedes())     # Index 3
        self.pages.addWidget(PageRelatorios())   # Index 4

        self.pages.setCurrentIndex(0)  # Página inicial

        self.horizontalLayout.addWidget(self.pages)
        self.verticalLayout.addLayout(self.horizontalLayout)

        # Timer para atualização de hora/data
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_relogio)
        self.timer.start(1000)  # Atualiza a cada 1 segundo
        self.atualizar_relogio()

        QMetaObject.connectSlotsByName(MainWindow)

    def atualizar_relogio(self):
        agora = QDateTime.currentDateTime()
        locale = QLocale(QLocale.Portuguese, QLocale.Brazil)

        data_formatada = locale.toString(agora, "dddd - dd/MM/yyyy")
        data_formatada = data_formatada[0].upper() + data_formatada[1:]

        hora_formatada = agora.toString("HH:mm:ss")

        self.label_data.setText(data_formatada)
        self.label_hora.setText(hora_formatada)

    def mudar_pagina(self, index):
        self.pages.setCurrentIndex(index)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyApp()
    window.show()
    app.exec()
