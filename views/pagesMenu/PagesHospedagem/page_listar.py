from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QLabel, QPushButton, QLineEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor
from datetime import datetime, timedelta
from views.PagesMenu.PagesHospedagem.page_hospedagem import Ui_page_hospedagem
from operations.Ui.hospedagem_operations import (hospedagens_ativas, atualiza_diarias, 
    total_pessoas_hospedadas, saidas_amanha)



from styles.styles import tabela_listar


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
        # Timer para atualizar automaticamente a tabela a cada 2 segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_data)
        self.timer.start(2000)

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
        self.table.setColumnCount(6) 
        self.table.setHorizontalHeaderLabels([
            'Quarto','Cliente', 'Empresa', 'Pessoas', 'Entrada', 'Prev-Saída'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setFont(QFont("Calibri", 12))
        self.table.setSortingEnabled(False)
        self.table.setStyleSheet(tabela_listar())


        # Ajuste de largura das colunas
        header = self.table.horizontalHeader()
        for i in range(6):
            if i in (0, 3):  # Colunas 'Pessoas' e 'Quarto'
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
                self.table.setColumnWidth(i, 50)
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)

        # Conecta evento de clique no cabeçalho para ordenação
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # Conecta duplo clique para abrir ficha da hospedagem
        self.table.cellActivated.connect(self.handle_cell_double_clicked)

        # Adiciona a tabela ao layout
        layout.addWidget(self.table)

        self.rodape = QWidget()
        self.rodape_layout = QHBoxLayout(self.rodape)
        self.rodape_layout.setContentsMargins(0, 0, 0, 0)

        self.fonte_rodape = QFont("Calibri", 12)

        self.label_total_hospedes = QLabel()
        self.label_total_hospedes.setContentsMargins(0, 0, 30, 0)
        self.label_total_hospedes.setFont(self.fonte_rodape)

        self.label_total_hospedages = QLabel("Total de hospedagens: 0")
        self.label_total_hospedages.setContentsMargins(0, 0, 30, 0)
        self.label_total_hospedages.setFont(self.fonte_rodape)

        self.label_saidas_amanha = QLabel()
        self.label_saidas_amanha.setContentsMargins(0, 0, 30, 0)
        self.label_saidas_amanha.setFont(self.fonte_rodape)

        self.label_chegadas_amanha = QLabel("Chegadas amanhã: 0")
        self.label_chegadas_amanha.setContentsMargins(0, 0, 30, 0)
        self.label_chegadas_amanha.setFont(self.fonte_rodape)

        self.rodape_layout.addWidget(self.label_total_hospedes)
        self.rodape_layout.addWidget(self.label_total_hospedages)
        self.rodape_layout.addStretch()
        self.rodape_layout.addWidget(self.label_saidas_amanha)
        self.rodape_layout.addWidget(self.label_chegadas_amanha)

        layout.addWidget(self.rodape)


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
        """Carrega os dados da hospedagem usando hospedagens_ativas"""
        atualiza_diarias()
        # Atualiza os rótulos de rodapé
        self.total_pessoas_hospedadas = total_pessoas_hospedadas()
        self.saidas_amanha = saidas_amanha()
        self.label_total_hospedes.setText(f"Total de hospedes: {self.total_pessoas_hospedadas}")
        self.label_saidas_amanha.setText(f"Saidas amanhã: {self.saidas_amanha}")

        try:
            # Obtém todas as hospedagens ativas
            hospedagens = hospedagens_ativas()

            # Filtro de busca
            filtro = self.search_input.text().strip().lower()
            if filtro:
                hospedagens = [
                    h for h in hospedagens
                    if filtro in h.hospede.nome.lower() or filtro in h.hospede.empresa.lower()
                ]

            # Ordenação dinâmica
            column_map = {
                0: lambda h: h.id_quarto,
                1: lambda h: h.hospede.nome.lower(),
                2: lambda h: h.hospede.empresa.lower(),
                3: lambda h: h.qtd_hospedes,
                4: lambda h: h.data_entrada,
                5: lambda h: h.data_saida
            }
            if self.current_sort_column in column_map:
                key_func = column_map[self.current_sort_column]
                reverse = self.sort_order == 'desc'
                hospedagens.sort(key=key_func, reverse=reverse)

            # Armazena os resultados visíveis
            self.hospedagens_visiveis = hospedagens
            self.table.setRowCount(len(hospedagens))

            # Datas para destacar saídas
            today = datetime.now().date()

            # Preenche as linhas da tabela
            for row, hospedagem in enumerate(hospedagens):
                self.table.setItem(row, 0, QTableWidgetItem(str(hospedagem.id_quarto)))
                self.table.setItem(row, 1, QTableWidgetItem(hospedagem.hospede.nome))
                self.table.setItem(row, 2, QTableWidgetItem(hospedagem.hospede.empresa))
                self.table.setItem(row, 3, QTableWidgetItem(str(hospedagem.qtd_hospedes)))

                entrada_item = QTableWidgetItem(hospedagem.data_entrada.strftime('%d/%m/%Y %H:%M'))
                entrada_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 4, entrada_item)

                saida_data = hospedagem.data_saida.date()
                saida_item = QTableWidgetItem(hospedagem.data_saida.strftime('%d/%m/%Y'))
                saida_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 5, saida_item)

                # Destaque para saídas hoje ou atrasadas
                cor_ocupado = QColor('#A52A2A')  # Vermelho claro
                cor_livre = QColor('#05452f')  # Verde claro
                if saida_data <= today:
                    for col in range(6):
                        item = self.table.item(row, col)
                        if item:
                            item.setData(Qt.ItemDataRole.BackgroundRole, cor_ocupado)
                else:
                    for col in range(6):
                        item = self.table.item(row, col)
                        if item:
                            item.setData(Qt.ItemDataRole.BackgroundRole, cor_livre)


        except Exception as e:
            print("Erro ao carregar dados:", e)

    def abrir_janela_hospedagem(self, hospedagem):
        """Abre a janela de ficha da hospedagem"""
        try:
            janela = Ui_page_hospedagem(hospedagem)
            self.janelas_abertas.append(janela)
            janela.setWindowModality(Qt.ApplicationModal) # Para bloquear a janela principal
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

