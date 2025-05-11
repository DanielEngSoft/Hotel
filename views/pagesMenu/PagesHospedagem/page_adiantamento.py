# Janela de Adiantamento, não é uma pagina, é uma janela que abre ao clicar no botão "Adiantamento"

from PySide6.QtCore import QDateTime, QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox, QDateTimeEdit, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
)
from operations.Ui.despesas_operations import somar_despesas
from operations.Ui.hospedagem_operations import adicionar_adiantamento, somar_adiantamentos

from styles.styles import style_botao_verde

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


class Ui_page_adiantamento_hospedagem(QWidget):
    def __init__(self, hospedagem, parent=None):
        super().__init__(parent)
        self.hospedagem = hospedagem
        self.setObjectName("page_adiantamento")

        font = QFont()
        font.setPointSize(14)
        self.total = 0

        self.layout_principal = QVBoxLayout(self)

        # Grupo de campos de entrada
        self.groupBox = QGroupBox("Dados do pagamento", self)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setFixedSize(450, 350)

        self.layout_groupBox = QVBoxLayout(self.groupBox)
        self.formLayout = QFormLayout()

        # Data Label
        self.label_data = QLabel("Data:")
        self.label_data.setFont(font)

        # Data Input
        self.dateTimeEdit_data = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateTimeEdit_data.setFont(font)
        self.dateTimeEdit_data.setObjectName("dateTimeEdit")

        # Adicionar campos ao layout
        self.formLayout.addRow(self.label_data, self.dateTimeEdit_data)

        # Pagamento Label
        self.label_pagamento = QLabel("Método de pagamento:")
        self.label_pagamento.setFont(font)

        # Pagamento Input
        self.comboBox_pagamento = QComboBox()
        self.comboBox_pagamento.setFont(font)
        self.comboBox_pagamento.setObjectName("comboBox_pagamento")
        self.comboBox_pagamento.addItems(["Crédito", "Débito", "PIX", "Dinheiro", "Faturar"])

        # Adicionar campos ao layout
        self.formLayout.addRow(self.label_pagamento, self.comboBox_pagamento)

        # Valor recebido Label
        self.label_recebido = QLabel("Valor recebido:")
        self.label_recebido.setFont(font)

        # Valor recebido Input
        self.lineEdit_recebido = LineEditMonetario(f'R$ 0.00')
        self.lineEdit_recebido.setFont(font)
        self.lineEdit_recebido.setObjectName("lineEdit_recebido")

        # Adicionar campos ao layout
        self.formLayout.addRow(self.label_recebido, self.lineEdit_recebido)

        # Descrição Label
        self.label_descricao = QLabel("Descrição:")
        self.label_descricao.setFont(font)

        # Descrição Input
        self.lineEdit_descricao = QLineEdit('PAGAMENTO')
        self.lineEdit_descricao.setFont(font)
        self.lineEdit_descricao.setObjectName("lineEdit_descricao")

        # Adicionar campos ao layout
        self.formLayout.addRow(self.label_descricao, self.lineEdit_descricao)

        # Adicionar formLayout ao layout_groupBox
        self.layout_groupBox.addLayout(self.formLayout)

        # Botão "Adicionar"
        self.button_adicionar = QPushButton("Adicionar")
        self.button_adicionar.setFont(font)
        self.button_adicionar.setObjectName("button_encerrar")
        self.button_adicionar.setStyleSheet(style_botao_verde())
        self.button_adicionar.clicked.connect(self.button_adicionar_clicked)

        # Adicionar botão ao layout
        self.layout_groupBox.addWidget(self.button_adicionar)

        self.layout_principal.addWidget(self.groupBox, alignment=Qt.AlignCenter)
        self.page_hospedagem_instance = None

    # Função para definir a instância da página de hospedagem
    def set_page_hospedagem_instance(self, instance):
        self.page_hospedagem_instance = instance

    # Função para adicionar o pagamento
    def button_adicionar_clicked(self):
        data = self.dateTimeEdit_data.dateTime().toPython()
        descricao = self.lineEdit_descricao.text()
        metodo_pagamento = self.comboBox_pagamento.currentText()
        valor = self.lineEdit_recebido.get_valor_float()

        if valor > 0:
            reply = QMessageBox.warning(self, "Atenção", "Deseja realmente incluir esse pagamento", QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                adicionar_adiantamento(data, self.hospedagem.id, valor, descricao, metodo_pagamento)
                QMessageBox.information(self, "Sucesso", "Pagamento adicionado com sucesso!")
                if self.page_hospedagem_instance:
                    self.page_hospedagem_instance.close()

    # Função para atualizar as informações
    def atualizar_informacoes(self):
        """Atualiza os dados da tela com base nas despesas da hospedagem."""
        self.total = somar_despesas(self.hospedagem.id) - somar_adiantamentos(self.hospedagem.id)

        if self.total > 0:
            self.lineEdit_recebido.setText(f"R$ {self.total:.2f}")
            self.lineEdit_recebido.valor_cents = int(self.total * 100)
        else:
            self.lineEdit_recebido.setText("R$ 0.00")
            self.lineEdit_recebido.valor_cents = 0

    # Função para atualizar as informações
    def showEvent(self, event):
        self.atualizar_informacoes()
        super().showEvent(event)
