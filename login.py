from PySide6.QtCore import QMetaObject, QRect, Qt, QThread, Signal, QSize, QTimer
from PySide6.QtGui import QFont, QMovie, QKeyEvent, QIcon, QPixmap
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMainWindow, QVBoxLayout, QWidget, QStyleFactory)

from styles.styles import style_groupbox_login, style_botao_verde, style_botao_vermelho
import sys
import time
import traceback
import qt_material

from main_interface import Ui_MainWindow  # Interface da janela principal


class WorkerThread(QThread):
    """
    Thread auxiliar usada para simular um processo de carregamento (ex: validação de login).
    """
    finished = Signal()

    def run(self):
        time.sleep(2)
        self.finished.emit()


class Ui_Form(QWidget):
    """
    Interface gráfica da tela de login.
    """
    def __init__(self):
        super().__init__(parent=None)
        self.setupUi(self)

    def setupUi(self, Form):
        """
        Inicializa os componentes da interface.
        """
        if not Form.objectName():
            Form.setObjectName("Form")

        Form.setFixedSize(571, 376)
        Form.setWindowTitle("Login")
        Form.setWindowIcon(QIcon("imgs/login_white.png"))
        

        font = QFont()
        font.setPointSize(14)

        # Layout principal
        self.layout_principal = QVBoxLayout(Form)

        # Caixa principal com título
        self.groupBox = QGroupBox(Form)
        self.groupBox.setStyleSheet(style_groupbox_login())
        self.groupBox.setObjectName("groupBox")  
        self.groupBox.setTitle("Horizonte Prime")
        self.groupBox.setMaximumHeight(250)
        self.groupBox.setFont(font)

        # Layout principal da caixa
        self.layout_groupbox = QVBoxLayout(self.groupBox)
        self.layout_groupbox.setSpacing(10)
        self.layout_groupbox.setContentsMargins(15, 15, 15, 15)

        # Layout de formulário para campos de login
        self.formLayout = QFormLayout()

        # Usuário Icon
        self.label_usuario = QLabel("", self.groupBox)
        self.icon_usuario = QIcon("imgs/usuario_white.png")
        self.label_usuario.setPixmap(self.icon_usuario.pixmap(32, 32))
        # Usuário input
        self.lineEdit__usuario = QLineEdit(self.groupBox)
        self.lineEdit__usuario.setFont(font)
        self.formLayout.addRow(self.label_usuario, self.lineEdit__usuario)

        # Senha Icon
        self.label_senha = QLabel("", self.groupBox)
        self.icon_senha = QIcon("imgs/senha_white.png")
        self.label_senha.setPixmap(self.icon_senha.pixmap(32, 32))
        # Senha input
        self.lineEdit_senha = QLineEdit(self.groupBox)
        self.lineEdit_senha.setFont(font)
        self.lineEdit_senha.setEchoMode(QLineEdit.EchoMode.Password)
        self.formLayout.addRow(self.label_senha, self.lineEdit_senha)

        self.layout_groupbox.addLayout(self.formLayout)

        # Mensagem de feedback (erro ou sucesso)
        self.label_feedbeck = QLabel("", self.groupBox)
        self.label_feedbeck.setAlignment(Qt.AlignCenter)
        self.label_feedbeck.setFont(font)
        self.layout_groupbox.addWidget(self.label_feedbeck)

        # Adiciona o groupbox ao layout principal
        self.layout_principal.addWidget(self.groupBox)

        # Botões de ação
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(50, 5, 50, 0)

        self.pushButton_sair = QPushButton("Sair", self.groupBox)
        self.pushButton_sair.setFont(font)
        self.pushButton_sair.setStyleSheet(style_botao_vermelho())
        self.pushButton_sair.clicked.connect(self.button_sair_clicked)
        self.horizontalLayout.addWidget(self.pushButton_sair)

        self.pushButton__entrar = QPushButton("Entrar", self.groupBox)
        self.pushButton__entrar.setFont(font)
        self.pushButton__entrar.setStyleSheet(style_botao_verde())
        self.pushButton__entrar.clicked.connect(self.button_entrar_clicked)
        self.horizontalLayout.addWidget(self.pushButton__entrar)

        # Adiciona os botões ao layout principal
        self.layout_principal.addLayout(self.horizontalLayout)
        self.layout_principal.addStretch()
        
        # Spinner de carregamento
        self.label_spinner = QLabel("", self.groupBox)
        self.label_spinner.setAlignment(Qt.AlignCenter)
        self.movie = QMovie("imgs/spinner.gif")
        self.movie.setScaledSize(QSize(55, 55))
        self.label_spinner.setMovie(self.movie)
        self.label_spinner.hide()

        # Adiciona o spinner ao layout principal
        self.layout_principal.addWidget(self.label_spinner)

        # Adicionando espaço 
        self.layout_principal.addStretch()

        QMetaObject.connectSlotsByName(Form)

    def button_sair_clicked(self):
        """
        Fecha a janela de login.
        """
        self.groupBox.parent().close()

    def button_entrar_clicked(self):
        """
        Inicia o processo de login.
        """
        self.login()

    def login(self):
        """
        Verifica credenciais e simula carregamento em segundo plano.
        """
        usuario = self.lineEdit__usuario.text()
        senha = self.lineEdit_senha.text()

        if usuario == "admin" and senha == "admin":
            self.label_feedbeck.setText("Login realizado com sucesso!")
            self.pushButton__entrar.setEnabled(False)
            self.movie.start()
            self.label_spinner.show()

            self.thread = WorkerThread()
            self.thread.finished.connect(self.abrir_tela_principal)
            self.thread.start()
        else:
            self.label_feedbeck.setText("Usuário ou senha inválidos!")
            self.label_feedbeck.setStyleSheet("color: red;")
            QTimer.singleShot(2000, lambda: self.label_feedbeck.setText(""))

    def abrir_tela_principal(self):
        """
        Abre a interface principal da aplicação após o login.
        """
        self.movie.stop()
        self.label_spinner.hide()

        self.main_window = QMainWindow()
        self.main_interface = Ui_MainWindow()
        self.main_interface.setupUi(self.main_window)
        self.main_window.show()

        self.groupBox.parent().close()

    def keyPressEvent(self, event: QKeyEvent):
        """
        Atalhos de teclado: Enter para login, Esc para sair.
        """
        if event.key() == Qt.Key_Escape:
            self.button_sair_clicked()
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.button_entrar_clicked()


if __name__ == "__main__":
    """
    Inicializa e executa a aplicação.
    """
    app = QApplication(sys.argv)
    app.setStyle("Windows11")

    window = Ui_Form()
    window.show()
    sys.exit(app.exec())
