# ui_page_abrir.py

# ====== IMPORTAÇÕES ======
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

# ====== CLASSE PRINCIPAL DA PÁGINA ABRIR HOSPEDAGEM ======
class Ui_page_abrir(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)  # Inicializa a interface

    # ====== CONFIGURAÇÃO DA INTERFACE ======
    def setupUi(self, page_abrir):
        # Define nome do objeto, se ainda não tiver
        if not page_abrir.objectName():
            page_abrir.setObjectName("page_abrir")

        layout = QHBoxLayout(self)

        self.widget = QWidget(page_abrir)
        layout.addWidget(self.widget)

        # Layout horizontal principal com margens
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setPointSize(14)

        # ====== LADO ESQUERDO (ABERTURA DE HOSPEDAGEM) ======
        self.verticalLayout_abrir = QVBoxLayout()

        # Layout para o formulário
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(20)

        # CPF----------------------------------------------------
        self.layout_cpf = QHBoxLayout()
        
        self.label_cpf = QLabel("CPF:", self.widget)
        self.label_cpf.setFont(font)

        self.lineEdit_cpf = QLineEdit(self.widget)
        self.lineEdit_cpf.setInputMask("000.000.000-00;_")
        self.lineEdit_cpf.setPlaceholderText("000.000.000-00")
        self.lineEdit_cpf.setFont(font)
        self.lineEdit_cpf.setMinimumSize(150, 0)
        self.lineEdit_cpf.setMaximumSize(150, 16777215)
        self.layout_cpf.addWidget(self.lineEdit_cpf)

        self.label_nome = QLabel("", self.widget)
        self.label_nome.setFont(font)
        self.layout_cpf.addWidget(self.label_nome)

        self.form_layout.addRow(self.label_cpf, self.layout_cpf)

        # Evento para posicionar cursor no início do campo CPF
        def cpf_focus_in_event(event):
            QLineEdit.focusInEvent(self.lineEdit_cpf, event)
            QTimer.singleShot(0, lambda: self.lineEdit_cpf.setCursorPosition(0))

        # Atualiza o label do CPF com o nome do hóspede (se encontrado)
        def update_cpf_label():
            cpf = self.lineEdit_cpf.text()
            if len(cpf) == 14:
                hospede = procura_hospede_por_cpf(cpf)
                self.label_nome.setText(f"{hospede.nome}" if hospede else "Nenhum encontrado")

        self.lineEdit_cpf.focusInEvent = cpf_focus_in_event
        self.lineEdit_cpf.textChanged.connect(update_cpf_label)
        self.lineEdit_cpf.editingFinished.connect(update_cpf_label)

        # Quantidade de hóspedes + Preço
        qtd_price_layout = QHBoxLayout()
        self.label_qtd_hospedes = QLabel("Quantidade de hóspedes:", self.widget)
        self.label_qtd_hospedes.setFont(font)

        self.spinBox_qtd_hospedes = QSpinBox(self.widget)
        self.spinBox_qtd_hospedes.setFont(font)
        self.spinBox_qtd_hospedes.setMaximumWidth(80)
        self.spinBox_qtd_hospedes.setRange(1, 10)
        self.spinBox_qtd_hospedes.setValue(1)
        qtd_price_layout.addWidget(self.spinBox_qtd_hospedes)

        self.label_preco = QLabel("R$ 100", self.widget)
        self.label_preco.setFont(font)
        self.label_preco.setMaximumWidth(80)
        self.label_preco.setStyleSheet("color: green; font-weight: bold;")
        qtd_price_layout.addWidget(self.label_preco)

        self.checkBox_desconto = QCheckBox("Desconto", self.widget)
        self.checkBox_desconto.setFont(font)
        self.checkBox_desconto.clicked.connect(self.atualizar_preco)
        qtd_price_layout.addWidget(self.checkBox_desconto)
        qtd_price_layout.addStretch()

        self.form_layout.addRow(self.label_qtd_hospedes, qtd_price_layout)
        self.spinBox_qtd_hospedes.valueChanged.connect(self.atualizar_preco)

        # Previsão de saída
        self.label_prev_saida = QLabel("Previsão de saída:", self.widget)
        self.label_prev_saida.setFont(font)

        self.dateEdit_prev_saida = QDateEdit(QDate.currentDate(), self.widget)
        self.dateEdit_prev_saida.setMaximumWidth(150)
        self.dateEdit_prev_saida.setFont(font)
        self.form_layout.addRow(self.label_prev_saida, self.dateEdit_prev_saida)

        # Quantidade de quartos disponíveis
        self.label_total_quartos = QLabel("Selecione o quarto:", self.widget)
        self.label_total_quartos.setFont(font)

        # Tabela de quartos disponíveis
        self.tableWidget_quartos = QTableWidget(0, 2, self.widget)
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
        self.form_layout.addRow(self.label_total_quartos, self.tableWidget_quartos)

        self.verticalLayout_abrir.addLayout(self.form_layout) 
        self.update_quartos()

        # Feedback de mensagens (erro/sucesso)
        self.label_feedback = QLabel("", self.widget)
        self.label_feedback.setFont(font)
        self.label_feedback.setAlignment(Qt.AlignCenter)
        self.verticalLayout_abrir.addWidget(self.label_feedback)

        self.verticalLayout_abrir.addStretch()

        # Botão abrir hospedagem
        self.pushButton_abrir = QPushButton("Abrir", self.widget)
        self.pushButton_abrir.setFont(font)
        self.pushButton_abrir.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_abrir.setMinimumWidth(500)
        self.pushButton_abrir.setStyleSheet(style_botao_verde())
        self.pushButton_abrir.clicked.connect(self.button_abrir_clicked)

        abrir_layout = QHBoxLayout()
        abrir_layout.addStretch()
        abrir_layout.addWidget(self.pushButton_abrir)
        abrir_layout.addStretch()
        self.verticalLayout_abrir.addLayout(abrir_layout)

        # Adiciona layout do lado esquerdo na tela
        self.horizontalLayout.addLayout(self.verticalLayout_abrir)

        # Linha separadora entre colunas
        self.line_separador = QFrame(self.widget)
        self.line_separador.setFrameShape(QFrame.VLine)
        self.line_separador.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout.addWidget(self.line_separador)

        # ============================================= LADO DIREITO (BUSCA DE HÓSPEDES) ==============================================
        self.verticalLayout_buscar = QVBoxLayout()

        # Título e linha separadora
        self.label_buscar = QLabel("Buscar", self.widget)
        self.label_buscar.setFont(font)
        self.label_buscar.setAlignment(Qt.AlignCenter)
        self.verticalLayout_buscar.addWidget(self.label_buscar)

        self.line_separador_busca = QFrame(self.widget)
        self.line_separador_busca.setFrameShape(QFrame.HLine)
        self.line_separador_busca.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_buscar.addWidget(self.line_separador_busca)

        # Campo de busca por nome
        self.lineEdit_nome = QLineEdit(self.widget)
        self.lineEdit_nome.setPlaceholderText("Nome do hóspede")
        self.lineEdit_nome.setFont(font)
        self.lineEdit_nome.textChanged.connect(self.search_hospedes)
        self.verticalLayout_buscar.addWidget(self.lineEdit_nome)

        # Tabela de hóspedes encontrados
        self.tableWidget_hospedes = QTableWidget(0, 3, self.widget)
        self.tableWidget_hospedes.setHorizontalHeaderLabels(["Nome", "Empresa", "CPF"])
        self.tableWidget_hospedes.setStyleSheet(tabelas())
        self.tableWidget_hospedes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_hospedes.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget_hospedes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_hospedes.setAlternatingRowColors(True)
        self.tableWidget_hospedes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_hospedes.setVisible(False)
        self.tableWidget_hospedes.verticalHeader().setVisible(False)
        self.verticalLayout_buscar.addWidget(self.tableWidget_hospedes)

        self.tableWidget_hospedes.cellClicked.connect(self.pegar_cpf)

        # Espaçamento final
        self.verticalLayout_buscar.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Adiciona layout do lado direito na tela
        self.horizontalLayout.addLayout(self.verticalLayout_buscar)

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
        self.label_feedback.setStyleSheet("")

        if row == -1 or len(cpf) != 14:
            self.label_feedback.setText("Selecione um quarto e preencha o CPF.")
            self.label_feedback.setStyleSheet("color: red;")
            return

        quarto_num = self.tableWidget_quartos.item(row, 0).text()
        qtd_hospedes = self.spinBox_qtd_hospedes.value()
        data_saida = self.dateEdit_prev_saida.date().toPython()

        # Verifica se o hóspede existe no banco de dados
        hospede = procura_hospede_por_cpf(cpf)
        if not hospede:
            self.label_feedback.setText("Hóspede não encontrado.")
            self.label_feedback.setStyleSheet("color: red;")
            return
            
        produto = buscar_produto_por_id(qtd_hospedes)
        valor_diaria = produto.valor

        # Adicionar condições em caso do checkBox estiver marcado
        if self.checkBox_desconto.isChecked():
            valor_diaria = produto.valor * (1 - DESCONTO)
        
        # Cria a hospedagem no banco de dados
        create_hospedagem(cpf, quarto_num, data_saida, qtd_hospedes, valor_diaria=valor_diaria) # vALOR DA DIÁRIA = VALOR DO PRODUTO
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
        nome = self.lineEdit_nome.text()
        
        if self.lineEdit_nome.text() == "":
            self.lineEdit_nome.setPlaceholderText("Nome do hóspede")
            self.tableWidget_hospedes.setVisible(False)

        hospedes = procura_hospedes_por_nome(nome)
        if hospedes:
            if self.lineEdit_nome.text() == "":
                self.lineEdit_nome.setPlaceholderText("Nome do hóspede")
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
        self.lineEdit_cpf.setText(cpf)
        self.lineEdit_cpf.setFocus()

    # Atualiza o preço de acordo com a quantidade de hóspedes
    def atualizar_preco(self, qtd_hospedes):
        preco = diaria(qtd_hospedes)
        if self.checkBox_desconto.isChecked():
            preco = preco * (1 - DESCONTO)
        self.label_preco.setText(f"R$ {preco}")
    
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

    def limpar_campos(self):
        self.lineEdit_cpf.setText("..-")
        self.dateEdit_prev_saida.setDate(QDate.currentDate())
        self.spinBox_qtd_hospedes.setValue(1)
        self.atualizar_preco(1)
        self.update_quartos()
        self.checkBox_desconto.setChecked(False)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.limpar_campos()
