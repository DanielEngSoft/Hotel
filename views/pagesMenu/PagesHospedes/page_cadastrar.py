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
        self.lineEdit.setText("..-")
        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout)

        # Nome
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_nome = QLabel("Nome:", self.widget)
        self.label_nome.setMinimumSize(QSize(100, 0))
        self.label_nome.setMaximumSize(QSize(100, 16777215))
        self.label_nome.setFont(font)
        self.horizontalLayout_2.addWidget(self.label_nome)

        self.lineEdit_2 = QLineEdit(self.widget)
        self.lineEdit_2.setMinimumSize(QSize(0, 30))
        self.lineEdit_2.setMaximumSize(QSize(400, 16777215))
        self.lineEdit_2.setFont(font)
        self.horizontalLayout_2.addWidget(self.lineEdit_2)

        self.horizontalLayout_2.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        # Telefone
        self.horizontalLayout_3 = QHBoxLayout()
        self.label_telefone = QLabel("Telefone:", self.widget)
        self.label_telefone.setMinimumSize(QSize(100, 0))
        self.label_telefone.setMaximumSize(QSize(100, 16777215))
        self.label_telefone.setFont(font)
        self.horizontalLayout_3.addWidget(self.label_telefone)

        self.lineEdit_3 = QLineEdit(self.widget)
        self.lineEdit_3.setMinimumSize(QSize(0, 30))
        self.lineEdit_3.setMaximumSize(QSize(145, 16777215))
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setInputMask("(00)00000-0000;_")
        self.horizontalLayout_3.addWidget(self.lineEdit_3)

        self.horizontalLayout_3.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        # Endereço: estado (combo), cidade
        self.horizontalLayout_6 = QHBoxLayout()
        self.comboBox = QComboBox(self.widget)
        self.comboBox.addItems(["PI", "MA", "CE", "TO", "PA", "PR", "BA", "PB", "SP", "RJ", "GO", "DF", "--"])
        self.comboBox.setFont(font)
        self.horizontalLayout_6.addWidget(self.comboBox)

        self.label_2 = QLabel(self.widget)  # espaço reservado (vazio)
        self.label_2.setMinimumSize(QSize(24, 0))
        self.horizontalLayout_6.addWidget(self.label_2)

        self.label = QLabel(self.widget)  # outro espaço reservado
        self.horizontalLayout_6.addWidget(self.label)

        self.lineEdit_5 = QLineEdit(self.widget)
        self.lineEdit_5.setMinimumSize(QSize(150, 0))
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setPlaceholderText("Cidade")
        self.horizontalLayout_6.addWidget(self.lineEdit_5)

        self.horizontalLayout_6.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_6)

        # Empresa
        self.horizontalLayout_4 = QHBoxLayout()
        self.label_4 = QLabel("Empresa:", self.widget)
        self.label_4.setMinimumSize(QSize(100, 0))
        self.label_4.setFont(font)
        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_4 = QLineEdit(self.widget)
        self.lineEdit_4.setMinimumSize(QSize(0, 30))
        self.lineEdit_4.setFont(font)
        self.horizontalLayout_4.addWidget(self.lineEdit_4)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        # Botão
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.pushButton = QPushButton("Cadastrar", self.widget)
        self.pushButton.setFont(font)
        self.horizontalLayout_5.addWidget(self.pushButton)

        self.horizontalLayout_5.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        layout.addWidget(self.widget)
