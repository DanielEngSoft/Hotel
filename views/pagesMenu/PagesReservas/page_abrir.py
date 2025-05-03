

from PySide6.QtCore import QDateTime, QTimer, QMetaObject, Qt, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QCheckBox, QDateTimeEdit, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel,QLineEdit, QPlainTextEdit, QPushButton,
    QSpinBox, QTableWidget, QTableWidgetItem,QVBoxLayout, QWidget, QHeaderView)

from styles.styles import style_botao_verde, tabelas
from operations.Ui.quartos_operations import listar_quartos_disponiveis
from operations.Ui.hospedes_operations import procura_hospede_por_cpf, procura_hospedes_por_nome

class Ui_page_abrir(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Inicializa a interface

    def setupUi(self, page_abrir):
        if not page_abrir.objectName():
            page_abrir.setObjectName(u"page_abrir")
        page_abrir.resize(881, 722)

        # Configurando layout principal com margens
        self.layout_principal = QHBoxLayout(page_abrir)
        self.layout_principal.setObjectName(u"layout_principal")

        self.layout_buscar_groupbox = QVBoxLayout()
        self.layout_buscar_groupbox.setObjectName(u"verticalLayout_5")
        self.layout_buscar_groupbox.setContentsMargins(-1, 30, -1, -1)

        font = QFont()
        font.setPointSize(14)

        self.lineEdit_buscar = QLineEdit(page_abrir)
        self.lineEdit_buscar.setPlaceholderText('Buscar hospede')
        self.lineEdit_buscar.setObjectName(u"lineEdit")
        self.lineEdit_buscar.textChanged.connect(self.search_hospedes)
        self.lineEdit_buscar.setFont(font)

        self.layout_buscar_groupbox.addWidget(self.lineEdit_buscar)

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
        # Adicionar a tabela ao layout
        self.layout_buscar_groupbox.addWidget(self.tableWidget_hospedes)

        self.tableWidget_hospedes.cellActivated.connect(self.pegar_cpf)

        # Grupo dos dados da reserva
        self.groupBox = QGroupBox(page_abrir)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(Qt.AlignCenter)

        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)

        self.form_layout = QFormLayout()
        self.form_layout.setObjectName(u"formLayout")
        self.form_layout.setHorizontalSpacing(35)
        self.form_layout.setVerticalSpacing(20)
        
        self.label_cpf = QLabel("CPF:", self.groupBox)
        self.label_cpf.setFont(font)

        self.lineEdit_cpf = QLineEdit(self.groupBox)
        self.lineEdit_cpf.setInputMask("000.000.000-00;_")
        self.lineEdit_cpf.setPlaceholderText("000.000.000-00")
        self.lineEdit_cpf.setFont(font)
        self.lineEdit_cpf.setMinimumSize(150, 0)
        self.lineEdit_cpf.setMaximumSize(150, 25)

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
            else:
                self.groupBox.setTitle("")

        self.lineEdit_cpf.focusInEvent = cpf_focus_in_event
        self.lineEdit_cpf.textChanged.connect(update_cpf_label)
        self.lineEdit_cpf.editingFinished.connect(update_cpf_label)

        # Data de entrada
        self.dataEntrada_label = QLabel(self.groupBox)
        self.dataEntrada_label.setObjectName(u"dataDeEntradaLabel")
        self.dataEntrada_label.setText("Data de entrada:")
        self.dataEntrada_label.setFont(font)

        self.form_layout.setWidget(1, QFormLayout.LabelRole, self.dataEntrada_label)

        self.dataEtrada_DateTimeEdit = QDateTimeEdit(self.groupBox)
        self.dataEtrada_DateTimeEdit.setObjectName(u"dataEtrada_DateTimeEdit")
        self.dataEtrada_DateTimeEdit.setMaximumSize(QSize(300, 16777215))
        self.dataEtrada_DateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.dataEtrada_DateTimeEdit.setFont(font)

        self.form_layout.setWidget(1, QFormLayout.FieldRole, self.dataEtrada_DateTimeEdit)

        # Data de saida
        self.dataSaida_label = QLabel(self.groupBox)
        self.dataSaida_label.setObjectName(u"dataSaida")
        self.dataSaida_label.setText("Data de saída:")
        self.dataSaida_label.setFont(font)

        self.form_layout.setWidget(2, QFormLayout.LabelRole, self.dataSaida_label)

        self.dataSaidaDateTimeEdit = QDateTimeEdit(self.groupBox)
        self.dataSaidaDateTimeEdit.setObjectName(u"dataSaidaDateTimeEdit")
        self.dataSaidaDateTimeEdit.setMaximumSize(QSize(300, 16777215))
        self.dataSaidaDateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.dataSaidaDateTimeEdit.setFont(font)

        self.form_layout.setWidget(2, QFormLayout.FieldRole, self.dataSaidaDateTimeEdit)

        # Quantidade de pessoas(label e spinbox)
        self.quantidadeDePessoasLabel = QLabel(self.groupBox)
        self.quantidadeDePessoasLabel.setObjectName(u"quantidadeDePessoasLabel")
        self.quantidadeDePessoasLabel.setText("Quantidade de pessoas:")
        self.quantidadeDePessoasLabel.setFont(font)

        self.form_layout.setWidget(3, QFormLayout.LabelRole, self.quantidadeDePessoasLabel)

        self.quantidadeDePessoasWidget = QWidget(self.groupBox)
        self.quantidadeDePessoasWidget.setObjectName(u"quantidadeDePessoasWidget")
        self.quantidadeDePessoasWidget.setMinimumSize(QSize(0, 30))
        self.quantidadeDePessoasWidget.setMaximumSize(QSize(16777215, 50))
        self.quantidadeDePessoasWidget.setFont(font)

        self.verticalLayout_4 = QVBoxLayout(self.quantidadeDePessoasWidget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.widget = QWidget(self.quantidadeDePessoasWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 25))
        self.widget.setMaximumSize(QSize(300, 16777215))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.spinBox = QSpinBox(self.widget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(0, 25))
        self.spinBox.setFont(font)

        self.horizontalLayout.addWidget(self.spinBox)

        self.checkBox = QCheckBox(self.widget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setFont(font)
        self.checkBox.setText('Desconto')

        self.horizontalLayout.addWidget(self.checkBox)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        # Arrumar depois
        self.label.setText("R$ 100,00")
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_4.addWidget(self.widget)

        self.form_layout.setWidget(3, QFormLayout.FieldRole, self.quantidadeDePessoasWidget)

        # Adiantamento
        self.adiantamentoLabel = QLabel(self.groupBox)
        self.adiantamentoLabel.setObjectName(u"adiantamentoLabel")
        self.adiantamentoLabel.setText("Adiantamento:")
        self.adiantamentoLabel.setFont(font)

        self.adiantamentoLineEdit = LineEditMonetario(f'R$ 0.00')
        self.adiantamentoLineEdit.setObjectName(u"adiantamentoLineEdit")
        self.adiantamentoLineEdit.setFont(font)

        self.form_layout.addRow(self.adiantamentoLabel, self.adiantamentoLineEdit)

        # Quartos
        self.quartosLabel = QLabel(self.groupBox)
        self.quartosLabel.setObjectName(u"quartosLabel")
        self.quartosLabel.setText(f"Selecione o quarto: ")
        self.quartosLabel.setFont(font)

        # Tabela de quartos disponíveis
        self.tableWidget_quartos = QTableWidget(0, 2, self.widget)
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
        
        self.form_layout.addRow(self.quartosLabel, self.tableWidget_quartos)
        self.update_quartos()

        # Observações
        self.ObsLabel = QLabel(self.groupBox)
        self.ObsLabel.setObjectName(u"ObsLabel")
        self.ObsLabel.setText("Observações:")
        self.ObsLabel.setFont(font)

        self.plainTextEdit = QPlainTextEdit(self.widget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMaximumSize(QSize(300, 100))

        self.form_layout.addRow(self.ObsLabel, self.plainTextEdit)

        # Adiciona o layout do Form ao layout principal
        self.verticalLayout.addLayout(self.form_layout)

        self.layout_buscar_groupbox.addWidget(self.groupBox)

        # Botão "Abrir reserva"
        self.pushButton = QPushButton(page_abrir)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setText("Abrir reserva")
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(style_botao_verde())

        self.layout_buscar_groupbox.addWidget(self.pushButton)
        self.layout_buscar_groupbox.addStretch()

        self.layout_principal.addStretch()
        self.layout_principal.addLayout(self.layout_buscar_groupbox)
        self.layout_principal.addStretch()

        QMetaObject.connectSlotsByName(page_abrir)

    def pegar_cpf(self, row):
        cpf = self.tableWidget_hospedes.item(row, 2).text()
        self.lineEdit_cpf.setText(cpf)
        self.tableWidget_hospedes.setVisible(False)
        self.lineEdit_buscar.setText("")

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
        self.quartosLabel.setText(f"Selecione o quarto: {quarto}")

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