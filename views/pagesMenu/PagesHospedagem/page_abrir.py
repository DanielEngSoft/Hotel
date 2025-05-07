from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# Modelos e operações do sistema
from operations.Ui.hospedagem_operations import create_hospedagem, buscar_hospedagem_por_quarto, diaria
from operations.Ui.hospedes_operations import procura_hospede_por_cpf, procura_hospedes_por_nome
from operations.Ui.quartos_operations import listar_quartos_disponiveis
from operations.Ui.despesas_operations import create_despesa
from operations.Ui.produtos_operations import buscar_produto_por_id
from datetime import datetime

# Estilo personalizado
from styles.styles import style_botao_verde, tabelas

# CONSTANTES
DESCONTO = 0.1  # 10% de desconto
LABEL_DESCONTO = int(DESCONTO * 100)

# ====== CLASSE PRINCIPAL DA PÁGINA ABRIR HOSPEDAGEM ======
class Ui_page_abrir(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Inicializa a interface

    def setupUi(self, page_abrir):
        if not page_abrir.objectName():
            page_abrir.setObjectName("page_abrir")

        # Layout principal 
        self.layout_principal = QHBoxLayout(page_abrir)
        self.layout_principal.setObjectName("layout_principal")

        # Layout vertical principal
        self.layout_central = QVBoxLayout()
        self.layout_central.setObjectName(u"layout_central")
        self.layout_central.setContentsMargins(0, 10, 0, 0)

        # Fonte padrão para o texto
        font = QFont()
        font.setPointSize(14)

        # Layout Horizontal para a barra de busca e botão de cadastrar
        self.layout_buscar = QHBoxLayout()

        # Linha de busca + btn cadastrar
        self.lineEdit_buscar = QLineEdit(page_abrir)
        self.lineEdit_buscar.setObjectName("lineEdit_buscar")
        self.lineEdit_buscar.setPlaceholderText("Buscar hóspede")
        self.lineEdit_buscar.textChanged.connect(self.search_hospedes)
        self.lineEdit_buscar.setFont(font)

        self.pushButton_Cadastrar = QPushButton(page_abrir)
        self.pushButton_Cadastrar.setObjectName("pushButton_Cadastrar")
        self.pushButton_Cadastrar.setFont(font)
        self.pushButton_Cadastrar.setStyleSheet(style_botao_verde())
        self.pushButton_Cadastrar.setText("Cadastrar")

        self.layout_buscar.addWidget(self.lineEdit_buscar)
        self.layout_buscar.addWidget(self.pushButton_Cadastrar)

        self.layout_central.addLayout(self.layout_buscar)
        # Adicionar tabela de resultados de busca
        self.tableWidget_hospedes = QTableWidget(0, 3, page_abrir)
        self.tableWidget_hospedes.setStyleSheet(tabelas())
        self.tableWidget_hospedes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_hospedes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_hospedes.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget_hospedes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_hospedes.verticalHeader().setVisible(False)
        self.tableWidget_hospedes.setAlternatingRowColors(True)
        self.tableWidget_hospedes.setVisible(False)
        self.tableWidget_hospedes.setHorizontalHeaderLabels(["Nome", "Empresa", "CPF"])
        # Adicionar a tabela ao layout
        self.layout_central.addWidget(self.tableWidget_hospedes)

        self.tableWidget_hospedes.cellActivated.connect(self.pegar_cpf)

        # Grupo dos dados da reserva
        self.groupBox = QGroupBox(page_abrir)
        self.groupBox.setMaximumWidth(550)
        self.groupBox.setMaximumHeight(700)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(Qt.AlignCenter)

        # Layout vertical do grupo
        self.layout_groupBox = QVBoxLayout(self.groupBox)
        self.layout_groupBox.setObjectName("verticalLayout")
        self.layout_groupBox.setContentsMargins(30, 30, 30, 30)

        # Formulário
        self.form_layout = QFormLayout()
        self.form_layout.setObjectName("formLayout")
        self.form_layout.setHorizontalSpacing(35)
        self.form_layout.setVerticalSpacing(10)

        # CPF Label
        self.label_cpf = QLabel("CPF:", self.groupBox)
        self.label_cpf.setFont(font)

        # CPF Input
        self.lineEdit_cpf = QLineEdit(self.groupBox)
        self.lineEdit_cpf.setInputMask("000.000.000-00;_")
        self.lineEdit_cpf.setPlaceholderText("000.000.000-00")
        self.lineEdit_cpf.setFont(font)
        self.lineEdit_cpf.setMinimumSize(150, 0)
        self.lineEdit_cpf.setMaximumSize(150, 16777215)

        # Adicionar o campo CPF ao formulário
        self.form_layout.addRow(self.label_cpf, self.lineEdit_cpf)

        # Evento para posicionar cursor no início do campo CPF
        def cpf_focus_in_event(event):
            QLineEdit.focusInEvent(self.lineEdit_cpf, event)
            QTimer.singleShot(0, lambda: self.lineEdit_cpf.setCursorPosition(0))

        # Atualiza o label do CPF com o nome do hóspede (se encontrado)
        def update_cpf_label():
            cpf = self.lineEdit_cpf.text()
            if len(cpf) == 14:
                hospede = procura_hospede_por_cpf(cpf)
                self.groupBox.setTitle(f"{hospede.nome}" if hospede else "Nenhum encontrado")

        # Chamada das funções de atualização do label do CPF 
        self.lineEdit_cpf.focusInEvent = cpf_focus_in_event
        self.lineEdit_cpf.textChanged.connect(update_cpf_label)
        self.lineEdit_cpf.editingFinished.connect(update_cpf_label)

        # Data de saida Label
        self.dataSaida_label = QLabel(self.groupBox)
        self.dataSaida_label.setObjectName("dataSaida")
        self.dataSaida_label.setText("Data de saída:")
        self.dataSaida_label.setFont(font)

        # Data de saida Input
        self.dataSaida_DateTimeEdit = QDateTimeEdit(self.groupBox)
        self.dataSaida_DateTimeEdit.setObjectName("dataSaidaDateTimeEdit")
        self.dataSaida_DateTimeEdit.setMaximumSize(QSize(300, 16777215))
        self.dataSaida_DateTimeEdit.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.dataSaida_DateTimeEdit.setFont(font)

        # Adiciona os widgets ao formulário
        self.form_layout.addRow(self.dataSaida_label, self.dataSaida_DateTimeEdit)
        
        # Quantidade de pessoas Label
        self.qtd_pessoas_label = QLabel(self.groupBox)
        self.qtd_pessoas_label.setObjectName("quantidadeDePessoasLabel")
        self.qtd_pessoas_label.setText("Quantidade de pessoas:")
        self.qtd_pessoas_label.setFont(font)

        # Widget de SpinBox + Checkbox + Label de valor
        self.qtd_pessoas_widget = QWidget(self.groupBox)
        self.qtd_pessoas_widget.setObjectName("quantidadeDePessoasWidget")
        self.qtd_pessoas_widget.setMinimumSize(QSize(0, 30))
        self.qtd_pessoas_widget.setMaximumSize(QSize(16777215, 50))
        self.qtd_pessoas_widget.setFont(font)

        # Layout horizontal do Widget
        self.horizontalLayout = QHBoxLayout(self.qtd_pessoas_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("verticalLayout_4")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        # Spinbox qtd pessoas
        self.spinBox = QSpinBox(page_abrir)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMinimumWidth(30)
        self.spinBox.setRange(1, 10)
        self.spinBox.setValue(1)
        self.spinBox.setFont(font)
        self.spinBox.valueChanged.connect(self.atualizar_preco)

        self.horizontalLayout.addWidget(self.spinBox)

        # Checkbox desconto
        self.checkBox = QCheckBox(page_abrir)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setFont(font)
        self.checkBox.setText(f'- {LABEL_DESCONTO}% ')
        self.checkBox.stateChanged.connect(self.atualizar_preco)

        self.horizontalLayout.addWidget(self.checkBox)

        # Valor da diária
        self.label = QLabel(page_abrir)
        self.label.setText("R$ 100.00")
        self.label.setObjectName("label")
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.form_layout.addRow(self.qtd_pessoas_label, self.qtd_pessoas_widget)

        # Acompanhantes Label
        self.acompanhantes_label = QLabel(self.groupBox)
        self.acompanhantes_label.setObjectName("acompanhantes_label")
        self.acompanhantes_label.setText("Acompanhantes:")
        self.acompanhantes_label.setFont(font)

        # Acompanhantes Input
        self.acompanhantes_plainTextEdit = QPlainTextEdit(page_abrir)
        self.acompanhantes_plainTextEdit.setObjectName("acompanhantes_plainTextEdit")
        self.acompanhantes_plainTextEdit.setMaximumSize(QSize(300, 90))

        # Adiciona os widgets ao formulário
        self.form_layout.addRow(self.acompanhantes_label, self.acompanhantes_plainTextEdit)

        # Quantidade de quartos disponíveis
        self.label_quartos = QLabel("Selecione o quarto:", self.groupBox)
        self.label_quartos.setFont(font)

        # Tabela de quartos disponíveis
        self.tableWidget_quartos = QTableWidget(0, 2, self.groupBox)
        self.tableWidget_quartos.setHorizontalHeaderLabels(["Nº", "Tipo"])
        self.tableWidget_quartos.setStyleSheet(tabelas())
        self.tableWidget_quartos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_quartos.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget_quartos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_quartos.setAlternatingRowColors(True)
        self.tableWidget_quartos.setMinimumHeight(200)
        self.tableWidget_quartos.setColumnWidth(0, 50)
        self.tableWidget_quartos.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_quartos.verticalHeader().setVisible(False)
        self.tableWidget_quartos.currentCellChanged.connect(self.selecionar_quarto)

        # Adiciona os widgets ao formulário
        self.form_layout.addRow(self.label_quartos, self.tableWidget_quartos)
        self.update_quartos()

        # Observações Label
        self.label_obs = QLabel(self.groupBox)
        self.label_obs.setObjectName("ObsLabel")
        self.label_obs.setText("Observações:")
        self.label_obs.setFont(font)

        # Observações Input
        self.plainTextEdit_obs = QPlainTextEdit(page_abrir)
        self.plainTextEdit_obs.setObjectName("plainTextEdit")
        self.plainTextEdit_obs.setMaximumSize(QSize(300, 100))

        # Adiciona os widgets ao formulário
        self.form_layout.addRow(self.label_obs, self.plainTextEdit_obs)
        
        # Adiciona o layout do Form ao layout do groupbox
        self.layout_groupBox.addLayout(self.form_layout) 
        
        # Adiciona o groupbox ao layout principal
        self.layout_central.addWidget(self.groupBox)

        # Feedback de mensagens (erro/sucesso)
        self.label_feedback = QLabel("", page_abrir)
        self.label_feedback.setFont(font)
        self.label_feedback.setAlignment(Qt.AlignCenter)
        self.layout_central.addWidget(self.label_feedback)


        # Botão abrir hospedagem
        self.pushButton_abrir = QPushButton("Abrir", page_abrir)
        self.pushButton_abrir.setFont(font)
        self.pushButton_abrir.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_abrir.setMinimumWidth(500)
        self.pushButton_abrir.setStyleSheet(style_botao_verde())
        self.pushButton_abrir.clicked.connect(self.button_abrir_clicked)

        self.abrir_layout = QHBoxLayout()
        self.abrir_layout.addStretch()
        self.abrir_layout.addWidget(self.pushButton_abrir)
        self.abrir_layout.addStretch()

        self.layout_central.addLayout(self.abrir_layout)
        self.layout_central.addStretch()

        self.layout_principal.addStretch()
        self.layout_principal.addLayout(self.layout_central)
        self.layout_principal.addStretch()

        QMetaObject.connectSlotsByName(page_abrir)

    # Atualiza a tabela de quartos disponíveis
    def showEvent(self, event):
        self.update_quartos()
        super().showEvent(event)

    def update_quartos(self):
        self.tableWidget_quartos.setRowCount(0)
        quartos = listar_quartos_disponiveis()
        for quarto in quartos:
            row = self.tableWidget_quartos.rowCount()
            self.tableWidget_quartos.insertRow(row)
            item_num = QTableWidgetItem(str(quarto.numero))
            item_num.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_quartos.setItem(row, 0, item_num)
            self.tableWidget_quartos.setItem(row, 1, QTableWidgetItem(quarto.tipo))


    # Lógica ao clicar no botão "Abrir"
    def button_abrir_clicked(self):
        row = self.tableWidget_quartos.currentRow()
        cpf = self.lineEdit_cpf.text()

        self.label_feedback.setText("")

        if row == -1 or len(cpf) != 14:
            self.label_feedback.setText("Selecione um quarto e preencha o CPF.")
            self.label_feedback.setStyleSheet("color: red;")
            return

        quarto_num = self.tableWidget_quartos.item(row, 0).text()
        qtd_hospedes = self.spinBox.value()
        data_saida = self.dataSaida_DateTimeEdit.date().toPython()
        obs = self.plainTextEdit_obs.toPlainText().strip()
        acompanhantes = self.acompanhantes_plainTextEdit.toPlainText()

        # Verifica se o hóspede existe no banco de dados
        hospede = procura_hospede_por_cpf(cpf)
        if not hospede:
            self.label_feedback.setText("Hóspede não encontrado.")
            self.label_feedback.setStyleSheet("color: red;")
            return
            
        produto = buscar_produto_por_id(qtd_hospedes)
        valor_diaria = produto.valor

        # Adicionar condições em caso do checkBox estiver marcado
        if self.checkBox.isChecked():
            valor_diaria = produto.valor * (1 - DESCONTO)
        
        # Cria a hospedagem no banco de dados
        create_hospedagem(id_hospede=cpf, id_quarto=quarto_num, data_saida=data_saida, qtd_hospedes=qtd_hospedes, valor_diaria=valor_diaria, obs=obs, acompanhantes=acompanhantes) # vALOR DA DIÁRIA = VALOR DO PRODUTO
        self.label_feedback.setText(f"Hospedagem criada para {hospede.nome}")
        self.label_feedback.setStyleSheet("color: green;")

        hospedagem = buscar_hospedagem_por_quarto(quarto_num)

        # Adicionando a despesa de Diária no hospede, de acordo com a quantidade de hóspedes. 
        # Considerando que os produtos das diárias foram criados de acordo com o arquvo de OBSERVAÇÕES.txt
        create_despesa(
            id_hospedagem=hospedagem.id,
            id_produto=qtd_hospedes,  # Despesas de diárias tem o id do produto igual à quantidade de hóspedes
            quantidade=1,  # Quantidade de diárias
            valor_produto=valor_diaria,  # Valor da diária
        )
        # Limpa os campos após sucesso
        self.limpar_campos()

        QTimer.singleShot(4000, lambda: self.label_feedback.setText(""))

    # Busca hóspedes por nome e preenche a tabela
    def search_hospedes(self):
        self.tableWidget_hospedes.setRowCount(0)
        nome = self.lineEdit_buscar.text()
        
        if self.lineEdit_buscar.text() == "":
            self.lineEdit_buscar.setPlaceholderText("Nome do hóspede")
            self.tableWidget_hospedes.setVisible(False)

        hospedes = procura_hospedes_por_nome(nome)
        if hospedes:
            if self.lineEdit_buscar.text() == "":
                self.lineEdit_buscar.setPlaceholderText("Nome do hóspede")
                self.tableWidget_hospedes.setVisible(False)
            else:
                self.tableWidget_hospedes.setVisible(True)
                for hospede in hospedes:
                    row = self.tableWidget_hospedes.rowCount()
                    self.tableWidget_hospedes.insertRow(row)
                    self.tableWidget_hospedes.setItem(row, 0, QTableWidgetItem(hospede.nome))
                    self.tableWidget_hospedes.setItem(row, 1, QTableWidgetItem(hospede.empresa))
                    self.tableWidget_hospedes.setItem(row, 2, QTableWidgetItem(hospede.cpf))
        self._ajustar_altura_tabela()

    # Preenche o campo CPF ao clicar em um hóspede da lista
    def pegar_cpf(self, row):
        cpf = self.tableWidget_hospedes.item(row, 2).text()
        self.lineEdit_buscar.clear()
        self.lineEdit_cpf.setText(cpf)
        self.dataSaida_DateTimeEdit.setFocus()
        self.tableWidget_hospedes.setVisible(False)

    # Atualiza o preço de acordo com a quantidade de hóspedes
    def atualizar_preco(self):
        qtd = self.spinBox.value()
        if self.checkBox.isChecked():
            preco = diaria(qtd) * (1 - DESCONTO)
        else:
            preco = diaria(qtd)
        self.label.setText(f"R$ {preco:.2f}")
    
    def _ajustar_altura_tabela(self):
        row_count = self.tableWidget_hospedes.rowCount()
        if row_count == 0:
            self.tableWidget_hospedes.setVisible(False)
            return
        row_height = self.tableWidget_hospedes.verticalHeader().defaultSectionSize()
        header_height = self.tableWidget_hospedes.horizontalHeader().height()
        scrollbar_height = self.tableWidget_hospedes.horizontalScrollBar().height() if self.tableWidget_hospedes.horizontalScrollBar().isVisible() else 0

        # Calcula a altura desejada com base no número de linhas
        desired_height = row_count * row_height + header_height + scrollbar_height + 2

        self.tableWidget_hospedes.setMaximumHeight(desired_height)
        self.tableWidget_hospedes.setMinimumHeight(desired_height)
        if desired_height > 250:
            self.tableWidget_hospedes.setMaximumHeight(250)
        self.tableWidget_hospedes.setVisible(True)

    def limpar_campos(self):
        self.lineEdit_cpf.setText("..-")
        self.dataSaida_DateTimeEdit.setDate(QDate.currentDate())
        self.groupBox.setTitle("")
        self.lineEdit_buscar.setText("")
        self.spinBox.setValue(1)
        self.checkBox.setChecked(False)
        self.label.setText("R$ 100.00")
        self.update_quartos()

    def selecionar_quarto(self, row, col):
        item = self.tableWidget_quartos.item(row, 0)
        if item is not None:
            quarto = item.text()
        else:
            quarto = ''
        self.label_quartos.setText(f"Selecione o quarto: [{quarto}]")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.limpar_campos()
