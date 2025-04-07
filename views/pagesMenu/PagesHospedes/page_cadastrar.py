from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget
)

class Ui_page_cadastrar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, page_cadastrar):
        if not page_cadastrar.objectName():
            page_cadastrar.setObjectName("page_cadastrar")

        # Layout principal
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Tamanho da janela
        page_cadastrar.resize(1000, 655)

        # Widget principal
        self.widget = QWidget(page_cadastrar)
        self.widget.setObjectName("widget")

        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        font = QFont()
        font.setPointSize(14)

        # CPF
        self.horizontalLayout = QHBoxLayout()
        self.label_cpf = QLabel("CPF:", self.widget)
        self.label_cpf.setMinimumSize(QSize(100, 0))
        self.label_cpf.setMaximumSize(QSize(100, 16777215))
        self.label_cpf.setFont(font)
        self.label_cpf.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.horizontalLayout.addWidget(self.label_cpf)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setMaximumSize(QSize(145, 16777215))
        self.lineEdit.setFont(font)
        self.lineEdit.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lineEdit.setInputMask("000.000.000-00;_")
        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout)

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
        self.lineEdit_nome.setPlaceholderText("Digite o nome completo")  # ← ADICIONADO
        self.horizontalLayout_nome.addWidget(self.lineEdit_nome)

        self.horizontalLayout_nome.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_nome)

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

        self.horizontalLayout_telefone.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_telefone)

        # Endereço: estado (combo), cidade
        self.horizontalLayout_endereco = QHBoxLayout()
        self.comboBox = QComboBox(self.widget)
        self.comboBox.addItems([
            "PI", "MA", "CE", "PE", "BA", "TO",
            "PB", "RN", "AL", "SE", "DF", "GO",
            "PA", "MT", "MG", "ES", "RJ", "SP",
            "RO", "AM", "RR", "AC", "AP", "MS",
            "PR", "SC", "RS"
        ])
        self.comboBox.setFont(font)
        self.horizontalLayout_endereco.addWidget(self.comboBox)

        self.label_vazia = QLabel(self.widget)  # espaço reservado (vazio)
        self.label_vazia.setMinimumSize(QSize(25, 0))
        self.horizontalLayout_endereco.addWidget(self.label_vazia)

        self.lineEdit_cidade = QLineEdit(self.widget)
        self.lineEdit_cidade.setMinimumSize(QSize(150, 0))
        self.lineEdit_cidade.setMaximumSize(QSize(400, 16777215))
        self.lineEdit_cidade.setFont(font)
        self.lineEdit_cidade.setPlaceholderText("Cidade")
        self.horizontalLayout_endereco.addWidget(self.lineEdit_cidade)

        self.horizontalLayout_endereco.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_endereco)

        # Empresa
        self.horizontalLayout_empresa = QHBoxLayout()
        self.label_4 = QLabel("Empresa:", self.widget)
        self.label_4.setMinimumSize(QSize(100, 0))
        self.label_4.setFont(font)
        self.horizontalLayout_empresa.addWidget(self.label_4)

        self.lineEdit_empresa = QLineEdit(self.widget)
        self.lineEdit_empresa.setMinimumSize(QSize(0, 30))
        self.lineEdit_empresa.setMaximumSize(QSize(400, 16777215))
        self.lineEdit_empresa.setFont(font)
        self.lineEdit_empresa.setPlaceholderText("Nome da empresa")  # ← ADICIONADO
        self.horizontalLayout_empresa.addWidget(self.lineEdit_empresa)

        self.horizontalLayout_empresa.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.verticalLayout.addLayout(self.horizontalLayout_empresa)

        # Separador visual
        self.separator = QFrame(self.widget)  # ← ADICIONADO
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.separator)

        # Botão
        self.horizontalLayout_button = QHBoxLayout()
        self.horizontalLayout_button.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.pushButton = QPushButton("Cadastrar", self.widget)
        self.pushButton.setFont(font)
        self.horizontalLayout_button.addWidget(self.pushButton)

        self.horizontalLayout_button.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_button)

        layout.addWidget(self.widget)
