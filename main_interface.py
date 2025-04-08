# Importações do PySide6 para criação de interfaces gráficas
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

# Estilos personalizados importados de um arquivo separado
from styles.styles import (
    data_menu_superior, hora_menu_superior,
    nome_menu_superior, style_label_menu_lateral,
    style_botao_sair
)

# Importação das páginas do sistema
from views.PagesMenu.hospedagem import PageHospedagem
from views.PagesMenu.hospedes import PageHospedes
from views.PagesMenu.quartos import PageQuartos
from views.PagesMenu.relatorios import PageRelatorios
from views.PagesMenu.reservas import PageReservas


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Nome da janela principal
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")

        # Tamanho e título da janela
        MainWindow.resize(1108, 706)
        MainWindow.setWindowTitle("Horizonte Prime")
        MainWindow.setWindowIcon(QIcon("imgs/icons/hotel.png"))  # Ícone da janela

        # Widget central da janela principal
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Layout vertical principal (topo + conteúdo)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Frame superior (barra de topo)
        self.frame_superior = QFrame(self.centralwidget)
        self.frame_superior.setObjectName("frame_superior")
        self.frame_superior.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_superior.setFrameShadow(QFrame.Shadow.Raised)

        # Layout horizontal do frame superior
        self.layout_frame_superior = QHBoxLayout(self.frame_superior)
        self.layout_frame_superior.setObjectName("layout_frame_superior")

        # Nome do sistema
        self.label_horizonte_prime = QLabel("Horizonte Prime", self.frame_superior)
        self.label_horizonte_prime.setObjectName("label_horizonte_prime")
        self.label_horizonte_prime.setStyleSheet(nome_menu_superior())  # Estilo externo
        self.label_horizonte_prime.setMaximumHeight(45)
        self.layout_frame_superior.addWidget(self.label_horizonte_prime)

        # Espaçador para empurrar os elementos seguintes para o lado direito
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.layout_frame_superior.addItem(spacer)

        # Label de data atual (atualizada via timer)
        self.label_data = QLabel()
        self.label_data.setStyleSheet(data_menu_superior())

        # Label de hora atual (atualizada via timer)
        self.label_hora = QLabel()
        self.label_hora.setStyleSheet(hora_menu_superior())

        # Adiciona os labels de data e hora ao layout
        self.layout_frame_superior.addWidget(self.label_data)
        self.layout_frame_superior.addWidget(self.label_hora)

        # Botão "Sair" com atalho e ação para encerrar o app
        self.button_sair = QPushButton("Sair", self.frame_superior)
        self.button_sair.setObjectName("button_sair")
        self.button_sair.setMinimumSize(QSize(0, 40))
        self.button_sair.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_sair.setShortcut("Ctrl+Q")  # Atalho de teclado
        self.button_sair.setStyleSheet(style_botao_sair())
        self.button_sair.clicked.connect(QApplication.instance().quit)  # Ação: fechar app
        self.layout_frame_superior.addWidget(self.button_sair)

        # Adiciona o frame superior ao layout principal
        self.verticalLayout.addWidget(self.frame_superior)

        # Layout horizontal principal (menu lateral + conteúdo)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Menu lateral (QListWidget com os itens de navegação)
        self.MenuLateral = QListWidget(self.centralwidget)
        self.MenuLateral.setObjectName("MenuLateral")
        self.MenuLateral.setMinimumSize(QSize(200, 50))
        self.MenuLateral.setMaximumSize(QSize(220, 1900))
        self.MenuLateral.setSpacing(15)  # Espaçamento entre os itens
        self.MenuLateral.setCursor(QCursor(Qt.PointingHandCursor))
        self.MenuLateral.setStyleSheet(style_label_menu_lateral())  # Estilo externo

        # Lista de itens e ícones do menu
        menu_items = ["Hospedagem", "Reservas", "Quartos", "Hospedes", "Relatorios"]
        icons = ["🏨", "📅", "🛏️", "🧑", "📊"]  # Emojis como ícones simples

        # Adiciona os itens com ícones ao menu lateral
        for i, text in enumerate(menu_items):
            item = QListWidgetItem(f"{icons[i]}  {text}")
            self.MenuLateral.addItem(item)

        # Conecta mudança de item à troca de página no conteúdo
        self.MenuLateral.currentRowChanged.connect(self.mudar_pagina)

        # Adiciona o menu lateral ao layout horizontal
        self.horizontalLayout.addWidget(self.MenuLateral)

        # Conteúdo principal (QStackedWidget com as páginas)
        self.pages = QStackedWidget(self.centralwidget)
        self.pages.setObjectName("pages")

        # Adiciona as páginas ao QStackedWidget
        self.pages.addWidget(PageHospedagem())   # Index 0
        self.pages.addWidget(PageReservas())     # Index 1
        self.pages.addWidget(PageQuartos())      # Index 2
        self.pages.addWidget(PageHospedes())     # Index 3
        self.pages.addWidget(PageRelatorios())   # Index 4

        self.pages.setCurrentIndex(0)  # Define página inicial como "Hospedagem"

        # Adiciona o widget de páginas ao layout horizontal
        self.horizontalLayout.addWidget(self.pages)

        # Adiciona o layout horizontal (menu + páginas) ao vertical principal
        self.verticalLayout.addLayout(self.horizontalLayout)

        # Timer para atualizar data e hora em tempo real
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_relogio)
        self.timer.start(1000)  # Atualiza a cada 1 segundo
        self.atualizar_relogio()  # Atualiza imediatamente ao iniciar

        # Conecta os sinais dos widgets
        QMetaObject.connectSlotsByName(MainWindow)

    def atualizar_relogio(self):
        """Atualiza os labels de data e hora com base na hora do sistema"""
        agora = QDateTime.currentDateTime()
        locale = QLocale(QLocale.Portuguese, QLocale.Brazil)

        # Data no formato "segunda-feira - 01/01/2025"
        data_formatada = locale.toString(agora, "dddd - dd/MM/yyyy").capitalize()

        # Hora no formato "HH:mm:ss"
        hora_formatada = agora.toString("HH:mm:ss")

        self.label_data.setText(data_formatada)
        self.label_hora.setText(hora_formatada)

    def mudar_pagina(self, index):
        """Troca a página exibida com base no item selecionado do menu lateral"""
        self.pages.setCurrentIndex(index)


# Classe principal da aplicação
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa a interface


# Execução da aplicação
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyApp()
    window.show()
    app.exec()
