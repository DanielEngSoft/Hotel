from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit,QMessageBox, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QGroupBox
)
from sqlalchemy.orm import sessionmaker
from models.models import Hospede, db

from operations.Ui.quartos_operations import varifica_quarto_existe, cadastra_quarto
from styles.styles import style_botao_verde, style_groupbox


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

        # GroupBox com estilo
        self.groupBox = QGroupBox("Dados do hóspede", self.widget)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(style_groupbox())
        self.groupBoxLayout = QFormLayout(self.groupBox)
        self.groupBoxLayout.setSpacing(30)
        self.groupBoxLayout.setContentsMargins(10, 10, 10, 10)

        def create_input_with_error(input_widget, error_label):
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(input_widget)
            layout.addWidget(error_label)
            return container

        def cpf_focus_in_event(event):
            QLineEdit.focusInEvent(self.lineEdit_cpf, event)
            QTimer.singleShot(0, lambda: self.lineEdit_cpf.setCursorPosition(0))

        def update_cpf_label():
            cpf = self.lineEdit_cpf.text()
            if len(cpf) == 14:
                Session = sessionmaker(bind=db.engine)
                with Session() as session:
                    hospede = session.query(Hospede).filter(Hospede.cpf == cpf).first()
        # CPF
        self.lineEdit_cpf = QLineEdit()
        self.lineEdit_cpf.setInputMask("000.000.000-00;_")
        self.lineEdit_cpf.setPlaceholderText("000.000.000-00")
        self.lineEdit_cpf.setFont(font)
        self.lineEdit_cpf.setMinimumWidth(150)
        self.lineEdit_cpf.focusInEvent = cpf_focus_in_event
        self.lineEdit_cpf.textChanged.connect(update_cpf_label)


        self.label_error_cpf = QLabel("")
        self.label_error_cpf.setStyleSheet("color: red;")
        self.label_error_cpf.setFont(font)

        self.groupBoxLayout.addRow("CPF:", create_input_with_error(self.lineEdit_cpf, self.label_error_cpf))

        # Nome
        self.lineEdit_nome = QLineEdit()
        self.lineEdit_nome.setPlaceholderText("Digite o nome completo")
        self.lineEdit_nome.setFont(font)
        self.lineEdit_nome.setMinimumWidth(300)

        self.label_error_nome = QLabel("")
        self.label_error_nome.setStyleSheet("color: red;")
        self.label_error_nome.setFont(font)

        self.groupBoxLayout.addRow("Nome:", create_input_with_error(self.lineEdit_nome, self.label_error_nome))

        # Telefone
        self.lineEdit_telefone = QLineEdit()
        self.lineEdit_telefone.setInputMask("(00)00000-0000;_")
        self.lineEdit_telefone.setFont(font)
        self.lineEdit_telefone.setMinimumWidth(150)

        self.label_error_telefone = QLabel("")
        self.label_error_telefone.setStyleSheet("color: red;")
        self.label_error_telefone.setFont(font)

        self.groupBoxLayout.addRow("Telefone:", create_input_with_error(self.lineEdit_telefone, self.label_error_telefone))

        # Endereço (UF + Cidade)
        endereco_container = QWidget()
        endereco_layout = QHBoxLayout(endereco_container)
        endereco_layout.setContentsMargins(0, 0, 0, 0)

        self.comboBox = QComboBox()
        self.comboBox.setFont(font)
        self.comboBox.addItems([
            "PI", "MA", "CE", "PE", "BA", "TO", "PB", "RN", "AL", "SE", "DF", "GO",
            "PA", "MT", "MG", "ES", "RJ", "SP", "RO", "AM", "RR", "AC", "AP", "MS", "PR", "SC", "RS"
        ])

        self.lineEdit_cidade = QLineEdit()
        self.lineEdit_cidade.setPlaceholderText("Cidade")
        self.lineEdit_cidade.setFont(font)
        self.lineEdit_cidade.setMinimumWidth(150)

        self.label_error_cidade = QLabel("")
        self.label_error_cidade.setStyleSheet("color: red;")
        self.label_error_cidade.setFont(font)

        endereco_layout.addWidget(self.comboBox)
        endereco_layout.addSpacing(10)
        endereco_layout.addWidget(self.lineEdit_cidade)
        endereco_layout.addWidget(self.label_error_cidade)

        self.groupBoxLayout.addRow("Endereço:", endereco_container)

        # Empresa
        self.lineEdit_empresa = QLineEdit()
        self.lineEdit_empresa.setPlaceholderText("Digite o nome da empresa")
        self.lineEdit_empresa.setFont(font)
        self.lineEdit_empresa.setMinimumWidth(300)

        self.groupBoxLayout.addRow("Empresa:", self.lineEdit_empresa)

        self.verticalLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)

        # Botão cadastrar
        self.horizontalLayout_button = QHBoxLayout()
        self.horizontalLayout_button.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.pushButton = QPushButton("Cadastrar")
        self.pushButton.setFont(font)
        self.pushButton.setMinimumWidth(150)
        self.pushButton.setStyleSheet(style_botao_verde())
        self.pushButton.clicked.connect(self.abrir_cadastro)

        self.horizontalLayout_button.addWidget(self.pushButton)
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
        if varifica_cpf_existe(cpf):
            self.label_error_cpf.setText(" CPF já cadastrado*")
            erro = True
        if not nome:
            self.label_error_nome.setText(" Nome obrigatório*")
            erro = True
        if len(nome) < 4:
            self.label_error_nome.setText(" Nome muito curto*")
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
        
        try:
            Session = sessionmaker(bind=db.engine)
            with Session() as session:
                hospede = Hospede(nome=nome, cpf=cpf, telefone=telefone, endereco=endereco, empresa=empresa)
                session.add(hospede)
                session.commit()
                QMessageBox.warning(self, "Cadastro realizado", "Cadastro realizado com sucesso!")

                # Limpa os campos após o cadastro
                self.lineEdit_cpf.clear()
                self.lineEdit_nome.clear()
                self.lineEdit_telefone.clear()
                self.lineEdit_cidade.clear()
                self.lineEdit_empresa.clear()

        except Exception as e:
            QMessageBox.warning(self, "Erro ao cadastrar", "Tente novamente")

        print("Cadastro realizado com sucesso!")
