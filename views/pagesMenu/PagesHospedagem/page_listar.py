from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QLabel, QPushButton, QLineEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor
from models.models import Hospedagem, Hospede, db
from sqlalchemy.orm import sessionmaker, joinedload
from datetime import datetime, timedelta
from views.PagesMenu.PagesHospedagem.page_ficha import JanelaHospedagem

# Sessão para comunicação com o banco de dados
Session = sessionmaker(bind=db)

# Página de listagem de hospedagens
class Ui_page_listar(QWidget):
    def __init__(self):
        super().__init__()
        self.page_size = 20
        self.current_page = 0
        self.current_sort_column = None
        self.sort_order = 'asc'
        self.hospedagens_visiveis = []
        self.janelas_abertas = []

        self.setup_ui()

    def setup_ui(self):
        # Layout vertical principal da página
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Layout horizontal para campo de busca
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por cliente ou empresa...")
        self.search_input.textChanged.connect(self.load_data)
        filter_layout.addWidget(self.search_input)
        layout.addLayout(filter_layout)

        # Tabela de hospedagens
        self.table = QTableWidget()
        self.table.setFont(QFont("Calibri", 12))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'Cliente', 'Empresa', 'Pessoas', 'Entrada', 'Prev-Saída', 'Quarto'
        ])
        self.table.setSortingEnabled(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Ajuste de largura das colunas
        header = self.table.horizontalHeader()
        for i in range(6):
            if i in (2, 5):  # Colunas 'Pessoas' e 'Quarto'
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
                self.table.setColumnWidth(i, 50)
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)

        # Conecta evento de clique no cabeçalho para ordenação
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # Conecta duplo clique para abrir ficha da hospedagem
        self.table.cellDoubleClicked.connect(self.handle_cell_double_clicked)

        # Adiciona a tabela ao layout
        layout.addWidget(self.table)

    def showEvent(self, event):
        """Atualiza os dados da tabela ao exibir a página"""
        self.load_data()
        super().showEvent(event)

    def on_header_clicked(self, logical_index):
        """Ordena os dados da tabela com base na coluna clicada"""
        if self.current_sort_column == logical_index:
            self.sort_order = 'desc' if self.sort_order == 'asc' else 'asc'
        else:
            self.sort_order = 'asc'
        self.current_sort_column = logical_index
        self.load_data(page=self.current_page)

    def load_data(self, page=0):
        """Carrega os dados da hospedagem do banco para a tabela"""
        with Session() as session:
            query = session.query(Hospedagem).options(
                joinedload(Hospedagem.hospede),
                joinedload(Hospedagem.quarto)
            ).join(Hospede)

            # Filtro de busca
            filtro = self.search_input.text().strip().lower()
            if filtro:
                query = query.filter(
                    (Hospede.nome.ilike(f'%{filtro}%')) |
                    (Hospede.empresa.ilike(f'%{filtro}%'))
                )

            # Ordenação dinâmica
            column_map = {
                0: Hospede.nome,
                1: Hospede.empresa,
                2: Hospedagem.qtd_hospedes,
                3: Hospedagem.data_entrada,
                4: Hospedagem.data_saida,
                5: Hospedagem.id_quarto
            }
            if self.current_sort_column in column_map:
                coluna = column_map[self.current_sort_column]
                query = query.order_by(coluna.asc() if self.sort_order == 'asc' else coluna.desc())

            # Executa a consulta e armazena os resultados visíveis
            hospedagens = query.all()
            self.hospedagens_visiveis = hospedagens
            self.table.setRowCount(len(hospedagens))

            # Datas para destacar saídas
            today = datetime.now().date()

            # Preenche as linhas da tabela
            for row, hospedagem in enumerate(hospedagens):
                self.table.setItem(row, 0, QTableWidgetItem(hospedagem.hospede.nome))
                self.table.setItem(row, 1, QTableWidgetItem(hospedagem.hospede.empresa))
                self.table.setItem(row, 2, QTableWidgetItem(str(hospedagem.qtd_hospedes)))

                entrada_item = QTableWidgetItem(hospedagem.data_entrada.strftime('%d/%m/%Y %H:%M'))
                entrada_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 3, entrada_item)

                saida_data = hospedagem.data_saida.date()
                saida_item = QTableWidgetItem(hospedagem.data_saida.strftime('%d/%m/%Y'))
                saida_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 4, saida_item)

                self.table.setItem(row, 5, QTableWidgetItem(str(hospedagem.id_quarto)))

                # Destaque para saídas hoje ou atrasadas
                if saida_data <= today:
                    cor = QColor(255, 102, 102)  # Vermelho claro
                    for col in range(6):
                        item = self.table.item(row, col)
                        if item:
                            item.setBackground(cor)

    def abrir_janela_hospedagem(self, hospedagem):
        """Abre a janela de ficha da hospedagem"""
        try:
            janela = JanelaHospedagem(hospedagem)
            self.janelas_abertas.append(janela)
            janela.setWindowModality(Qt.ApplicationModal)
            janela.raise_()
            janela.activateWindow()
            janela.show()
        except Exception as e:
            print("Erro ao abrir ficha:", e)

    def handle_cell_double_clicked(self, row, column):
        """Dispara ao clicar duas vezes em uma linha da tabela"""
        try:
            hospedagem = self.hospedagens_visiveis[row]
            self.abrir_janela_hospedagem(hospedagem)
        except IndexError:
            print("Erro: índice fora do intervalo ao tentar abrir ficha de hospedagem.")
