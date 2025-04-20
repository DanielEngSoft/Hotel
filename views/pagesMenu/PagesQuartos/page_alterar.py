from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QGroupBox
)
from operations.Ui.quartos_operations import verifica_quarto_existe, alterar_quarto
from styles.styles import style_botao_verde, style_groupbox

# Cores e estilos reutilizáveis
COR_SUCESSO = "color: green;"
COR_ERRO = "color: red;"
BORDA_ERRO = "border: 1px solid red;"
BORDA_PADRAO = "border: 1px solid lightgray;"


class Ui_page_alterar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, page_alterar):
        if not page_alterar.objectName():
            page_alterar.setObjectName("page_alterar")

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.widget = QWidget(page_alterar)
        self.widget.setObjectName("widget")

        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        font = QFont()
        font.setPointSize(14)

        # GroupBox com estilo
        self.groupBox = QGroupBox("Alterar quarto", self.widget)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(style_groupbox())
        self.groupBoxLayout = QFormLayout(self.groupBox)
        self.groupBoxLayout.setSpacing(20)
        self.groupBoxLayout.setContentsMargins(10, 10, 10, 10)

        # Função auxiliar para agrupar input e erro
        def create_input_with_error(input_widget, error_label):
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)
            layout.addWidget(input_widget)
            layout.addWidget(error_label)
            return container

        # Número do quarto
        self.lineEdit_numero = QLineEdit()
        self.lineEdit_numero.setInputMask("000; ")
        self.lineEdit_numero.setFont(font)
        self.lineEdit_numero.setMinimumWidth(60)
        self.lineEdit_numero.setStyleSheet(BORDA_PADRAO)

        def numero_focus_in_event(event):
            QLineEdit.focusInEvent(self.lineEdit_numero, event)
            QTimer.singleShot(0, lambda: self.lineEdit_numero.setCursorPosition(0))

        self.lineEdit_numero.focusInEvent = numero_focus_in_event

        self.label_error_numero = QLabel("")
        self.label_error_numero.setStyleSheet(COR_ERRO)
        self.label_error_numero.setFont(font)

        self.groupBoxLayout.addRow("Número:", create_input_with_error(self.lineEdit_numero, self.label_error_numero))

        # Tipo do quarto
        self.comboBox_tipo = QComboBox()
        self.comboBox_tipo.setFont(font)
        self.comboBox_tipo.addItems([
            'Solteiro', 'Casal', 'Casal + Solteiro',
            'Casal + 2 Solteiros', '2 Solteiros', '3 Solteiros'
        ])
        self.comboBox_tipo.setMinimumWidth(200)
        self.groupBoxLayout.addRow("Novo tipo:", self.comboBox_tipo)

        # Adiciona GroupBox ao layout
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.groupBox, alignment=Qt.AlignHCenter)

        # Botão cadastrar centralizado
        self.horizontalLayout_button = QHBoxLayout()
        self.horizontalLayout_button.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.pushButton = QPushButton("Alterar")
        self.pushButton.setFont(font)
        self.pushButton.setMinimumWidth(150)
        self.pushButton.setStyleSheet(style_botao_verde())
        self.pushButton.clicked.connect(self.alterar_quarto)

        self.horizontalLayout_button.addWidget(self.pushButton)
        self.horizontalLayout_button.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_button)

        # Feedback geral
        self.label_feedback = QLabel("")
        self.label_feedback.setFont(font)
        self.label_feedback.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_feedback)

        self.verticalLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout.addWidget(self.widget)

    def alterar_quarto(self):
        # Limpa mensagens anteriores
        self.label_error_numero.setText("")
        self.label_feedback.setText("")
        self.lineEdit_numero.setStyleSheet(BORDA_PADRAO)

        numero_texto = self.lineEdit_numero.text().strip()
        tipo = self.comboBox_tipo.currentText()
        erro = False

        if not numero_texto:
            self.label_error_numero.setText(" Número obrigatório*")
            self.lineEdit_numero.setStyleSheet(BORDA_ERRO)
            erro = True
        else:
            try:
                numero = int(numero_texto)
                if not verifica_quarto_existe(numero):
                    self.label_error_numero.setText(" Quarto não cadastrado*")
                    self.lineEdit_numero.setStyleSheet(BORDA_ERRO)
                    erro = True
            except ValueError:
                self.label_error_numero.setText(" Número inválido*")
                self.lineEdit_numero.setStyleSheet(BORDA_ERRO)
                erro = True

        if erro:
            return

        # Cadastra no banco de dados
        try:
            alterar_quarto(numero, tipo)
            self.label_feedback.setText("Quarto atualizado com sucesso!")
            self.label_feedback.setStyleSheet(COR_SUCESSO)
            self.lineEdit_numero.clear()
        except Exception as e:
            self.label_feedback.setText(f"Erro ao atualizar o quarto: {str(e)}")
            self.label_feedback.setStyleSheet(COR_ERRO)

        # Limpa o feedback após 4 segundos
        QTimer.singleShot(4000, lambda: self.label_feedback.setText(""))
