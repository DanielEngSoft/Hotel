from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QGroupBox
)

from utils.validadores_ui import valida_cpf, formata_nome, valida_telefone


class Ui_page_cadastrar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, page_cadastrar):
        if not page_cadastrar.objectName():
            page_cadastrar.setObjectName("page_cadastrar")

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.widget = QWidget(page_cadastrar)
        self.widget.setObjectName("widget")

        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        font = QFont()
        font.setPointSize(14)

        # GroupBox para agrupar os campos
        self.groupBox = QGroupBox("Dados do hospede", self.widget)
        self.groupBox.setFont(font)
        self.groupBoxLayout = QVBoxLayout(self.groupBox)
        self.groupBoxLayout.setSpacing(70)
        self.groupBoxLayout.setContentsMargins(10, 10, 10, 10)

        self

        # CPF
        self.horizontalLayout = QHBoxLayout()
        self.label_cpf = QLabel("CPF:", self.widget)
        self.label_cpf.setMinimumSize(QSize(100, 0))
        self.label_cpf.setMaximumSize(QSize(100, 16777215))
        self.label_cpf.setFont(font)
        self.label_cpf.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.horizontalLayout.addWidget(self.label_cpf)

        self.lineEdit_cpf = QLineEdit(self.widget)
        self.lineEdit_cpf.setInputMask("000.000.000-00;_")
        self.lineEdit_cpf.setPlaceholderText("000.000.000-00")
        self.lineEdit_cpf.setFont(font)
        self.lineEdit_cpf.setMinimumSize(150, 0)
        self.lineEdit_cpf.setMaximumSize(150, 16777215)
        self.horizontalLayout.addWidget(self.lineEdit_cpf)

        self.label_error_cpf = QLabel("", self.widget)
        self.label_error_cpf.setStyleSheet("color: red;")
        self.label_error_cpf.setFont(font)
        self.horizontalLayout.addWidget(self.label_error_cpf)

        self.horizontalLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.groupBoxLayout.addLayout(self.horizontalLayout)

        # Nome
        self.horizontalLayout_nome = QHBoxLayout()
        self.label_nome = QLabel("Nome:", self.widget)
        self.label_nome.setMinimumSize(QSize(100, 0))
        self.label_nome.setMaximumSize(QSize(100, 16777215))
        self.label_nome.setFont(font)
        self.horizontalLayout_nome.addWidget(self.label_nome)

        self.lineEdit_nome = QLineEdit(self.widget)
        self.lineEdit_nome.setMinimumSize(QSize(0, 30))
        self.lineEdit_nome.setMaximumSize(QSize(400, 16777215))
        self.lineEdit_nome.setFont(font)
        self.lineEdit_nome.setPlaceholderText("Digite o nome completo")
        self.horizontalLayout_nome.addWidget(self.lineEdit_nome)

        self.label_error_nome = QLabel("", self.widget)
        self.label_error_nome.setStyleSheet("color: red;")
        self.label_error_nome.setFont(font)
        self.horizontalLayout_nome.addWidget(self.label_error_nome)

        self.horizontalLayout_nome.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.groupBoxLayout.addLayout(self.horizontalLayout_nome)

        # Telefone
        self.horizontalLayout_telefone = QHBoxLayout()
        self.label_telefone = QLabel("Telefone:", self.widget)
        self.label_telefone.setMinimumSize(QSize(100, 0))
        self.label_telefone.setMaximumSize(QSize(100, 16777215))
        self.label_telefone.setFont(font)
        self.horizontalLayout_telefone.addWidget(self.label_telefone)

        self.lineEdit_telefone = QLineEdit(self.widget)
        self.lineEdit_telefone.setMinimumSize(QSize(0, 30))
        self.lineEdit_telefone.setMaximumSize(QSize(145, 16777215))
        self.lineEdit_telefone.setFont(font)
        self.lineEdit_telefone.setInputMask("(00)00000-0000;_")
        self.horizontalLayout_telefone.addWidget(self.lineEdit_telefone)

        self.label_error_telefone = QLabel("", self.widget)
        self.label_error_telefone.setStyleSheet("color: red;")
        self.label_error_telefone.setFont(font)
        self.horizontalLayout_telefone.addWidget(self.label_error_telefone)

        self.horizontalLayout_telefone.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.groupBoxLayout.addLayout(self.horizontalLayout_telefone)

        # Endereço: estado + cidade
        self.horizontalLayout_endereco = QHBoxLayout()
        self.comboBox = QComboBox(self.widget)
        self.comboBox.addItems([
            "PI", "MA", "CE", "PE", "BA", "TO", "PB", "RN", "AL", "SE", "DF", "GO",
            "PA", "MT", "MG", "ES", "RJ", "SP", "RO", "AM", "RR", "AC", "AP", "MS", "PR", "SC", "RS"
        ])
        self.comboBox.setFont(font)
        self.horizontalLayout_endereco.addWidget(self.comboBox)

        self.label_vazia = QLabel(self.widget)
        self.label_vazia.setMinimumSize(QSize(25, 0))
        self.horizontalLayout_endereco.addWidget(self.label_vazia)

        self.lineEdit_cidade = QLineEdit(self.widget)
        self.lineEdit_cidade.setMinimumSize(QSize(150, 0))
        self.lineEdit_cidade.setMaximumSize(QSize(400, 16777215))
        self.lineEdit_cidade.setFont(font)
        self.lineEdit_cidade.setPlaceholderText("Cidade")
        self.horizontalLayout_endereco.addWidget(self.lineEdit_cidade)

        self.label_error_cidade = QLabel("", self.widget)
        self.label_error_cidade.setStyleSheet("color: red;")
        self.label_error_cidade.setFont(font)
        self.horizontalLayout_endereco.addWidget(self.label_error_cidade)

        self.horizontalLayout_endereco.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.groupBoxLayout.addLayout(self.horizontalLayout_endereco)

        # Empresa
        self.horizontalLayout_empresa = QHBoxLayout()
        self.label_empresa = QLabel("Empresa:", self.widget)
        self.label_empresa.setMinimumSize(QSize(100, 0))
        self.label_empresa.setMaximumSize(QSize(100, 16777215))
        self.label_empresa.setFont(font)
        self.horizontalLayout_empresa.addWidget(self.label_empresa)

        self.lineEdit_empresa = QLineEdit(self.widget)
        self.lineEdit_empresa.setMinimumSize(QSize(0, 30))
        self.lineEdit_empresa.setMaximumSize(QSize(400, 16777215))
        self.lineEdit_empresa.setFont(font)
        self.lineEdit_empresa.setPlaceholderText("Digite o nome da empresa")
        self.horizontalLayout_empresa.addWidget(self.lineEdit_empresa)
        self.label_invisivel = QLabel(self.widget)
        self.horizontalLayout_empresa.addWidget(self.label_invisivel)

        self.groupBoxLayout.addLayout(self.horizontalLayout_empresa)

        self.verticalLayout.addWidget(self.groupBox)

        # Botão
        self.horizontalLayout_button = QHBoxLayout()
        self.horizontalLayout_button.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.pushButton = QPushButton("Cadastrar", self.widget)
        self.pushButton.setFont(font)
        self.pushButton.setMinimumWidth(150)
        self.pushButton.setStyleSheet("""
                                                QPushButton {
                                                background-color: green; 
                                                color: white;
                                                }
                                            """)
        self.horizontalLayout_button.addWidget(self.pushButton)

        self.pushButton.clicked.connect(self.abrir_cadastro)

        self.horizontalLayout_button.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_button)

        self.verticalLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        layout.addWidget(self.widget)

    def abrir_cadastro(self):
        # Limpa mensagens de erro
        self.label_error_cpf.setText("")
        self.label_error_nome.setText("")
        self.label_error_telefone.setText("")
        self.label_error_cidade.setText("")

        cpf = self.lineEdit_cpf.text()
        telefone = self.lineEdit_telefone.text()

        nome = self.lineEdit_nome.text()
        nome = formata_nome(nome)
        cidade = self.lineEdit_cidade.text()
        cidade = formata_nome(cidade)
        endereco = self.comboBox.currentText() + " - " + cidade
        empresa = self.lineEdit_empresa.text()
        empresa = formata_nome(empresa)

        erro = False

        if not valida_cpf(cpf):
            self.label_error_cpf.setText(" CPF inválido*")
            erro = True
        if not nome:
            self.label_error_nome.setText(" Nome obrigatório*")
            erro = True
        if not cidade:
            self.label_error_cidade.setText(" Cidade obrigatória*")
            erro = True
        if not valida_telefone(telefone):
            self.label_error_telefone.setText(" Telefone inválido*")
            erro = True

        if erro:
            return

        if not empresa:
            empresa = "------"

        # Aqui você pode prosseguir com o cadastro
        print("Cadastro realizado com sucesso!")
