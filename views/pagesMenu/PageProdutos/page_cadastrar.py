from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QGroupBox
)

from operations.Ui.produtos_operations import create_produto, verifica_produto_existente
from styles.styles import style_botao_verde, style_groupbox
from utils.validadores_ui import valida_cpf, formata_nome, valida_telefone

class LineEditMonetario(QLineEdit):
    def __init__(self, total, parent=None):
        super().__init__(parent)
        self.setText(total)
        self.valor_cents = 0
        self.textEdited.connect(self.formatar_valor_monetario)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        QTimer.singleShot(0, lambda: self.setCursorPosition(len(self.text())))

    def formatar_valor_monetario(self, _):
        texto = self.text()
        apenas_numeros = ''.join(filter(str.isdigit, texto))
        self.valor_cents = int(apenas_numeros) if apenas_numeros else 0

        reais = self.valor_cents // 100
        centavos = self.valor_cents % 100
        texto_formatado = f"R$ {reais}.{centavos:02d}"

        self.blockSignals(True)
        self.setText(texto_formatado)
        self.blockSignals(False)
        self.setCursorPosition(len(texto_formatado))

    def get_valor_float(self):
        return self.valor_cents / 100.0

class Ui_page_cadastrar_produto(QWidget):
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
        self.groupBox = QGroupBox("Cadastrar produto", self)
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
        
        # Descrição
        self.lineEdit_descricao = QLineEdit()
        self.lineEdit_descricao.setPlaceholderText("Nome do produto")
        self.lineEdit_descricao.setFont(font)
        self.lineEdit_descricao.setMinimumWidth(300)

        self.label_error_descricao = QLabel("")
        self.label_error_descricao.setStyleSheet("color: red;")
        self.label_error_descricao.setFont(font)

        self.groupBoxLayout.addRow("Produto:", create_input_with_error(self.lineEdit_descricao, self.label_error_descricao))

        # Valor
        self.lineEdit_valor = LineEditMonetario(total="R$ 0.00")
        self.lineEdit_valor.setFont(font)
        self.lineEdit_valor.setMaximumWidth(150)

        self.groupBoxLayout.addRow("Valor:", self.lineEdit_valor)

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
        self.label_error_descricao.setText("")

        # Coleta e formata dados
        descricao = self.lineEdit_descricao.text()
        erro = False

        # Validações
        if not descricao:
            self.label_error_descricao.setText(" Nome obrigatório*")
            erro = True
        elif len(descricao) < 4:
            self.label_error_descricao.setText(" Descrição muito curta*")
            erro = True
        elif verifica_produto_existente(descricao):
            self.label_error_descricao.setText(" Produto já cadastrado*")
            erro = True

        if erro:
            return
        
        # Tenta cadastrar o produto
        try:
            create_produto(descricao, self.lineEdit_valor.get_valor_float())
            QMessageBox.information(self, "Cadastro", "Cadastro realizado com sucesso!")

            # Limpa os campos após o cadastro
            self.lineEdit_descricao.clear()
            self.lineEdit_valor.setText("R$ 0.00")

        except Exception as e:
            QMessageBox.warning(self, "Erro ao cadastrar", "Tente novamente")
