# ui_page_listar.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QLabel, QPushButton
)
from PySide6.QtCore import Qt
from models.models import Hospedagem, Hospede, db
from sqlalchemy.orm import sessionmaker

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
                self.table.setColumnWidth(i, 50)  # Limite mínimo visual
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)

        self.table.cellClicked.connect(self.mostrar_info_hospede)
        layout.addWidget(self.table)

    def showEvent(self, event):
        self.load_data()
        super().showEvent(event)

    def on_header_clicked(self, logical_index):
        order_column = self.table.horizontalHeaderItem(logical_index).text()

        if self.current_sort_column == order_column:
            self.sort_order = 'desc' if self.sort_order == 'asc' else 'asc'
        else:
            self.sort_order = 'asc'
        self.current_sort_column = order_column

        self.load_data(page=self.current_page)

    def load_data(self, page=0):
        with Session() as session:
            query = session.query(Hospedagem).join(Hospede)

            column_map = {
                'Cliente': Hospede.nome,
                'Empresa': Hospede.empresa,
                'Pessoas': Hospedagem.qtd_hospedes,
                'Entrada': Hospedagem.data_entrada,
                'Prev-Saída': Hospedagem.data_saida,
                'Quarto': Hospedagem.id_quarto
            }

            if self.current_sort_column in column_map:
                column_attr = column_map[self.current_sort_column]
                if self.sort_order == 'asc':
                    query = query.order_by(column_attr.asc())
                else:
                    query = query.order_by(column_attr.desc())

            # Paginação (preparado, mas não implementado nos controles)
            # query = query.offset(page * self.page_size).limit(self.page_size)

            hospedagens = query.all()
            self.hospedagens_visiveis = hospedagens

            self.table.setRowCount(len(hospedagens))
            for row, hospedagem in enumerate(hospedagens):
                self.table.setItem(row, 0, QTableWidgetItem(hospedagem.hospede.nome))
                self.table.setItem(row, 1, QTableWidgetItem(hospedagem.hospede.empresa))
                self.table.setItem(row, 2, QTableWidgetItem(str(hospedagem.qtd_hospedes)))

                entrada_item = QTableWidgetItem(hospedagem.data_entrada.strftime('%d/%m/%Y %H:%M'))
                entrada_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 3, entrada_item)

                saida_item = QTableWidgetItem(hospedagem.data_saida.strftime('%d/%m/%Y'))
                saida_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 4, saida_item)

                self.table.setItem(row, 5, QTableWidgetItem(str(hospedagem.id_quarto)))

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
