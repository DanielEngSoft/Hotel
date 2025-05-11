from PySide6.QtCore import Qt, QDateTime, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox, QDateTimeEdit, QDateEdit, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem,
)
from operations.Ui.despesas_operations import buscar_despesas_por_id_hospedagem
from operations.Ui.quartos_operations import listar_quartos_disponiveis, quarto_por_id_hospedagem
from operations.Ui.hospedagem_operations import alterar_hospedagem

from styles.styles import style_botao_verde, tabelas

class Ui_page_alterar_hospedagem(QWidget):
    def __init__(self, hospedagem, parent=None):
        super().__init__(parent)
        self.hospedagem = hospedagem
        self.setObjectName("page_alterar")

        font = QFont()
        font.setPointSize(14)

        # Layout principal
        self.layout_principal = QVBoxLayout(self)

        # Criação do grupo de campos para a hospedagem
        self.groupBox = QGroupBox("Alterar dados da hospedagem", self)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setFixedSize(550, 400)

        self.layout_groupBox = QVBoxLayout(self.groupBox)
        self.formLayout = QFormLayout()

        # Label data de entrada
        self.label_data_entrada = QLabel("Data de entrada:")
        self.label_data_entrada.setFont(font)

        # Data de entrada input
        self.dateTimeEdit_entrada = QDateTimeEdit(hospedagem.data_entrada)
        self.dateTimeEdit_entrada.setFont(font)
        self.dateTimeEdit_entrada.setObjectName("dateTimeEdit_entrada")

        # Adicionar campos ao layout
        self.formLayout.addRow(self.label_data_entrada, self.dateTimeEdit_entrada)

        # Label data de saída
        self.label_data_saida = QLabel("Previsão de saída:")
        self.label_data_saida.setFont(font)

        # Data de saída input
        self.dateEdit_saida = QDateEdit(hospedagem.data_saida)
        self.dateEdit_saida.setFont(font)
        self.dateEdit_saida.setObjectName("dateTimeEdit_saida")

        # Adicionar campos ao layout
        self.formLayout.addRow(self.label_data_saida, self.dateEdit_saida)

        # Label quarto
        self.label_novo_quarto = QLabel("Número do quarto:")
        self.label_novo_quarto.setFont(font)

        # Tabela de quartos disponíveis
        self.tableWidget_quartos = QTableWidget()
        self.tableWidget_quartos.setColumnCount(2)
        self.tableWidget_quartos.setHorizontalHeaderLabels(["Nº", "Tipo"])
        self.tableWidget_quartos.setStyleSheet(tabelas())
        self.tableWidget_quartos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_quartos.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget_quartos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_quartos.setAlternatingRowColors(True)
        self.tableWidget_quartos.setMaximumHeight(200)
        self.tableWidget_quartos.setColumnWidth(0, 50)
        self.tableWidget_quartos.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_quartos.verticalHeader().setVisible(False)
        self.tableWidget_quartos.itemSelectionChanged.connect(self.on_quarto_selected)

        # Adicionar campos ao layout
        self.formLayout.addRow(self.label_novo_quarto, self.tableWidget_quartos)
        
        # Funçoes para atualizar a tabela de quartos disponíveis
        self.quartos = listar_quartos_disponiveis()
        self.update_quartos()

        # Adiciona FormLayout ao layout do grupo
        self.layout_groupBox.addLayout(self.formLayout)

        # Botão de alterar
        self.button_alterar = QPushButton("Alterar")
        self.button_alterar.setFont(font)
        self.button_alterar.setObjectName("button_confirmar")
        self.button_alterar.setStyleSheet(style_botao_verde())
        self.button_alterar.clicked.connect(self.button_alterar_clicked)

        # Adiciona botão ao layout do grupo
        self.layout_groupBox.addWidget(self.button_alterar)

        # Adiciona grupo ao layout principal
        self.layout_principal.addWidget(self.groupBox, alignment=Qt.AlignCenter)

        # Variáveis de controle para acesso às instâncias
        self.page_alterar_instance = None
        self.novo_quarto = None

    def set_page_hospedagem_instance(self, instance):
        self.page_alterar_instance = instance

    def button_alterar_clicked(self):
        self.quarto = quarto_por_id_hospedagem(self.hospedagem.id)
        if self.dateTimeEdit_entrada.dateTime().toPython().date() > self.dateEdit_saida.date().toPython():
            QMessageBox.warning(self, "Dados inválidos", "A data de entrada deve ser anterior à data de saída.")
            return
        
        # Define o mesmo quarto se nenhum tiver sido selecionado
        if not self.novo_quarto:
            self.novo_quarto = self.quarto.numero
        
        # Pega as novas datas da interface
        self.data_entrada = self.dateTimeEdit_entrada.dateTime().toPython()
        self.data_saida = self.dateEdit_saida.date().toPython()

        # Confirmação do usuário
        reply = QMessageBox.warning(
            self,
            "Atenção",
            "Deseja realmente alterar a hospedagem?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # Chama a função de alteração
                alterar_hospedagem(
                    id_hospedagem=self.hospedagem.id,
                    novo_quarto=self.novo_quarto,
                    data_entrada=self.data_entrada,
                    data_saida=self.data_saida
                )

                QMessageBox.information(self, "Sucesso", "Hospedagem alterada com sucesso!")

                # Fecha a janela de alteração, se existir
                if getattr(self, "page_alterar_instance", None):
                    self.page_alterar_instance.close()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao alterar hospedagem:\n{str(e)}")



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

    def on_quarto_selected(self):
        selected_items = self.tableWidget_quartos.selectedItems()
        if selected_items:
            numero = int(selected_items[0].text())
            for quarto in self.quartos:
                if quarto.numero == numero:
                    self.novo_quarto = quarto.numero
                    break