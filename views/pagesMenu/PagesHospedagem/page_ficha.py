# Imports necessários do PySide6 e operações personalizadas
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QSpacerItem, QSizePolicy, QFrame, QLineEdit, QSpinBox,
    QPushButton, QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem
)

from operations.Ui.produtos_operations import buscar_produto_por_nome
from operations.Ui.despesas_operations import buscar_despesas_por_id_hospedagem, create_despesa

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
        self.setWindowTitle(f"Hospedagem - Quarto {getattr(hospedagem.quarto, 'numero', 'Desconhecido')}")
        self.hospedagem = hospedagem
        self.setGeometry(100, 100, 800, 600)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # Fontes utilizadas
        font_title = QFont()
        font_title.setPointSize(14)
        font_content = QFont()
        font_content.setPointSize(10)

        main_layout = QVBoxLayout(self)

        # Container da ficha da hospedagem
        group_box = QGroupBox("Ficha da Hospedagem")
        group_box.setFont(font_content)
        group_layout = QVBoxLayout(group_box)

        # Cabeçalho com nome do hóspede e número do quarto
        header_layout = QHBoxLayout()
        self.label_nome = QLabel(hospedagem.hospede.nome)
        self.label_nome.setFont(font_title)
        header_layout.addWidget(self.label_nome)

        header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.label_quarto = QLabel(f"Quarto: {hospedagem.quarto.numero}")
        self.label_quarto.setFont(font_title)
        header_layout.addWidget(self.label_quarto)
        group_layout.addLayout(header_layout)

        # Linha separadora
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        group_layout.addWidget(line)

        # Layout com campos para adicionar nova despesa
        input_layout = QHBoxLayout()
        self.input_descricao = QLineEdit()
        self.input_descricao.setPlaceholderText("Descrição do produto")
        input_layout.addWidget(self.input_descricao)

        self.input_valor = LineEditMonetario()
        self.input_valor.setMaximumWidth(100)
        input_layout.addWidget(self.input_valor)

        self.input_quantidade = QSpinBox()
        self.input_quantidade.setMinimum(1)
        input_layout.addWidget(self.input_quantidade)

        self.btn_adicionar = QPushButton("Adicionar")
        input_layout.addWidget(self.btn_adicionar)

        group_layout.addLayout(input_layout)

        # Lista de sugestões com base na descrição
        self.lista_sugestoes = QListWidget()
        self.lista_sugestoes.setMaximumHeight(100)
        self.lista_sugestoes.setVisible(False)
        group_layout.addWidget(self.lista_sugestoes)

        # Conexões dos sinais com as ações
        self.produto_selecionado = None
        self.input_descricao.textChanged.connect(self.atualizar_sugestoes)
        self.lista_sugestoes.itemClicked.connect(self.selecionar_sugestao)
        self.btn_adicionar.clicked.connect(self.adicionar_despesa)

        # Tabela que exibe as despesas
        self.tabela = QTableWidget(0, 5)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela.setHorizontalHeaderLabels(["Data", "Descrição", "QTD", "Valor", "TOTAL"])

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

        self.label_total = QLabel("Total: R$0,00  ")
        self.label_total.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.label_total.setFont(font_title)
        totals_layout.addWidget(self.label_total)

        group_layout.addLayout(totals_layout)
        main_layout.addWidget(group_box)

        # Atalhos exibidos no fim da janela
        self.label_atalhos = QLabel("[ + ] aumenta [ - ] diminui [Del] Exclui [F5] Encerra")
        self.label_atalhos.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_atalhos)

        # Carrega as despesas já registradas no banco
        self.carregar_despesas()

    # Atualiza a lista de sugestões conforme a descrição digitada
    def atualizar_sugestoes(self, texto):
        self.lista_sugestoes.clear()
        if not texto.strip():
            self.lista_sugestoes.setVisible(False)
            return

        resultados = buscar_produto_por_nome(texto)
        if not resultados:
            self.lista_sugestoes.setVisible(False)
            return

        for produto in resultados:
            item = QListWidgetItem(f"{produto.descricao} - R${produto.valor:.2f}")
            item.setData(Qt.ItemDataRole.UserRole, produto)
            self.lista_sugestoes.addItem(item)

        self.lista_sugestoes.setVisible(True)

    # Preenche os campos ao selecionar uma sugestão
    def selecionar_sugestao(self, item):
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

        self.lista_sugestoes.setVisible(False)

    # Adiciona uma nova despesa à tabela e ao banco
    def adicionar_despesa(self):
        produto = self.produto_selecionado
        if not produto:
            return

        quantidade = self.input_quantidade.value()
        valor_digitado = self.input_valor.get_valor_float()

        despesa = create_despesa(
            id_hospedagem=self.hospedagem.id,
            id_produto=produto.id,
            quantidade=quantidade,
            valor_produto=valor_digitado
        )

        row = self.tabela.rowCount()
        self.tabela.insertRow(row)
        self.tabela.setItem(row, 0, QTableWidgetItem(despesa.data.strftime("%d/%m/%Y")))
        self.tabela.setItem(row, 1, QTableWidgetItem(produto.descricao))
        self.tabela.setItem(row, 2, QTableWidgetItem(str(despesa.quantidade)))
        self.tabela.setItem(row, 3, QTableWidgetItem(f"R${despesa.valor_produto:.2f}"))
        self.tabela.setItem(row, 4, QTableWidgetItem(f"R${despesa.valor:.2f}"))

        # Limpa campos após inserção
        self.input_descricao.clear()
        self.input_valor.setText(VALOR_ZERO)
        self.input_valor.valor_cents = 0
        self.input_quantidade.setValue(1)
        self.produto_selecionado = None
        self.lista_sugestoes.setVisible(False)

        self.atualizar_totais()

    # Atualiza os totais de despesas, diárias e valor total
    def atualizar_totais(self):
        total_despesas = 0.0
        for row in range(self.tabela.rowCount()):
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
        self.label_total.setText(f"Total: R${valor_diarias + total_despesas:.2f}  ")

    # Carrega despesas da hospedagem e insere na tabela
    def carregar_despesas(self):
        self.tabela.setRowCount(0)
        despesas = buscar_despesas_por_id_hospedagem(self.hospedagem.id)

        for despesa in despesas:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            data_formatada = despesa.data.strftime("%d/%m/%Y")
            descricao = despesa.produto.descricao
            self.tabela.setItem(row, 0, QTableWidgetItem(data_formatada))
            self.tabela.setItem(row, 1, QTableWidgetItem(descricao))
            self.tabela.setItem(row, 2, QTableWidgetItem(str(despesa.quantidade)))
            self.tabela.setItem(row, 3, QTableWidgetItem(f"R${despesa.valor_produto:.2f}"))
            self.tabela.setItem(row, 4, QTableWidgetItem(f"R${despesa.valor:.2f}"))

        self.atualizar_totais()
