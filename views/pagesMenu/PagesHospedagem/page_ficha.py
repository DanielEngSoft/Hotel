# Imports necessários do PySide6 e operações personalizadas
from PySide6.QtCore import Qt, QTimer, QDateTime, QEvent
from PySide6.QtGui import QFont, QKeyEvent, QColor
from PySide6.QtWidgets import (
    QAbstractItemView, QDateTimeEdit, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QSpacerItem, QSizePolicy, QFrame, QLineEdit, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem
)

from operations.Ui.produtos_operations import buscar_produto_por_nome
from operations.Ui.hospedagem_operations import somar_adiantamentos, adiantamentos_hospedagem
from operations.Ui.despesas_operations import buscar_despesas_por_id_hospedagem, create_despesa
from styles.styles import tabelas, style_botao_verde


# Constante para valor inicial monetário
VALOR_ZERO = "R$ 0,00"

# Campo de entrada monetária customizado com formatação automática
class LineEditMonetario(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setText(VALOR_ZERO)
        self.valor_cents = 0
        self.textEdited.connect(self.formatar_valor_monetario)

    # Garante que o cursor vá pro final ao focar no campo
    def focusInEvent(self, event):
        super().focusInEvent(event)
        QTimer.singleShot(0, lambda: self.setCursorPosition(len(self.text())))

    # Formata o texto digitado como valor monetário (R$ X,XX)
    def formatar_valor_monetario(self, _):
        texto = self.text()
        apenas_numeros = ''.join(filter(str.isdigit, texto))
        self.valor_cents = int(apenas_numeros) if apenas_numeros else 0

        reais = self.valor_cents // 100
        centavos = self.valor_cents % 100
        texto_formatado = f"R$ {reais},{centavos:02d}"

        self.blockSignals(True)
        self.setText(texto_formatado)
        self.blockSignals(False)
        self.setCursorPosition(len(texto_formatado))

    # Retorna o valor atual como float (em reais)
    def get_valor_float(self):
        return self.valor_cents / 100.0

# Janela principal de visualização da hospedagem
class Ui_page_ficha(QWidget):
    def __init__(self, hospedagem, parent=None):
        super().__init__(parent)
        self.hospedagem = hospedagem

        # Fontes utilizadas
        font_title = QFont()
        font_title.setPointSize(14)
        font_content = QFont()
        font_content.setPointSize(10)

        main_layout = QVBoxLayout(self)

        # Container da ficha da hospedagem
        group_box = QGroupBox("Ficha da Hospedagem")
        group_box.setGeometry(10, 10, 600, 450)
        group_box.setFont(font_content)
        group_layout = QVBoxLayout(group_box)

        # Layout com campos para adicionar nova despesa
        input_layout = QHBoxLayout()
        self.input_descricao = QLineEdit()
        self.input_descricao.setPlaceholderText("Descrição do produto")
        self.input_descricao.installEventFilter(self)
        input_layout.addWidget(self.input_descricao)
        
        self.input_valor = LineEditMonetario()
        self.input_valor.setMaximumWidth(100)
        input_layout.addWidget(self.input_valor)

        self.input_quantidade = QSpinBox()
        self.input_quantidade.setMinimum(1)
        input_layout.addWidget(self.input_quantidade)

        self.input_data = QDateTimeEdit(QDateTime.currentDateTime())
        self.input_data.setMaximumWidth(150)
        input_layout.addWidget(self.input_data)

        self.btn_adicionar = QPushButton("Adicionar")
        self.btn_adicionar.setStyleSheet(style_botao_verde())
        self.btn_adicionar.setFocusPolicy(Qt.StrongFocus)
        self.btn_adicionar.setDefault(True)

        input_layout.addWidget(self.btn_adicionar)

        group_layout.addLayout(input_layout)

        # Tabela de sugestões com base na descrição
        self.tabela_sugestoes = QTableWidget(0, 2)
        self.tabela_sugestoes.setStyleSheet(tabelas())
        self.tabela_sugestoes.setHorizontalHeaderLabels(["Preço", "Descrição"])
        self.tabela_sugestoes.setVisible(False)
        self.tabela_sugestoes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela_sugestoes.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela_sugestoes.verticalHeader().setVisible(False)
        self.tabela_sugestoes.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tabela_sugestoes.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabela_sugestoes.horizontalHeader().setMaximumHeight(25)
        group_layout.addWidget(self.tabela_sugestoes)

        # Conexões dos sinais com as ações
        self.produto_selecionado = None
        self.input_descricao.textChanged.connect(self.atualizar_sugestoes)
        self.tabela_sugestoes.cellActivated.connect(self.selecionar_sugestao)
        self.btn_adicionar.clicked.connect(self.adicionar_despesa)

        # Tabela que exibe as despesas
        self.tabela = QTableWidget(0, 5)
        self.tabela.setHorizontalHeaderLabels(["Data", "Descrição", "QTD", "Valor", "TOTAL"])
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setAlternatingRowColors(True)

        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        group_layout.addWidget(self.tabela)

        # Rodapé com totais
        totals_layout = QHBoxLayout()
        self.label_diarias = QLabel("  Diárias: R$0,00")
        self.label_diarias.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label_diarias.setFont(font_title)
        totals_layout.addWidget(self.label_diarias)

        self.label_despesas = QLabel("Despesas: R$0,00")
        self.label_despesas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_despesas.setFont(font_title)
        totals_layout.addWidget(self.label_despesas)

        self.label_pagamentos = QLabel("Pagamentos: R$0,00")
        self.label_pagamentos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_pagamentos.setFont(font_title)
        totals_layout.addWidget(self.label_pagamentos)

        self.label_total = QLabel("Total: R$0,00  ")
        self.label_total.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.label_total.setFont(font_title)
        totals_layout.addWidget(self.label_total)

        group_layout.addLayout(totals_layout)
        main_layout.addWidget(group_box)

        # Atalhos exibidos no fim da janela
        self.label_atalhos = QLabel("[ + ] Aumenta  |  [ - ] Diminui  |  [Del] Exclui  |  [F6] Alterar  |  [F5] Encerrar")
        self.label_atalhos.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_atalhos)

        # Carrega as despesas já registradas no banco
        self.carregar_despesas()

    # Atualiza a lista de sugestões conforme a descrição digitada
    def atualizar_sugestoes(self, texto):
        self.tabela_sugestoes.setRowCount(0)
        if not texto.strip():
            self.tabela_sugestoes.setVisible(False)
            return

        resultados = buscar_produto_por_nome(texto)
        if not resultados:
            self.tabela_sugestoes.setVisible(False)
            return

        self.tabela_sugestoes.setRowCount(len(resultados))
        for row, produto in enumerate(resultados):
            descricao_item = QTableWidgetItem(produto.descricao)
            valor_item = QTableWidgetItem(f"R${produto.valor:.2f}")
            descricao_item.setData(Qt.ItemDataRole.UserRole, produto)

            self.tabela_sugestoes.setItem(row, 0, valor_item)
            self.tabela_sugestoes.setItem(row, 1, descricao_item)

        self._ajustar_altura_tabela_sugestao()
        self.tabela_sugestoes.setVisible(True)

    # Preenche os campos ao selecionar uma sugestão
    def selecionar_sugestao(self, row, column):
        item = self.tabela_sugestoes.item(row, 1)  # Coluna 1 contém a descrição com o produto associado
        if not item:
            return

        produto = item.data(Qt.ItemDataRole.UserRole)
        self.produto_selecionado = produto
        self.input_descricao.setText(produto.descricao)
        self.input_valor.valor_cents = int(produto.valor * 100)
        reais = self.input_valor.valor_cents // 100
        centavos = self.input_valor.valor_cents % 100
        texto_formatado = f"R$ {reais},{centavos:02d}"

        self.input_valor.blockSignals(True)
        self.input_valor.setText(texto_formatado)
        self.input_valor.blockSignals(False)
        self.input_valor.setCursorPosition(len(texto_formatado))

        self.tabela_sugestoes.setVisible(False)
        self.btn_adicionar.setFocus()
        
    # Adiciona uma nova despesa à tabela e ao banco
    def adicionar_despesa(self):
        produto = self.produto_selecionado
        if not produto:
            return

        quantidade = self.input_quantidade.value()
        valor_digitado = self.input_valor.get_valor_float()
        data = self.input_data.dateTime().toPython()

        create_despesa(
            id_hospedagem=self.hospedagem.id,
            id_produto=produto.id,
            quantidade=quantidade,
            valor_produto=valor_digitado,
            data=data
        )

        # Limpa campos após inserção
        self.input_descricao.clear()
        self.input_valor.setText(VALOR_ZERO)
        self.input_valor.valor_cents = 0
        self.input_quantidade.setValue(1)
        self.produto_selecionado = None
        self.tabela_sugestoes.setVisible(False)

        self.atualizar_totais()
        self.carregar_despesas()

    # Atualiza os totais de despesas, diárias e valor total
    def atualizar_totais(self):
        total_despesas = 0.0
        valor_pagamentos = somar_adiantamentos(self.hospedagem.id)
        for row in range(1, self.tabela.rowCount()):
            item_total = self.tabela.item(row, 4)
            if item_total:
                valor = float(item_total.text().replace("R$", "").replace(",", "."))
                total_despesas += valor

        self.label_despesas.setText(f"Despesas: R${total_despesas:.2f}")
        despesas = buscar_despesas_por_id_hospedagem(self.hospedagem.id)
        if despesas:
            valor_diarias = despesas[0].valor
        else:
            valor_diarias = 0.0

        self.label_diarias.setText(f"  Diárias: R${valor_diarias:.2f}")
        self.label_pagamentos.setText(f"Pagamentos: R${valor_pagamentos:.2f}")
        self.label_total.setText(f"Total: R${valor_diarias + total_despesas - valor_pagamentos}0  ")


    # Carrega despesas da hospedagem e insere na tabela
    def carregar_despesas(self):
        self.tabela.setRowCount(0)
        despesas = buscar_despesas_por_id_hospedagem(self.hospedagem.id)
        pagamentos = adiantamentos_hospedagem(self.hospedagem.id)

        for despesa in despesas:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            data_formatada = despesa.data.strftime("%d/%m/%Y %H:%M")
            descricao = despesa.produto.descricao
            self.tabela.setItem(row, 0, QTableWidgetItem(data_formatada))
            self.tabela.setItem(row, 1, QTableWidgetItem(descricao))
            self.tabela.setItem(row, 2, QTableWidgetItem(str(despesa.quantidade)))
            self.tabela.setItem(row, 3, QTableWidgetItem(f"R${despesa.valor_produto:.2f}"))
            self.tabela.setItem(row, 4, QTableWidgetItem(f"R${despesa.valor:.2f}"))
        
        # Adiciona pagamentos na tabela
        for pagamento in pagamentos:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            data_formatada = pagamento.data.strftime("%d/%m/%Y %H:%M")
            descricao = pagamento.descricao
            self.tabela.setItem(row, 0, QTableWidgetItem(data_formatada))
            self.tabela.setItem(row, 1, QTableWidgetItem(descricao))
            self.tabela.setItem(row, 2, QTableWidgetItem(str(pagamento.metodo_pagamento)))
            self.tabela.setItem(row, 3, QTableWidgetItem(f"R${pagamento.valor:.2f}"))

        #  Deixa verde as linhas de pagamentos
        for row in range(self.tabela.rowCount()):
            item_total = self.tabela.item(row, 4)
            if not item_total:
                for col in range(5):
                    item = self.tabela.item(row, col)
                    if item:
                        item.setBackground(QColor("#05452f"))
        self.atualizar_totais()
    
    def _ajustar_altura_tabela_sugestao(self):
        row_count = self.tabela_sugestoes.rowCount()
        if row_count == 0:
            self.tabela_sugestoes.setVisible(False)
            return
        row_height = self.tabela_sugestoes.verticalHeader().defaultSectionSize()
        header_height = self.tabela_sugestoes.horizontalHeader().height()
        scrollbar_height = self.tabela_sugestoes.horizontalScrollBar().height() if self.tabela_sugestoes.horizontalScrollBar().isVisible() else 0

        # Calcula a altura desejada com base no número de linhas
        desired_height = row_count * row_height + header_height + scrollbar_height + 2

        if desired_height > 150:
            self.tabela_sugestoes.setMaximumHeight(150)
        else:
            self.tabela_sugestoes.setMaximumHeight(desired_height)
        self.tabela_sugestoes.setVisible(True)
        
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Down:
            self.tabela_sugestoes.setFocus()
            self.tabela_sugestoes.setCurrentCell(0, 0)
        if event.key() == Qt.Key_Escape:
            self.input_descricao.setFocus()
            self.input_descricao.clear()
            