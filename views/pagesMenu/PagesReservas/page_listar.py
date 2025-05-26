from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor
from datetime import datetime

from operations.Ui.reservas_operations import reservas_ativas


class Ui_page_listar_reserva(QWidget):
    def __init__(self):
        super().__init__()
        self.page_size = 20
        self.current_page = 0
        self.current_sort_column = None
        self.sort_order = 'asc'
        self.reservas_visiveis = []

        self.setup_ui()
        self.setup_timer()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Campo de busca
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por cliente ou empresa...")
        self.search_input.textChanged.connect(self.load_data)
        filter_layout.addWidget(self.search_input)
        layout.addLayout(filter_layout)

        # Tabela de reservas
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            'Quarto', 'Cliente', 'Empresa', 'Pessoas', 'Entrada', 'Prev-Saída'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setFont(QFont("Calibri", 12))
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)

        # Ajuste das colunas
        header = self.table.horizontalHeader()
        for i in range(6):
            if i in (0, 3):  # Quarto e Pessoas
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
                self.table.setColumnWidth(i, 50)
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)

        header.sectionClicked.connect(self.on_header_clicked)
        layout.addWidget(self.table)

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_data)
        self.timer.start(4000)

    def showEvent(self, event):
        self.load_data()
        super().showEvent(event)

    def on_header_clicked(self, logical_index):
        if self.current_sort_column == logical_index:
            self.sort_order = 'desc' if self.sort_order == 'asc' else 'asc'
        else:
            self.sort_order = 'asc'
        self.current_sort_column = logical_index
        self.load_data(page=self.current_page)

    def load_data(self, page=0):
        try:
            reservas = reservas_ativas()

            # Filtro
            filtro = self.search_input.text().strip().lower()
            if filtro:
                reservas = [
                    r for r in reservas
                    if filtro in r.hospede.nome.lower() or filtro in r.hospede.empresa.lower()
                ]

            # Ordenação
            column_map = {
                0: lambda r: r.id_quarto,
                1: lambda r: r.hospede.nome.lower(),
                2: lambda r: r.hospede.empresa.lower(),
                3: lambda r: r.qtd_hospedes,
                4: lambda r: r.data_entrada,
                5: lambda r: r.data_saida
            }
            if self.current_sort_column in column_map:
                key_func = column_map[self.current_sort_column]
                reverse = self.sort_order == 'desc'
                reservas.sort(key=key_func, reverse=reverse)

            # Exibição na tabela
            self.reservas_visiveis = reservas
            self.table.clearContents()  # Limpa o conteúdo atual da tabela
            self.table.setRowCount(len(reservas))
            today = datetime.now().date()

            for row, reserva in enumerate(reservas):
                if reserva is None:
                    continue
                    
                self.table.setItem(row, 0, QTableWidgetItem(str(reserva.id_quarto)))
                self.table.setItem(row, 1, QTableWidgetItem(str(reserva.hospede.nome)))
                self.table.setItem(row, 2, QTableWidgetItem(str(reserva.hospede.empresa)))
                self.table.setItem(row, 3, QTableWidgetItem(str(reserva.qtd_hospedes)))

                entrada_item = QTableWidgetItem(reserva.data_entrada.strftime('%d/%m/%Y %H:%M'))
                entrada_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 4, entrada_item)

                saida_data = reserva.data_saida.date()
                saida_item = QTableWidgetItem(reserva.data_saida.strftime('%d/%m/%Y'))
                saida_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 5, saida_item)

                # Destaque em vermelho para reservas com saída vencida ou no dia
                if saida_data <= today:
                    for col in range(6):
                        item = self.table.item(row, col)
                        if item:
                            item.setBackground(QColor('#A52A2A'))

            self.table.viewport().update()  # Força atualização visual da tabela

        except Exception as e:
            print("Erro ao carregar reservas:", e)
            import traceback
            traceback.print_exc()  # Imprime o stack trace completo do erro