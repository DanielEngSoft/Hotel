from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, QLabel,
    QSpinBox, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout,
    QHeaderView, QCheckBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from operations.Ui.hospedes_operations import procura_hospedes_por_nome
from operations.Ui.quartos_operations import listar_quartos_disponiveis
from operations.Ui.produtos_operations import buscar_produto_por_id

DESCONTO = 0.10  # 10% de desconto

class Ui_page_abrir2(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("page_abrir2")
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(10)

        # GroupBox para formulário
        self.groupBox = QGroupBox("Abrir Hospedagem", self)
        self.groupBox.setObjectName("groupBox_abrir2")
        self.layout_groupBox = QVBoxLayout(self.groupBox)
        self.layout_groupBox.setContentsMargins(20, 20, 20, 20)
        self.layout_groupBox.setSpacing(10)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)

        font = QFont()
        font.setPointSize(10)

        # Campo para CPF
        self.lineEdit_cpf = QLineEdit(self.groupBox)
        self.lineEdit_cpf.setPlaceholderText("CPF do hóspede")
        self.lineEdit_cpf.setFont(font)
        self.form_layout.addRow(QLabel("CPF:", self.groupBox), self.lineEdit_cpf)

        # Label nome do hóspede
        self.label_nome = QLabel("", self.groupBox)
        self.label_nome.setFont(font)
        self.label_nome.setStyleSheet("color: blue; font-weight: bold;")
        self.form_layout.addRow(QLabel("Nome:", self.groupBox), self.label_nome)

        # Campo para buscar hóspede
        self.lineEdit_buscar = QLineEdit(self.groupBox)
        self.lineEdit_buscar.setPlaceholderText("Nome do hóspede")
        self.lineEdit_buscar.setFont(font)
        self.form_layout.addRow(QLabel("Buscar hóspede:", self.groupBox), self.lineEdit_buscar)

        # Campo de quantidade de hóspedes
        self.spinBox_qtd_hospedes = QSpinBox(self.groupBox)
        self.spinBox_qtd_hospedes.setFont(font)
        self.spinBox_qtd_hospedes.setMinimum(1)
        self.spinBox_qtd_hospedes.setMaximum(10)
        self.form_layout.addRow(QLabel("Quantidade de hóspedes:", self.groupBox), self.spinBox_qtd_hospedes)

        # Checkbox para desconto
        self.checkBox_desconto = QCheckBox("Desconto de 10%", self.groupBox)
        self.checkBox_desconto.setFont(font)
        self.form_layout.addRow(QLabel(""), self.checkBox_desconto)

        # Tabela de quartos
        self.tableWidget_quartos = QTableWidget(self.groupBox)
        self.tableWidget_quartos.setColumnCount(2)
        self.tableWidget_quartos.setHorizontalHeaderLabels(["Número", "Tipo"])
        self.tableWidget_quartos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_quartos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_quartos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_quartos.setFixedHeight(150)

        self.form_layout.addRow(QLabel("Quartos disponíveis:", self.groupBox), self.tableWidget_quartos)

        # Tabela de resultados de hóspedes
        self.tableWidget_hospedes = QTableWidget(self.groupBox)
        self.tableWidget_hospedes.setColumnCount(3)
        self.tableWidget_hospedes.setHorizontalHeaderLabels(["Nome", "Empresa", "CPF"])
        self.tableWidget_hospedes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_hospedes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_hospedes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_hospedes.setVisible(False)

        # Label para valor final
        self.label_preco = QLabel("R$ 0.00", self.groupBox)
        self.label_preco.setFont(font)
        self.form_layout.addRow(QLabel("Valor total:", self.groupBox), self.label_preco)

        # Botões
        self.botao_abrir = QPushButton("Abrir Hospedagem", self.groupBox)
        self.botao_limpar = QPushButton("Limpar Campos", self.groupBox)

        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(self.botao_abrir)
        layout_botoes.addWidget(self.botao_limpar)

        # Label de feedback
        self.label_feedback = QLabel("", self.groupBox)
        self.label_feedback.setStyleSheet("color: green")

        # Adiciona tudo ao layout do GroupBox
        self.layout_groupBox.addLayout(self.form_layout)
        self.layout_groupBox.addWidget(self.label_feedback)
        self.layout_groupBox.addLayout(layout_botoes)

        # Adiciona widgets à página
        self.layout_principal.addWidget(self.groupBox)
        self.layout_principal.addWidget(self.tableWidget_hospedes)

        # Conexões
        self.botao_limpar.clicked.connect(self.limpar_campos)
        self.lineEdit_buscar.textChanged.connect(self.search_hospedes)
        self.spinBox_qtd_hospedes.valueChanged.connect(self.atualizar_preco)
        self.checkBox_desconto.stateChanged.connect(self.atualizar_preco)
        self.tableWidget_hospedes.cellActivated.connect(self.pegar_cpf)

        self.carregar_quartos()

    def limpar_campos(self):
        self.lineEdit_cpf.clear()
        self.lineEdit_buscar.clear()
        self.label_nome.setText("")
        self.label_preco.setText("R$ 0.00")
        self.spinBox_qtd_hospedes.setValue(1)
        self.checkBox_desconto.setChecked(False)
        self.tableWidget_quartos.clearSelection()
        self.label_feedback.clear()

    def carregar_quartos(self):
        quartos = listar_quartos_disponiveis()
        self.tableWidget_quartos.setRowCount(0)
        for quarto in quartos:
            row = self.tableWidget_quartos.rowCount()
            self.tableWidget_quartos.insertRow(row)
            self.tableWidget_quartos.setItem(row, 0, QTableWidgetItem(str(quarto.numero)))
            self.tableWidget_quartos.setItem(row, 1, QTableWidgetItem(quarto.tipo))

    def search_hospedes(self):
        self.tableWidget_hospedes.setRowCount(0)
        nome = self.lineEdit_buscar.text()

        if nome.strip() == "":
            self.lineEdit_buscar.setPlaceholderText("Nome do hóspede")
            self.tableWidget_hospedes.setVisible(False)
            return

        hospedes = procura_hospedes_por_nome(nome)
        if hospedes:
            self.tableWidget_hospedes.setVisible(True)
            for hospede in hospedes:
                row = self.tableWidget_hospedes.rowCount()
                self.tableWidget_hospedes.insertRow(row)
                self.tableWidget_hospedes.setItem(row, 0, QTableWidgetItem(hospede.nome))
                self.tableWidget_hospedes.setItem(row, 1, QTableWidgetItem(hospede.empresa or ""))
                self.tableWidget_hospedes.setItem(row, 2, QTableWidgetItem(hospede.cpf))
        else:
            self.tableWidget_hospedes.setVisible(False)

    def pegar_cpf(self, row, column):
        cpf_item = self.tableWidget_hospedes.item(row, 2)
        nome_item = self.tableWidget_hospedes.item(row, 0)
        if cpf_item and nome_item:
            self.lineEdit_cpf.setText(cpf_item.text())
            self.label_nome.setText(nome_item.text())
            self.tableWidget_hospedes.setVisible(False)

    def atualizar_preco(self):
        qtd = self.spinBox_qtd_hospedes.value()
        produto = buscar_produto_por_id(qtd)
        if produto:
            valor = produto.valor
            if self.checkBox_desconto.isChecked():
                valor *= (1 - DESCONTO)
            self.label_preco.setText(f"R$ {valor:.2f}")
        else:
            self.label_preco.setText("R$ 0.00")
