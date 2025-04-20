from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import  QKeyEvent

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget,
    QFrame, QHBoxLayout, QSizePolicy, QSpacerItem, QMessageBox,
    QStyle, QApplication
)

from views.PagesMenu.PagesHospedagem.page_ficha import Ui_page_ficha
from views.PagesMenu.PagesHospedagem.page_encerrar import Ui_page_encerrar
from views.PagesMenu.PagesHospedagem.page_alterar import Ui_page_alterar
from views.PagesMenu.PagesHospedagem.page_adiantamento import Ui_page_adiantamento

from styles.styles import style_botao_branco, style_botao_vermelho, style_botao_transparente


INDEX_FICHA = 0
INDEX_ENCERRAR = 1
INDEX_ALTERAR = 2
INDEX_ADIANTAMENTO = 3


class Ui_page_hospedagem(QWidget):
    def __init__(self, hospedagem):
        super().__init__()
        self.hospedagem = hospedagem
        self.setupUi()
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,\
                        QSize(900, 750), QApplication.primaryScreen().availableGeometry()))    
        self.setWindowTitle("Ficha de Hospedagem")

    def setupUi(self):
        self.layout = QVBoxLayout(self)

        # Cria o widget de páginas
        self.stacked_widget_hospedagem = QStackedWidget()
        self.layout.addWidget(self.stacked_widget_hospedagem)

        # Página Ficha
        self.page_ficha = QWidget()
        self.layout_ficha = QVBoxLayout(self.page_ficha)

        header_ficha = self._criar_header(
            self.hospedagem.hospede.nome,
            self.hospedagem.quarto.numero
        )

        self.button_encerrar = QPushButton("Encerrar")
        self.button_encerrar.setStyleSheet(style_botao_vermelho())
        self.button_encerrar.setMaximumWidth(150)
        self.button_encerrar.clicked.connect(self.mostrar_pagina_encerrar)
        header_ficha.layout().addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        header_ficha.layout().addWidget(self.button_encerrar)

        self.layout_ficha.addWidget(header_ficha)

        self.ui_page_ficha = Ui_page_ficha(self.hospedagem)
        self.layout_ficha.addWidget(self.ui_page_ficha)

        self.stacked_widget_hospedagem.addWidget(self.page_ficha)

        # Página Encerrar
        self.page_encerrar = QWidget()
        self.layout_encerrar = QVBoxLayout(self.page_encerrar)

        header_encerrar = self._criar_header(
            self.hospedagem.hospede.nome,
            self.hospedagem.quarto.numero,
            botao_voltar=True,
            funcao_voltar=self.mostrar_pagina_ficha
        )

        self.layout_encerrar.addWidget(header_encerrar)

        self.ui_page_encerrar = Ui_page_encerrar(self.hospedagem)

        # Recebe a instância da página Hospedagem
        self.ui_page_encerrar.set_page_hospedagem_instance(self)

        self.layout_encerrar.addWidget(self.ui_page_encerrar)

        self.stacked_widget_hospedagem.addWidget(self.page_encerrar)

        # Página Alterar
        self.page_alterar = QWidget()
        self.layout_alterar = QVBoxLayout(self.page_alterar)

        header_alterar = self._criar_header(
            self.hospedagem.hospede.nome,
            self.hospedagem.quarto.numero,
            botao_voltar=True,
            funcao_voltar=self.mostrar_pagina_ficha
        )

        self.layout_alterar.addWidget(header_alterar)

        self.ui_page_alterar = Ui_page_alterar(self.hospedagem)

        # Recebe a instância da página Hospedagem
        self.ui_page_alterar.set_page_hospedagem_instance(self)

        self.layout_alterar.addWidget(self.ui_page_alterar)

        self.stacked_widget_hospedagem.addWidget(self.page_alterar)

        # Página Adiantamento
        self.page_adiantamento = QWidget()
        self.layout_adiantamento = QVBoxLayout(self.page_adiantamento)

        header_adiantamento = self._criar_header(
            self.hospedagem.hospede.nome,
            self.hospedagem.quarto.numero,
            botao_voltar=True,
            funcao_voltar=self.mostrar_pagina_ficha
        )

        self.layout_adiantamento.addWidget(header_adiantamento)

        self.ui_page_adiantamento = Ui_page_adiantamento(self.hospedagem)

        # Recebe a instância da página Hospedagem
        self.ui_page_adiantamento.set_page_hospedagem_instance(self)

        self.layout_adiantamento.addWidget(self.ui_page_adiantamento)

        self.stacked_widget_hospedagem.addWidget(self.page_adiantamento)

    def _criar_header(self, titulo_hospede, numero_quarto, botao_voltar=False, funcao_voltar=None):
        header = QFrame()
        header.setContentsMargins(5, 5, 5, 5)
        header.setStyleSheet("background-color: #05452f;")
        header.setMaximumHeight(35)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        if botao_voltar:
            botao = QPushButton("Voltar")
            botao.setStyleSheet(style_botao_branco())
            if funcao_voltar:
                botao.clicked.connect(funcao_voltar)
            layout.addWidget(botao)
            layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        button_nome = QPushButton(titulo_hospede)
        button_nome.setStyleSheet(style_botao_transparente())
        button_nome.clicked.connect(self.mostrar_informacoes_hospede)
        layout.addWidget(button_nome)

        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.VLine)
        separador.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separador)

        label_quarto = QLabel(f"Quarto: {numero_quarto}")
        layout.addWidget(label_quarto)

        return header

    def mostrar_informacoes_hospede(self):
        hospede = self.hospedagem.hospede
        if hospede:
            QMessageBox.information(
                self,
                "Informações do Hóspede",
                f"Nome: {hospede.nome}\nCPF: {hospede.cpf}\nTelefone: {hospede.telefone}\nEndereço: {hospede.endereco}"
            )
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma informação de hóspede disponível.")

    def mostrar_pagina_ficha(self):
        self.stacked_widget_hospedagem.setCurrentIndex(INDEX_FICHA)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,\
                        QSize(800, 750), QApplication.primaryScreen().availableGeometry()))  
        self.setWindowTitle("Ficha de Hospedagem")

    def mostrar_pagina_encerrar(self):
        self.stacked_widget_hospedagem.setCurrentIndex(INDEX_ENCERRAR)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,\
                        QSize(600, 450), QApplication.primaryScreen().availableGeometry()))     
        self.setWindowTitle("Encerramento")      

    def mostrar_pagina_alterar(self):
        self.stacked_widget_hospedagem.setCurrentIndex(INDEX_ALTERAR)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,\
                        QSize(600, 450), QApplication.primaryScreen().availableGeometry()))  
        self.setWindowTitle("Alterar Hospedagem")

    def mostrar_pagina_adiantamento(self):
        self.stacked_widget_hospedagem.setCurrentIndex(INDEX_ADIANTAMENTO)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,\
                        QSize(600, 450), QApplication.primaryScreen().availableGeometry()))  
        self.setWindowTitle("Adicionar pagamento")

    def close_page_hospedagem(self):
        self.close()

                                
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_F5:
            self.mostrar_pagina_encerrar()
        if event.key() == Qt.Key_F6:
            self.mostrar_pagina_alterar()
        if event.key() == Qt.Key_Escape:
            self.close_page_hospedagem()
        if event.key() == Qt.Key_F4:
            self.mostrar_pagina_adiantamento()
            