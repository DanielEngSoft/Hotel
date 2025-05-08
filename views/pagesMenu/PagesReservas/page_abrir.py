from PySide6.QtCore import QDateTime, QTimer, QMetaObject, Qt, QSize
from PySide6.QtGui import QFont, QKeyEvent
from PySide6.QtWidgets import (QCheckBox, QDateTimeEdit, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel,QLineEdit, QPlainTextEdit, QPushButton,
    QSpinBox, QTableWidget, QTableWidgetItem,QVBoxLayout, QWidget, QHeaderView)

from styles.styles import style_botao_verde, tabelas
from operations.Ui.quartos_operations import listar_quartos_disponiveis, listar_quartos_por_data
from operations.Ui.produtos_operations import buscar_produto_por_id
from operations.Ui.hospedes_operations import procura_hospede_por_cpf, procura_hospedes_por_nome
from operations.Ui.reservas_operations import create_reserva
from operations.Ui.hospedagem_operations import diaria

# CONSTANTES
DESCONTO = 0.1  # 10% de desconto
LABEL_DESCONTO = int(DESCONTO * 100)

class Ui_page_abrir_reserva(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Inicializa a interface

    def setupUi(self, page_abrir):
        if not page_abrir.objectName():
            page_abrir.setObjectName("page_abrir")

        # Layout principal
        self.layout_principal = QHBoxLayout(page_abrir)
        self.layout_principal.setObjectName("layout_principal")
        self.layout_principal.setContentsMargins(0, 0, 0, 0)

        # Layout vertical principal
        self.layout_central = QVBoxLayout()
        self.layout_central.setObjectName("layout_central")
        self.layout_central.setContentsMargins(-1, 30, -1, -1)

        # Fonte padrão para o texto
        font = QFont()
        font.setPointSize(14)

        # Linha de busca
        self.lineEdit_buscar = QLineEdit(page_abrir)
        self.lineEdit_buscar.setObjectName("lineEdit_buscar")
        self.lineEdit_buscar.setPlaceholderText('Buscar hospede')
        self.lineEdit_buscar.textChanged.connect(self.search_hospedes)
        self.lineEdit_buscar.setFont(font)

        self.layout_central.addWidget(self.lineEdit_buscar)

        # Adicionar tabela de resultados de busca
        self.tableWidget_hospedes = QTableWidget(0, 3, page_abrir)
        self.tableWidget_hospedes.setHorizontalHeaderLabels(["Nome", "Empresa", "CPF"])
        self.tableWidget_hospedes.setStyleSheet(tabelas())
        self.tableWidget_hospedes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_hospedes.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget_hospedes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_hospedes.setAlternatingRowColors(True)
        self.tableWidget_hospedes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_hospedes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_hospedes.setVisible(False)
        self.tableWidget_hospedes.verticalHeader().setVisible(False)
        self.tableWidget_hospedes.cellActivated.connect(self.pegar_cpf)

        # Adicionar a tabela ao layout
        self.layout_central.addWidget(self.tableWidget_hospedes)

        # Grupo dos dados da reserva
        self.groupBox = QGroupBox(page_abrir)
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
        self.form_layout.setVerticalSpacing(9)
        
        # CPF Label
        self.label_cpf = QLabel("CPF:", self.groupBox)
        self.label_cpf.setFont(font)

        # CPF Input
        self.lineEdit_cpf = QLineEdit(self.groupBox)
        self.lineEdit_cpf.setInputMask("000.000.000-00;_")
        self.lineEdit_cpf.setPlaceholderText("000.000.000-00")
        self.lineEdit_cpf.setFont(font)
        self.lineEdit_cpf.setMaximumWidth(150)

        # Adiciona os widgets ao formulário
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

        # Data de entrada/saída
        self.label_datas = QLabel(self.groupBox)
        self.label_datas.setObjectName("dataDeEntradaLabel")
        self.label_datas.setText("Entrada/Saída:")
        self.label_datas.setFont(font)

        # Widget para seleção de data de entrada e de saída
        self.widget_datas = QWidget(self.groupBox)
        self.widget_datas.setObjectName("widget_datas")
        self.widget_datas.setFont(font)
        layout_datas = QHBoxLayout(self.widget_datas)
        layout_datas.setObjectName("layout_datas")
        layout_datas.setContentsMargins(0, 0, 0, 0)

        # Data de entrada Input
        self.dateTimeEdit_data_entrada = QDateTimeEdit(self.groupBox)
        self.dateTimeEdit_data_entrada.setObjectName("dataEtrada_DateTimeEdit")
        self.dateTimeEdit_data_entrada.setMaximumWidth(300)
        self.dateTimeEdit_data_entrada.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.dateTimeEdit_data_entrada.setCalendarPopup(True)
        self.dateTimeEdit_data_entrada.dateChanged.connect(self.update_quartos)
        self.dateTimeEdit_data_entrada.setFont(font)

        layout_datas.addWidget(self.dateTimeEdit_data_entrada)

        # Espaço entre os campos de entrada e saída
        label_entre_datas = QLabel('/', self.groupBox)
        label_entre_datas.setObjectName("label_entre_datas")

        layout_datas.addWidget(label_entre_datas)

        # Data de saida Input
        self.dateTimeEdit_data_saida = QDateTimeEdit(self.groupBox)
        self.dateTimeEdit_data_saida.setObjectName("dataSaidaDateTimeEdit")
        self.dateTimeEdit_data_saida.setMaximumWidth(300)
        self.dateTimeEdit_data_saida.setDateTime(QDateTime.currentDateTime().addDays(2))
        self.dateTimeEdit_data_saida.setCalendarPopup(True)
        self.dateTimeEdit_data_saida.dateChanged.connect(self.update_quartos)
        self.dateTimeEdit_data_saida.setFont(font)

        layout_datas.addWidget(self.dateTimeEdit_data_saida)

        # Adiciona os widgets ao formulário
        self.form_layout.addRow(self.label_datas, self.widget_datas)

        # Quantidade de pessoas Label
        self.qtd_pessoas_label = QLabel(self.groupBox)
        self.qtd_pessoas_label.setObjectName("quantidadeDePessoasLabel")
        self.qtd_pessoas_label.setText("Quantidade de pessoas:")
        self.qtd_pessoas_label.setFont(font)

        # Widget de SpinBox + Checkbox + Label de valor
        self.qtd_pessoas_widget = QWidget(self.groupBox)
        self.qtd_pessoas_widget.setObjectName("quantidadeDePessoasWidget")
        self.qtd_pessoas_widget.setMaximumWidth(400)
        self.qtd_pessoas_widget.setFont(font)

        # Layout horizontal do Widget
        self.horizontalLayout = QHBoxLayout(self.qtd_pessoas_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("verticalLayout_4")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        # Spinbox qtd pessoas
        self.spinBox = QSpinBox(page_abrir)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.setFont(font)
        self.spinBox.setValue(1)
        self.spinBox.valueChanged.connect(self.atualizar_preco)

        self.horizontalLayout.addWidget(self.spinBox)

        # Checkbox desconto
        self.checkBox = QCheckBox(page_abrir)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setFont(font)
        self.checkBox.setText('Desconto')
        self.checkBox.stateChanged.connect(self.atualizar_preco)

        self.horizontalLayout.addWidget(self.checkBox)

        # Valor da diária
        self.label = QLabel(page_abrir)
        self.label.setObjectName("label")
        self.label.setText("R$ 100,00")
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        # Adiciona os widgets ao formulário
        self.form_layout.addRow(self.qtd_pessoas_label, self.qtd_pessoas_widget)

        # Adiantamento
        self.adiantamentoLabel = QLabel(self.groupBox)
        self.adiantamentoLabel.setObjectName("adiantamentoLabel")
        self.adiantamentoLabel.setText("Adiantamento:")
        self.adiantamentoLabel.setFont(font)

        self.adiantamentoLineEdit = LineEditMonetario(f'R$ 0.00')
        self.adiantamentoLineEdit.setObjectName("adiantamentoLineEdit")
        self.adiantamentoLineEdit.setFont(font)

        self.form_layout.addRow(self.adiantamentoLabel, self.adiantamentoLineEdit)

        # Acompanhantes Label
        self.acompanhantes_label = QLabel(self.groupBox)
        self.acompanhantes_label.setObjectName("acompanhantes_label")
        self.acompanhantes_label.setText("Acompanhantes:")
        self.acompanhantes_label.setFont(font)

        # Acompanhantes Input
        self.acompanhantes_plainTextEdit = QPlainTextEdit(page_abrir)
        self.acompanhantes_plainTextEdit.setObjectName("acompanhantes_plainTextEdit")
        self.acompanhantes_plainTextEdit.setMaximumHeight(90)

        # Adiciona os widgets ao formulário
        self.form_layout.addRow(self.acompanhantes_label, self.acompanhantes_plainTextEdit)

        # Quartos
        self.label_quartos = QLabel(self.groupBox)
        self.label_quartos.setObjectName("quartosLabel")
        self.label_quartos.setText(f"Selecione o quarto: ")
        self.label_quartos.setFont(font)

        # Tabela de quartos disponíveis
        self.tableWidget_quartos = QTableWidget(0, 2, page_abrir)
        self.tableWidget_quartos.setStyleSheet(tabelas())
        self.tableWidget_quartos.setAlternatingRowColors(True)
        self.tableWidget_quartos.setMaximumHeight(150)
        self.tableWidget_quartos.setColumnWidth(0, 50)
        self.tableWidget_quartos.setHorizontalHeaderLabels(["Nº", "Tipo"])
        self.tableWidget_quartos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_quartos.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget_quartos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_quartos.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_quartos.verticalHeader().setVisible(False)
        self.tableWidget_quartos.currentCellChanged.connect(self.selecionar_quarto)
        
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
        self.plainTextEdit_obs.setMaximumHeight(90)

        # Adiciona os widgets ao formulário
        self.form_layout.addRow(self.label_obs, self.plainTextEdit_obs)

        # Adiciona o layout do Form ao layout do groupbox
        self.layout_groupBox.addLayout(self.form_layout)

        # Adiciona o groupbox ao layout principal
        self.layout_central.addWidget(self.groupBox)

        # Label de feedback
        self.label_feedback = QLabel(page_abrir)
        self.label_feedback.setObjectName("label_feedback")
        self.label_feedback.setFont(font)
        self.label_feedback.setAlignment(Qt.AlignCenter)
        self.label_feedback.setVisible(False)

        self.layout_central.addWidget(self.label_feedback)

        # Botão "Abrir reserva"
        self.pushButton_abrir = QPushButton(page_abrir)
        self.pushButton_abrir.setObjectName("pushButton")
        self.pushButton_abrir.setText("Abrir reserva")
        self.pushButton_abrir.setFont(font)
        self.pushButton_abrir.setStyleSheet(style_botao_verde())
        self.pushButton_abrir.clicked.connect(self.abrir_reserva)

        self.layout_central.addWidget(self.pushButton_abrir)
        self.layout_central.addStretch()

        self.layout_principal.addStretch()
        self.layout_principal.addLayout(self.layout_central)
        self.layout_principal.addStretch()

        QMetaObject.connectSlotsByName(page_abrir)

    def pegar_cpf(self, row):
        cpf = self.tableWidget_hospedes.item(row, 2).text()
        self.lineEdit_cpf.setText(cpf)
        self.tableWidget_hospedes.setVisible(False)
        self.lineEdit_buscar.setText("")
        self.dateTimeEdit_data_entrada.setFocus()

    def atualizar_preco(self):
        qtd = self.spinBox.value()
        if self.checkBox.isChecked():
            preco = diaria(qtd) * (1 - DESCONTO)
        else:
            preco = diaria(qtd)
        self.label.setText(f"R$ {preco:.2f}")

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

    def selecionar_quarto(self, row, col):
        item = self.tableWidget_quartos.item(row, 0)
        if item is not None:
            quarto = item.text()
        else:
            quarto = ''
        self.label_quartos.setText(f"Selecione o quarto: {quarto}")

    def update_quartos(self):
        data_entrada = self.dateTimeEdit_data_entrada.date().toPython()
        data_saida = self.dateTimeEdit_data_saida.date().toPython()

        self.tableWidget_quartos.setRowCount(0)
        quartos = listar_quartos_por_data(data_entrada, data_saida)

        if not quartos:
            self.label_quartos.setText("Não há quartos disponíveis para a data selecionada.")
            return
        
        for quarto in quartos:
            row = self.tableWidget_quartos.rowCount()
            self.tableWidget_quartos.insertRow(row)
            
            item_num = QTableWidgetItem(str(quarto.numero))
            item_num.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_quartos.setItem(row, 0, item_num)

            item_tipo = QTableWidgetItem(quarto.tipo)
            item_tipo.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_quartos.setItem(row, 1, item_tipo)

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
        self.tableWidget_hospedes.setVisible(True)

    def abrir_reserva(self):
        row = self.tableWidget_quartos.currentRow()
        cpf = self.lineEdit_cpf.text()

        if row == -1 or len(cpf) != 14:
            self.label_feedback.setVisible(True)
            self.label_feedback.setText("Selecione um quarto e preencha o CPF.")
            self.label_feedback.setStyleSheet("color: red;")
            return

        id_hospede = procura_hospede_por_cpf(cpf)
        id_quarto = self.tableWidget_quartos.item(row, 0).text()
        data_entrada = self.dateTimeEdit_data_entrada.date().toPython()
        data_saida = self.dateTimeEdit_data_saida.date().toPython()
        qtd_hospedes = self.spinBox.value()
        acompanhantes = self.acompanhantes_plainTextEdit.toPlainText()
        obs = self.plainTextEdit_obs.toPlainText().strip()

        # Verifica se o hóspede existe no banco de dados
        if not id_hospede:
            self.label_feedback.setVisible(True)
            self.label_feedback.setText("Hóspede não encontrado.")
            self.label_feedback.setStyleSheet("color: red;")
            return
            
        produto = buscar_produto_por_id(qtd_hospedes)
        valor_diaria = produto.valor

        # Adicionar condições em caso do checkBox estiver marcado
        if self.checkBox.isChecked():
            valor_diaria = produto.valor * (1 - DESCONTO)
        
        create_reserva(
            id_hospede=cpf,
            id_quarto=id_quarto,
            data_entrada=data_entrada,
            data_saida=data_saida,
            qtd_hospedes=qtd_hospedes,
            acompanhantes=acompanhantes,
            valor_diaria=valor_diaria,
            adiantamento=0,
            obs=obs,
        )
        self.label_feedback.setVisible(True)
        self.label_feedback.setText(f"Reserva criada para {id_hospede.nome}")
        self.label_feedback.setStyleSheet("color: green;")
        self.limpar_campos()

    def limpar_campos(self):
        self.lineEdit_cpf.clear()
        self.dateTimeEdit_data_entrada.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.dateTimeEdit_data_saida.setDateTime(QDateTime.currentDateTime().addDays(2))
        self.spinBox.setValue(1)
        self.acompanhantes_plainTextEdit.clear()
        self.plainTextEdit_obs.clear()
        self.checkBox.setChecked(False)
        self.groupBox.setTitle("")
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.limpar_campos()

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