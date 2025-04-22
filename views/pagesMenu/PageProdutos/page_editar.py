from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView, QComboBox, QFormLayout, QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from operations.Ui.produtos_operations import buscar_produto_por_nome, selecionar_produto, update_produto
from styles.styles import style_botao_verde, style_groupbox
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
    
class Ui_page_editar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, page_editar):
        if not page_editar.objectName():
            page_editar.setObjectName("page_editar")

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.widget = QWidget(page_editar)
        self.widget.setObjectName("widget")

        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        font = QFont()
        font.setPointSize(14)

        # Campo de busca por nome

        self.label_buscar = QLabel("Selecione o produto:")
        self.label_buscar.setFont(font)
        self.label_buscar.setMaximumWidth(180)

        self.lineEdit_busca = QLineEdit()
        self.lineEdit_busca.setPlaceholderText("Buscar")
        self.lineEdit_busca.setFont(font)
        self.lineEdit_busca.setMaximumWidth(700)        
        self.lineEdit_busca.textChanged.connect(self.buscar_produto) 

        # Layout horizontal para campo de busca + botão
        busca_layout = QHBoxLayout()
        busca_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        busca_layout.addWidget(self.label_buscar)
        busca_layout.addWidget(self.lineEdit_busca)
        self.verticalLayout.addLayout(busca_layout)

        # Tabela de resultados da busca
        self.tabela_resultados = QTableWidget()
        self.tabela_resultados.setVisible(False)
        self.tabela_resultados.setMaximumHeight(150)
        self.tabela_resultados.setMinimumWidth(800)
        self.tabela_resultados.setColumnCount(2)
        self.tabela_resultados.setHorizontalHeaderLabels(["Descrição", "Valor"])
        self.tabela_resultados.setEditTriggers(QTableWidget.NoEditTriggers)  # impede edição direta
        self.tabela_resultados.setAlternatingRowColors(True)
        self.tabela_resultados.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela_resultados.cellClicked.connect(self.carregar_dados_produto)

        # Faz o cabeçalho se ajustar ao tamanho da tabela
        self.tabela_resultados.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Adiciona a tabela centralizada
        self.verticalLayout.addWidget(self.tabela_resultados, alignment=Qt.AlignCenter)

        # Linha separadora entre colunas
        self.line_separador = QFrame(self.widget)
        self.line_separador.setFrameShape(QFrame.HLine)
        self.line_separador.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_separador)

        # GroupBox estilizado para edição de dados
        self.groupBox = QGroupBox("Editar dados do produto", self.widget)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(style_groupbox())
        self.groupBoxLayout = QFormLayout(self.groupBox)
        self.groupBoxLayout.setSpacing(30)
        self.groupBoxLayout.setContentsMargins(10, 10, 10, 10)

        def create_input_with_error(input_widget, error_label):
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(input_widget)
            layout.addWidget(error_label)
            return container

        # Campo Descrição
        self.lineEdit_descricao = QLineEdit()
        self.lineEdit_descricao.setFont(font)
        self.lineEdit_descricao.setMinimumWidth(300)
        self.label_error_descricao = QLabel("")
        self.label_error_descricao.setStyleSheet("color: red;")
        self.label_error_descricao.setFont(font)
        self.groupBoxLayout.addRow("Produto:", create_input_with_error(self.lineEdit_descricao, self.label_error_descricao))

        # Campo Valor
        self.lineEdit_valor = LineEditMonetario(total='R$ 0,00')
        self.lineEdit_valor.setFont(font)
        self.lineEdit_valor.setMinimumWidth(300)
        self.groupBoxLayout.addRow("Valor:", self.lineEdit_valor)

        # Adiciona GroupBox centralizado
        self.verticalLayout.addWidget(self.groupBox, alignment=Qt.AlignCenter)

        # Botão de salvar alterações
        self.pushButton_salvar = QPushButton("Salvar Alterações")
        self.pushButton_salvar.setFont(font)
        self.pushButton_salvar.setMinimumWidth(200)
        self.pushButton_salvar.setStyleSheet(style_botao_verde())
        self.pushButton_salvar.clicked.connect(self.salvar_alteracoes)

        # Label de confirmação
        self.label_confirmacao = QLabel("")
        self.label_confirmacao.setFont(font)
        self.label_confirmacao.setStyleSheet("color: green;")

        self.verticalLayout.addWidget(self.pushButton_salvar, alignment=Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_confirmacao, alignment=Qt.AlignCenter)

        layout.addWidget(self.widget)
        self.produto_selecionado = None

    def buscar_produto(self):
        descricao = self.lineEdit_busca.text()
        self.tabela_resultados.setRowCount(0)

        produtos = buscar_produto_por_nome(descricao)
        if produtos:
            if self.lineEdit_busca.text() == "":
                self.tabela_resultados.setVisible(False)
            else:
                self.tabela_resultados.setVisible(True)
                for i, h in enumerate(produtos):
                    self.tabela_resultados.insertRow(i)
                    for j, val in enumerate([h.descricao, h.valor]):
                        self.tabela_resultados.setItem(i, j, QTableWidgetItem(str(val)))
        else:
            self.tabela_resultados.setVisible(False)
        self._ajustar_altura_tabela()

    def carregar_dados_produto(self, row, column):
        descricao = self.tabela_resultados.item(row, 0).text()
        valor = self.tabela_resultados.item(row, 1).text()

        self.lineEdit_descricao.setText(descricao)
        self.lineEdit_valor.setText(valor)

        self.produto_selecionado = selecionar_produto(descricao=descricao)

        self.lineEdit_busca.clear()
        self.lineEdit_busca.setPlaceholderText(descricao)
    def salvar_alteracoes(self):
        self.label_error_descricao.setText("")
        self.label_confirmacao.setText("")

        if not self.produto_selecionado:
            self.label_confirmacao.setText("Selecione um produto para editar!")
            return
        descricao = self.lineEdit_descricao.text()
        descricao = descricao.upper()
        erro = False
        if not descricao or len(descricao) < 4:
            self.label_error_descricao.setText("Nome Muito curto*")
            self.label_error_descricao.setMinimumWidth(200)
            erro = True

        if erro:
            return

        update_produto(id_produto=self.produto_selecionado.id, descricao=descricao, valor=self.lineEdit_valor.get_valor_float())

        self.label_confirmacao.setText("Dados atualizados com sucesso!")
        self.buscar_produto()
        QTimer.singleShot(2000, self.limpar_campos)

    def limpar_campos(self):
        self.lineEdit_descricao.clear()
        self.lineEdit_valor.setText("R$ 0,00")
        self.label_confirmacao.setText("")
        self.produto_selecionado = None
    
    def _ajustar_altura_tabela(self):
        row_count = self.tabela_resultados.rowCount()
        if row_count == 0:
            self.tabela_resultados.setVisible(False)
            return
        row_height = self.tabela_resultados.verticalHeader().defaultSectionSize()
        header_height = self.tabela_resultados.horizontalHeader().height()
        scrollbar_height = self.tabela_resultados.horizontalScrollBar().height() if self.tabela_resultados.horizontalScrollBar().isVisible() else 0

        # Calcula a altura desejada com base no número de linhas
        desired_height = row_count * row_height + header_height + scrollbar_height + 2

        self.tabela_resultados.setMaximumHeight(desired_height)
        self.tabela_resultados.setVisible(True)
