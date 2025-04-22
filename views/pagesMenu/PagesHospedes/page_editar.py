from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView, QComboBox, QFormLayout, QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from operations.Ui.hospedes_operations import procura_hospede_completo, procura_hospedes_por_nome, atualiza_hospede
from styles.styles import style_botao_verde, style_groupbox
from utils.validadores_ui import formata_nome, valida_telefone

class Ui_page_editar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, page_editar):
        if not page_editar.objectName():
            page_editar.setObjectName("page_editar")

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.widget = QWidget(page_editar)
        self.widget.setObjectName("widget")

        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        font = QFont()
        font.setPointSize(14)

        # Campo de busca por nome

        self.label_buscar = QLabel("Buscar:")
        self.label_buscar.setFont(font)
        self.label_buscar.setMaximumWidth(100)
        self.label_buscar.setFont(font)
        self.label_buscar.setStyleSheet(style_botao_verde())

        self.lineEdit_busca = QLineEdit()
        self.lineEdit_busca.setPlaceholderText("Nome do hóspede")
        self.lineEdit_busca.setFont(font)
        self.lineEdit_busca.setMaximumWidth(700)        
        self.lineEdit_busca.textChanged.connect(self.buscar_hospede) 

        # Layout horizontal para campo de busca + botão
        busca_layout = QHBoxLayout()
        busca_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        busca_layout.addWidget(self.label_buscar)
        busca_layout.addWidget(self.lineEdit_busca)
        self.verticalLayout.addLayout(busca_layout)

        # Tabela de resultados da busca
        self.tabela_resultados = QTableWidget()
        self.tabela_resultados.setVisible(False)
        self.tabela_resultados.setMaximumHeight(150)
        self.tabela_resultados.setMinimumWidth(800)
        self.tabela_resultados.setColumnCount(5)
        self.tabela_resultados.setHorizontalHeaderLabels(["Nome", "CPF", "Empresa", "Telefone", "Endereço"])
        self.tabela_resultados.setEditTriggers(QTableWidget.NoEditTriggers)  # impede edição direta
        self.tabela_resultados.setAlternatingRowColors(True)
        self.tabela_resultados.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela_resultados.cellClicked.connect(self.carregar_dados_hospede) 

        # Faz o cabeçalho se ajustar ao tamanho da tabela
        self.tabela_resultados.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Adiciona a tabela centralizada
        self.verticalLayout.addWidget(self.tabela_resultados, alignment=Qt.AlignCenter)

        # Linha separadora entre colunas
        self.line_separador = QFrame(self.widget)
        self.line_separador.setFrameShape(QFrame.HLine)
        self.line_separador.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_separador)

        # GroupBox estilizado para edição de dados
        self.groupBox = QGroupBox("Editar dados do hóspede", self.widget)
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

        # Campo Nome
        self.lineEdit_nome = QLineEdit()
        self.lineEdit_nome.setFont(font)
        self.lineEdit_nome.setMinimumWidth(300)
        self.label_error_nome = QLabel("")
        self.label_error_nome.setStyleSheet("color: red;")
        self.label_error_nome.setFont(font)
        self.groupBoxLayout.addRow("Nome:", create_input_with_error(self.lineEdit_nome, self.label_error_nome))

        # Campo Telefone
        self.lineEdit_telefone = QLineEdit()
        self.lineEdit_telefone.setInputMask("(00)00000-0000;_")
        self.lineEdit_telefone.setFont(font)
        self.label_error_telefone = QLabel("")
        self.label_error_telefone.setStyleSheet("color: red;")
        self.label_error_telefone.setFont(font)
        self.groupBoxLayout.addRow("Telefone:", create_input_with_error(self.lineEdit_telefone, self.label_error_telefone))

        # Campo Endereço (Estado + Cidade)
        endereco_container = QWidget()
        endereco_layout = QHBoxLayout(endereco_container)
        endereco_layout.setContentsMargins(0, 0, 0, 0)

        self.comboBox_estado = QComboBox()
        self.comboBox_estado.setFont(font)
        self.comboBox_estado.addItems([
            "PI", "MA", "CE", "PE", "BA", "TO", "PB", "RN", "AL", "SE", "DF", "GO",
            "PA", "MT", "MG", "ES", "RJ", "SP", "RO", "AM", "RR", "AC", "AP", "MS", "PR", "SC", "RS"
        ])

        self.lineEdit_cidade = QLineEdit()
        self.lineEdit_cidade.setFont(font)
        self.lineEdit_cidade.setMinimumWidth(150)
        self.label_error_cidade = QLabel("")
        self.label_error_cidade.setStyleSheet("color: red;")
        self.label_error_cidade.setFont(font)

        endereco_layout.addWidget(self.comboBox_estado)
        endereco_layout.addSpacing(10)
        endereco_layout.addWidget(self.lineEdit_cidade)
        endereco_layout.addWidget(self.label_error_cidade)

        self.groupBoxLayout.addRow("Endereço:", endereco_container)

        # Campo Empresa
        self.lineEdit_empresa = QLineEdit()
        self.lineEdit_empresa.setFont(font)
        self.lineEdit_empresa.setMinimumWidth(300)
        self.groupBoxLayout.addRow("Empresa:", self.lineEdit_empresa)

        # Adiciona GroupBox centralizado
        self.verticalLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)

        # Botão de salvar alterações
        self.pushButton_salvar = QPushButton("Salvar Alterações")
        self.pushButton_salvar.setFont(font)
        self.pushButton_salvar.setMinimumWidth(200)
        self.pushButton_salvar.setStyleSheet(style_botao_verde())
        self.pushButton_salvar.clicked.connect(self.salvar_alteracoes)

        # Label de confirmação
        self.label_confirmacao = QLabel("")
        self.label_confirmacao.setFont(font)
        self.label_confirmacao.setStyleSheet("color: green;")

        self.verticalLayout.addWidget(self.pushButton_salvar, alignment=Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_confirmacao, alignment=Qt.AlignCenter)

        layout.addWidget(self.widget)
        self.hospede_selecionado = None

    def buscar_hospede(self):
        nome = self.lineEdit_busca.text()
        self.tabela_resultados.setRowCount(0)

        hospedes = procura_hospedes_por_nome(nome)
        if hospedes:
            if self.lineEdit_busca.text() == "":
                self.tabela_resultados.setVisible(False)
            else:
                self.tabela_resultados.setVisible(True)
                for i, h in enumerate(hospedes):
                    self.tabela_resultados.insertRow(i)
                    for j, val in enumerate([h.nome, h.cpf, h.empresa, h.telefone, h.endereco]):
                        self.tabela_resultados.setItem(i, j, QTableWidgetItem(str(val)))
        else:
            self.tabela_resultados.setVisible(False)
        self._ajustar_altura_tabela()

    def carregar_dados_hospede(self, row, column):
        nome = self.tabela_resultados.item(row, 0).text()
        empresa = self.tabela_resultados.item(row, 2).text()
        telefone = self.tabela_resultados.item(row, 3).text()
        endereco = self.tabela_resultados.item(row, 4).text()

        self.lineEdit_nome.setText(nome)
        self.lineEdit_telefone.setText(telefone)
        self.lineEdit_empresa.setText(empresa)

        if " - " in endereco:
            uf, cidade = endereco.split(" - ")
            self.comboBox_estado.setCurrentText(uf)
            self.lineEdit_cidade.setText(cidade)
        else:
            self.comboBox_estado.setCurrentIndex(0)
            self.lineEdit_cidade.clear()

        self.hospede_selecionado = procura_hospede_completo(nome, empresa, telefone, endereco)

        self.lineEdit_busca.clear()
        self.lineEdit_busca.setPlaceholderText(nome)

    def salvar_alteracoes(self):
        self.label_error_nome.setText("")
        self.label_error_telefone.setText("")
        self.label_error_cidade.setText("")
        self.label_confirmacao.setText("")

        if not self.hospede_selecionado:
            return
        cpf = self.hospede_selecionado.cpf
        nome = formata_nome(self.lineEdit_nome.text())
        telefone = self.lineEdit_telefone.text()
        cidade = formata_nome(self.lineEdit_cidade.text())
        uf = self.comboBox_estado.currentText()
        endereco = f"{uf} - {cidade}"
        empresa = formata_nome(self.lineEdit_empresa.text())
        if empresa == "":
            empresa = "------"

        erro = False
        if not nome or len(nome) < 4:
            self.label_error_nome.setText("Nome Muito curto*")
            self.label_error_nome.setMinimumWidth(200)
            erro = True
        if not valida_telefone(telefone):
            self.label_error_telefone.setText("Telefone inválido*")
            self.label_error_telefone.setMinimumWidth(200)
            erro = True
        if not cidade:
            self.label_error_cidade.setText("Cidade obrigatória*")
            self.label_error_cidade.setMinimumWidth(200)
            erro = True

        if erro:
            return

        atualiza_hospede(cpf=cpf, nome=nome, telefone=telefone, endereco=endereco, empresa=empresa)

        self.label_confirmacao.setText("Dados atualizados com sucesso!")

        self.buscar_hospede()
        QTimer.singleShot(2000, self.limpar_campos)

    def limpar_campos(self):
        self.lineEdit_nome.clear()
        self.lineEdit_telefone.clear()
        self.lineEdit_cidade.clear()
        self.lineEdit_empresa.clear()
        self.comboBox_estado.setCurrentIndex(0)
        self.label_confirmacao.setText("")
        self.hospede_selecionado = None
    
    def _ajustar_altura_tabela(self):
        row_count = self.tabela_resultados.rowCount()
        if row_count == 0:
            self.tabela_resultados.setVisible(False)
            return
        row_height = self.tabela_resultados.verticalHeader().defaultSectionSize()
        header_height = self.tabela_resultados.horizontalHeader().height()
        scrollbar_height = self.tabela_resultados.horizontalScrollBar().height() if self.tabela_resultados.horizontalScrollBar().isVisible() else 0

        # Calcula a altura desejada com base no número de linhas
        desired_height = row_count * row_height + header_height + scrollbar_height + 2

        self.tabela_resultados.setMaximumHeight(desired_height)
        self.tabela_resultados.setVisible(True)
