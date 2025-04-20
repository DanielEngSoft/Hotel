from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QGroupBox
)

from operations.Ui.hospedes_operations import varifica_cpf_existe, cadastra_hospede, procura_hospede_por_cpf
from styles.styles import style_botao_verde, style_groupbox
from utils.validadores_ui import valida_cpf, formata_nome, valida_telefone


class Ui_page_cadastrar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, page_cadastrar):
        if not page_cadastrar.objectName():
            page_cadastrar.setObjectName("page_cadastrar")

        # Layout principal vertical para centralizar o conteúdo
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Espaço superior
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Container central que agrupa todo o conteúdo da tela
        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setContentsMargins(0, 0, 0, 0)

        # Fonte padrão
        font = QFont()
        font.setPointSize(14)

        # GroupBox estilizado com layout de formulário
        self.groupBox = QGroupBox("Dados do hóspede", self)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(style_groupbox())
        self.groupBoxLayout = QFormLayout(self.groupBox)
        self.groupBoxLayout.setSpacing(30)
        self.groupBoxLayout.setContentsMargins(10, 10, 10, 10)

        # Layout da seção principal
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # Função auxiliar para adicionar campo + label de erro
        def create_input_with_error(input_widget, error_label):
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(input_widget)
            layout.addWidget(error_label)
            return container

        # CPF
        self.lineEdit_cpf = QLineEdit()
        self.lineEdit_cpf.setInputMask("000.000.000-00;_")
        self.lineEdit_cpf.setPlaceholderText("000.000.000-00")
        self.lineEdit_cpf.setFont(font)
        self.lineEdit_cpf.setMinimumWidth(150)

        # Garante que o cursor vai para o início ao focar no campo
        def cpf_focus_in_event(event):
            QLineEdit.focusInEvent(self.lineEdit_cpf, event)
            QTimer.singleShot(0, lambda: self.lineEdit_cpf.setCursorPosition(0))

        def update_cpf_label():
            cpf = self.lineEdit_cpf.text()
            if len(cpf) == 14:
                procura_hospede_por_cpf(cpf)

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

        # Endereço: UF + Cidade
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

        # Adiciona o GroupBox centralizado
        self.verticalLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)

        # Botão cadastrar com espaçamento lateral
        self.pushButton = QPushButton("Cadastrar")
        self.pushButton.setFont(font)
        self.pushButton.setMinimumWidth(150)
        self.pushButton.setStyleSheet(style_botao_verde())
        self.pushButton.clicked.connect(self.abrir_cadastro)

        self.horizontalLayout_button = QHBoxLayout()
        self.horizontalLayout_button.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.horizontalLayout_button.addWidget(self.pushButton)
        self.horizontalLayout_button.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.verticalLayout.addLayout(self.horizontalLayout_button)

        # Espaço inferior dentro do container central
        self.verticalLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Adiciona o layout centralizado ao container principal
        center_layout.addLayout(self.verticalLayout)
        layout.addWidget(center_container)

        # Espaço inferior externo
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def abrir_cadastro(self):
        # Limpa mensagens de erro
        self.label_error_cpf.setText("")
        self.label_error_nome.setText("")
        self.label_error_telefone.setText("")
        self.label_error_cidade.setText("")

        # Coleta e formata dados
        cpf = self.lineEdit_cpf.text()
        telefone = self.lineEdit_telefone.text()
        nome = formata_nome(self.lineEdit_nome.text())
        cidade = formata_nome(self.lineEdit_cidade.text())
        endereco = self.comboBox.currentText() + " - " + cidade
        empresa = formata_nome(self.lineEdit_empresa.text())
        erro = False

        # Validações
        if not valida_cpf(cpf):
            self.label_error_cpf.setText(" CPF inválido*")
            erro = True
        if varifica_cpf_existe(cpf):
            self.label_error_cpf.setText(" CPF já cadastrado*")
            erro = True
        if not nome:
            self.label_error_nome.setText(" Nome obrigatório*")
            erro = True
        elif len(nome) < 4:
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

        # Preenche valor padrão para empresa se vazio
        if not empresa:
            empresa = "------"

        # Tenta cadastrar o hóspede
        try:
            cadastra_hospede(nome, cpf, telefone, endereco, empresa)
            QMessageBox.information(self, "Cadastro", "Cadastro realizado com sucesso!")

            # Limpa os campos após o cadastro
            self.lineEdit_cpf.clear()
            self.lineEdit_nome.clear()
            self.lineEdit_telefone.clear()
            self.lineEdit_cidade.clear()
            self.lineEdit_empresa.clear()

        except Exception as e:
            QMessageBox.warning(self, "Erro ao cadastrar", "Tente novamente")
