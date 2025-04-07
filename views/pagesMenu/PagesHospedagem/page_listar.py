# ui_page_listar.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QLabel, QPushButton, QLineEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QDate
from models.models import Hospedagem, Hospede, db
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Session = sessionmaker(bind=db)

class Ui_page_listar(QWidget):
    def __init__(self):
        super().__init__()
        self.page_size = 20
        self.current_page = 0
        self.current_sort_column = None
        self.sort_order = 'asc'
        self.hospedagens_visiveis = []
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Filtro de busca por nome ou empresa
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por cliente ou empresa...")
        self.search_input.textChanged.connect(self.load_data)
        filter_layout.addWidget(self.search_input)
        layout.addLayout(filter_layout)

        # Criar tabela
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Cliente','Empresa', 'Pessoas', 'Entrada', 'Prev-Saída', 'Quarto'])
        self.table.setSortingEnabled(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)


        # Chama a função on_header_clicked quando o cabeçalho é clicado
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # Ajusta o tamanho das colunas
        header = self.table.horizontalHeader()
        for i in range(6):
            if i in (2, 5):  # Colunas 'Pessoas' e 'Quarto'
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
                self.table.setColumnWidth(i, 50)
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)

        self.table.cellDoubleClicked.connect(self.mostrar_info_hospede)
        layout.addWidget(self.table)

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
        with Session() as session:
            query = session.query(Hospedagem).join(Hospede)

            column_map = {
                0: Hospede.nome,
                1: Hospede.empresa,
                2: Hospedagem.qtd_hospedes,
                3: Hospedagem.data_entrada,
                4: Hospedagem.data_saida,
                5: Hospedagem.id_quarto
            }

            # Filtro de texto
            filtro = self.search_input.text().strip().lower()
            if filtro:
                query = query.filter(
                    (Hospede.nome.ilike(f'%{filtro}%')) |
                    (Hospede.empresa.ilike(f'%{filtro}%'))
                )

            if self.current_sort_column in column_map:
                column_attr = column_map[self.current_sort_column]
                if self.sort_order == 'asc':
                    query = query.order_by(column_attr.asc())
                else:
                    query = query.order_by(column_attr.desc())

            hospedagens = query.all()
            self.hospedagens_visiveis = hospedagens

            self.table.setRowCount(len(hospedagens))

            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)

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

                # Destaque se a saída é hoje ou amanhã
                # Definir cores para destaque
                if saida_data == today:
                    cor = Qt.GlobalColor.darkRed
                else:
                    cor = None

                # Aplicar cor apenas se necessário
                if cor:
                    for col in range(6):
                        item = self.table.item(row, col)
                        if item:  # Verifica se o item existe
                            item.setBackground(cor)


    def mostrar_info_hospede(self, row):
        if row < 0 or row >= len(self.hospedagens_visiveis):
            return

        hospedagem = self.hospedagens_visiveis[row]
        hospede = hospedagem.hospede

        dialog = QDialog(self)
        dialog.setWindowTitle("Informações do Hóspede")
        layout = QVBoxLayout()

        info_labels = [
            f"Nome: {hospede.nome}",
            f"CPF: {hospede.cpf}",
            f"Telefone: {hospede.telefone}",
            f"Diária: R$ {hospedagem.valor_diaria:.2f}",
        ]

        for info in info_labels:
            layout.addWidget(QLabel(info))

        btn_fechar = QPushButton("Fechar")
        btn_fechar.clicked.connect(dialog.accept)
        layout.addWidget(btn_fechar)

        dialog.setLayout(layout)
        dialog.exec()
