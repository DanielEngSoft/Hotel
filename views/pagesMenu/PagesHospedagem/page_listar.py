from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

class PageListarHospedagem(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
    
        # Criar tabela
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Cliente', 'Pessoas', 'Entrada', 'Prev-Saída', 'Quarto'])
    
        # Ajusta o tamanho das colunas da tabela para se expandirem automaticamente
        # e preencherem todo o espaço disponível de forma uniforme
        header = self.table.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.Stretch)        
        layout.addWidget(self.table)
    
        # Carregar dados
        self.carregar_hospedagens()
    
    def carregar_hospedagens(self):
        pass