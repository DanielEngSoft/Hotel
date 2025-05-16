from PySide6.QtCore import Qt, QDateTime, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox, QDateTimeEdit, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
)
from operations.Ui.despesas_operations import buscar_despesas_por_id_hospedagem, somar_despesas
from operations.Ui.hospedagem_operations import encerrar_hospedagem, somar_adiantamentos

from styles.styles import style_botao_vermelho

# Campo de entrada monetária customizado com formatação automática
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


class Ui_page_encerrar_hospedagem(QWidget):
    def __init__(self, hospedagem, parent=None):
        super().__init__(parent)
        self.hospedagem = hospedagem
        self.setObjectName("page_encerrar")

        font = QFont()
        font.setPointSize(14)

        self.groupBox = QGroupBox("Dados do encerramento", self)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setMaximumWidth(600)

        self.verticalLayout_groupBox = QVBoxLayout(self.groupBox)
        self.formLayout = QFormLayout()

        self.label_data = QLabel("Data de saída:")
        self.label_data.setFont(font)
        self.dateTimeEdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateTimeEdit.setFont(font)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_data)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.dateTimeEdit)

        self.label_total = QLabel("Total:")
        self.label_total.setFont(font)

        self.total = somar_despesas(self.hospedagem.id)

        self.lineEdit_total = QLineEdit(f"R$ {self.total:.2f}")
        self.lineEdit_total.setReadOnly(True)
        self.lineEdit_total.setFont(font)
        self.lineEdit_total.setObjectName("lineEdit_total")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_total)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_total)

        self.label_pagamento = QLabel("Método de pagamento:")
        self.label_pagamento.setFont(font)
        self.comboBox_pagamento = QComboBox()
        self.comboBox_pagamento.setFont(font)
        self.comboBox_pagamento.setObjectName("comboBox_pagamento")
        self.comboBox_pagamento.addItems(["Crédito", "Débito", "PIX", "Dinheiro", "Faturar"])
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_pagamento)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox_pagamento)

        self.label_recebido = QLabel("Valor recebido:")
        self.label_recebido.setFont(font)

        self.lineEdit_recebido = QLineEdit(f"R$ {self.total:.2f}")        
        self.lineEdit_recebido.setReadOnly(True)
        self.lineEdit_recebido.setFont(font)
        self.lineEdit_recebido.setObjectName("lineEdit_recebido")
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_recebido)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEdit_recebido)

        self.total_a_pagar = QLabel("Total a pagar:")
        self.total_a_pagar.setFont(font)
        self.lineEdit_a_pagar = LineEditMonetario(f'R$ {str(self.total)}0')
        self.lineEdit_a_pagar.setFont(font)
        self.lineEdit_a_pagar.setObjectName("lineEdit_a_pagar")
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.total_a_pagar)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.lineEdit_a_pagar)

        self.verticalLayout_groupBox.addLayout(self.formLayout)

        self.button_encerrar = QPushButton("Encerrar")
        self.button_encerrar.setFont(font)
        self.button_encerrar.setObjectName("button_encerrar")
        self.button_encerrar.setStyleSheet(style_botao_vermelho())
        self.button_encerrar.clicked.connect(self.button_encerrar_clicked)
        self.verticalLayout_groupBox.addWidget(self.button_encerrar)

        self.outer_layout = QVBoxLayout(self)
        self.inner_layout = QHBoxLayout()
        self.inner_layout.addStretch(1)
        self.inner_layout.addWidget(self.groupBox)
        self.inner_layout.addStretch(1)
        self.outer_layout.addLayout(self.inner_layout)

        self.page_hospedagem_instance = None

    def set_page_hospedagem_instance(self, instance):
        self.page_hospedagem_instance = instance

    def button_encerrar_clicked(self):
        reply = QMessageBox.warning(self, "Atenção", "Deseja realmente encerrar a hospedagem?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            encerrar_hospedagem(self.hospedagem.id)
            QMessageBox.information(self, "Sucesso", "Hospedagem encerrada com sucesso!")
            if self.page_hospedagem_instance:
                self.page_hospedagem_instance.close()

    def atualizar_informacoes(self):
        """Atualiza os dados da tela com base nas despesas da hospedagem."""
        self.total = somar_despesas(self.hospedagem.id) 
        self.recebido = somar_adiantamentos(self.hospedagem.id)
        self.a_pagar = self.total - self.recebido

        self.lineEdit_total.setText(f"R$ {self.total:.2f}")
        self.lineEdit_recebido.setText(f"R$ {self.recebido:.2f}")
        self.lineEdit_recebido.valor_cents = int(self.recebido * 100)
        self.lineEdit_a_pagar.setText(f"R$ {str(self.a_pagar)}0")

    def showEvent(self, event):
        self.atualizar_informacoes()
        super().showEvent(event)
