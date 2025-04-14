# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QWidget)
from views.PagesMenu.PagesHospedagem.page_ficha import Ui_page_ficha
from views.PagesMenu.PagesHospedagem.page_encerrar import Ui_page_encerrar

class Ui_page_hospedagem(QWidget):
    def __init__(self, hospedagem, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Hospedagem - Quarto {getattr(hospedagem.quarto, 'numero', 'Desconhecido')}")
        self.hospedagem = hospedagem
        self.setGeometry(100, 100, 800, 600)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.stacked_widget_hospedagem = QStackedWidget(self)
        self.stacked_widget_hospedagem.setObjectName(u"stacked_widget_hospedagem")
        self.stacked_widget_hospedagem.setGeometry(QRect(10, 20, 851, 531))

        # *** Página Ficha *** ----------------------------------------------------------------------------------------------------
        self.page_ficha_widget = QWidget()
        self.page_ficha_layout = QVBoxLayout(self.page_ficha_widget)
        self.page_ficha = Ui_page_ficha(self.hospedagem)
        self.page_ficha_layout.addWidget(self.page_ficha)

        self.widget_header = QWidget(self.page_ficha) # Agora 'page_ficha' é um atributo de Ui_page_hospedagem
        self.widget_header.setObjectName(u"widget_header")
        self.horizontalLayout_header = QHBoxLayout(self.widget_header)
        self.horizontalLayout_header.setObjectName(u"horizontalLayout_header")
        self.horizontalLayout_header.setContentsMargins(0, 0, 0, 0)

        self.label_hospede_nome = QLabel(getattr(hospedagem.hospede, 'nome', 'Nome Desconhecido'))
        self.label_hospede_nome.setObjectName(u"label_hospede_nome")
        self.horizontalLayout_header.addWidget(self.label_hospede_nome)

        self.line_separator = QFrame(self.widget_header)
        self.line_separator.setObjectName(u"line_separator")
        self.line_separator.setFrameShape(QFrame.Shape.VLine)
        self.line_separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.horizontalLayout_header.addWidget(self.line_separator)

        self.label_numero_quarto = QLabel(f"Quarto: {getattr(hospedagem.quarto, 'numero', 'Desconhecido')}")
        self.label_numero_quarto.setObjectName(u"label_numero_quarto")
        self.horizontalLayout_header.addWidget(self.label_numero_quarto)

        self.horizontalSpacer_header = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_header.addItem(self.horizontalSpacer_header)

        self.button_encerrar_hospedagem = QPushButton("Encerrar")
        self.button_encerrar_hospedagem.setObjectName(u"button_encerrar_hospedagem")
        self.button_encerrar_hospedagem.setStyleSheet(u"background-color: rgb(170, 0, 0);")
        self.horizontalLayout_header.addWidget(self.button_encerrar_hospedagem)

        self.page_ficha_layout.insertWidget(0, self.widget_header)
        self.stacked_widget_hospedagem.addWidget(self.page_ficha_widget)

        # *** Página Encerrar *** -------------------------------------------------------------------------------------------------------
        self.page_encerrar_widget = QWidget()
        self.page_encerrar_layout = QVBoxLayout(self.page_encerrar_widget)
        self.page_encerrar = Ui_page_encerrar(hospedagem=self.hospedagem)
        self.page_encerrar_layout.addWidget(self.page_encerrar)

        # Criando o header para a página de encerramento (similar ao da página ficha)
        self.page_encerrar_header = QWidget(self.page_encerrar_widget)
        self.page_encerrar_header.setObjectName(u"page_encerrar_header")
        self.page_encerrar_header.setMaximumHeight(35)
        
        self.horizontalLayout_page_encerrar_header = QHBoxLayout(self.page_encerrar_header)
        self.horizontalLayout_page_encerrar_header.setObjectName(u"horizontalLayout_page_encerrar_header")
        self.horizontalLayout_page_encerrar_header.setContentsMargins(0, 0, 0, 0)

        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.setObjectName(u"button_voltar")
        self.button_voltar.setStyleSheet(u"background-color: rgb(8, 127, 38);\ncolor: rgb(0, 0, 0);")
        self.horizontalLayout_page_encerrar_header.addWidget(self.button_voltar)

        self.horizontalSpacer_encerrar_header = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_page_encerrar_header.addItem(self.horizontalSpacer_encerrar_header)

        self.label_encerrar_nome_header = QLabel(f"Hóspede: {getattr(hospedagem.hospede, 'nome', 'Nome Desconhecido')}")
        self.label_encerrar_nome_header.setObjectName(u"label_encerrar_nome_header")
        self.horizontalLayout_page_encerrar_header.addWidget(self.label_encerrar_nome_header)

        self.line_encerrar_separator_header = QFrame(self.page_encerrar_header)
        self.line_encerrar_separator_header.setObjectName(u"line_encerrar_separator_header")
        self.line_encerrar_separator_header.setFrameShape(QFrame.Shape.VLine)
        self.line_encerrar_separator_header.setFrameShadow(QFrame.Shadow.Sunken)
        self.horizontalLayout_page_encerrar_header.addWidget(self.line_encerrar_separator_header)

        self.label_encerrar_quarto_header = QLabel(f"Quarto: {getattr(hospedagem.quarto, 'numero', 'Desconhecido')}")
        self.label_encerrar_quarto_header.setObjectName(u"label_encerrar_quarto_header")
        self.horizontalLayout_page_encerrar_header.addWidget(self.label_encerrar_quarto_header)

        # Adicionando o header ao layout da página de encerramento
        self.page_encerrar_layout.insertWidget(0, self.page_encerrar_header)

        self.stacked_widget_hospedagem.addWidget(self.page_encerrar_widget)

        # Layout principal do seu widget Ui_page_hospedagem
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.stacked_widget_hospedagem)
        self.setLayout(self.main_layout)

        self.stacked_widget_hospedagem.setCurrentIndex(0) # Exibe a primeira página (índice 0)

        QMetaObject.connectSlotsByName(self)

        # Conecte os sinais dos botões aos slots (funções que serão chamadas)
        self.button_encerrar_hospedagem.clicked.connect(self.mostrar_pagina_encerrar)
        self.button_voltar.clicked.connect(self.mostrar_pagina_ficha)

    def mostrar_pagina_encerrar(self):
        self.stacked_widget_hospedagem.setCurrentIndex(1) # Índice da página de encerramento
        self.adjustSize()

    def mostrar_pagina_ficha(self):
        self.stacked_widget_hospedagem.setCurrentIndex(0) # Índice da página da ficha
        self.resize(800, 650)