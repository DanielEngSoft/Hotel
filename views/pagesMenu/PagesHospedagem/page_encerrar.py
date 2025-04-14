from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox, QDateTimeEdit, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
)
from operations.Ui.despesas_operations import buscar_despesas_por_id_hospedagem
from operations.Ui.hospedagem_operations import encerrar_hospedagem


class Ui_page_encerrar(QWidget):
    def __init__(self, hospedagem, parent=None):
        super().__init__(parent)
        self.hospedagem = hospedagem
        self.setObjectName("page_encerrar")

        # Fonte padrão
        font = QFont()
        font.setPointSize(14)

        # --- GroupBox principal ---
        self.groupBox = QGroupBox("Dados do encerramento", self)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setMaximumWidth(600)

        self.verticalLayout_groupBox = QVBoxLayout(self.groupBox)

        # --- Formulário ---
        self.formLayout = QFormLayout()

        # Data de saída
        self.label_data = QLabel("Data de saída:")
        self.label_data.setFont(font)

        self.dateTimeEdit = QDateTimeEdit(QDateTime.currentDateTime())
        
        self.dateTimeEdit.setFont(font)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_data)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.dateTimeEdit)

        # Total
        self.label_total = QLabel("Total:")
        self.label_total.setFont(font)

        self.total = 0
        self.despesas = buscar_despesas_por_id_hospedagem(self.hospedagem.id)
        for despesa in self.despesas:
            self.total += despesa.valor

        self.lineEdit_total = QLineEdit(f"R$ {self.total:.2f}")
        self.lineEdit_total.setReadOnly(True)
        self.lineEdit_total.setFont(font)
        self.lineEdit_total.setObjectName("lineEdit_total")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_total)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_total)

        # Método de pagamento
        self.label_pagamento = QLabel("Método de pagamento:")
        self.label_pagamento.setFont(font)
        self.comboBox_pagamento = QComboBox()
        self.comboBox_pagamento.setFont(font)
        self.comboBox_pagamento.setObjectName("comboBox_pagamento")
        self.comboBox_pagamento.addItems(["Crédito", "Débito", "PIX", "Dinheiro", "Faturar"])
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_pagamento)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox_pagamento)

        # Valor recebido
        self.label_recebido = QLabel("Valor recebido:")
        self.label_recebido.setFont(font)
        self.lineEdit_recebido = QLineEdit()
        self.lineEdit_recebido.setFont(font)
        self.lineEdit_recebido.setObjectName("lineEdit_recebido")
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_recebido)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEdit_recebido)

        self.verticalLayout_groupBox.addLayout(self.formLayout)

        # Botão Encerrar
        self.button_encerrar = QPushButton("Encerrar")
        self.button_encerrar.setFont(font)
        self.button_encerrar.setObjectName("button_encerrar")
        self.button_encerrar.setStyleSheet(
            "background-color: rgb(170, 0, 0); color: black;"
        )
        self.button_encerrar.clicked.connect(self.set_button_encerrar_clicked)
        self.verticalLayout_groupBox.addWidget(self.button_encerrar)
        

        # --- Layout principal ---
        self.outer_layout = QVBoxLayout(self)  # Layout vertical principal da página
        self.inner_layout = QHBoxLayout()      # Layout horizontal para centralizar o groupBox
        self.inner_layout.addStretch(1)
        self.inner_layout.addWidget(self.groupBox)
        self.inner_layout.addStretch(1)

        self.outer_layout.addLayout(self.inner_layout)

    def set_button_encerrar_clicked(self):
        QMessageBox.warning(self, "Atenção", "Deseja realmente encerrar a hospedagem?", QMessageBox.Yes | QMessageBox.No)
        if QMessageBox.Yes:
            encerrar_hospedagem(self.hospedagem.id)
            QMessageBox.information(self, "Sucesso", "Hospedagem encerrada com sucesso!")
            

