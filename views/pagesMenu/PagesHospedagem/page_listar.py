from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from models.models import Hospedagem, Hospede, db
from sqlalchemy.orm import sessionmaker
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout

Session = sessionmaker(bind=db)

class Ui_page_listar(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
    
        # Criar tabela
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.verticalHeader().setVisible(True)
        self.table.setHorizontalHeaderLabels(['Cliente', 'Pessoas', 'Entrada', 'Prev-Saída', 'Quarto'])
        self.table.setSortingEnabled(True) # Habilita a ordenação da tabela
        self.table.setAlternatingRowColors(True) # Cores alternadas para as linhas
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Seleciona linhas inteiras
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection) # Seleciona apenas uma linha
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Desabilita edição
    
        # Ajusta o tamanho das colunas
        header = self.table.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, QHeaderView.Stretch)  

        # Conecta o evento de clique na tabela
        self.table.cellClicked.connect(self.mostrar_info_hospede)      
        layout.addWidget(self.table)
    
    def showEvent(self, event):
        # Atualiza os dados sempre que a página é mostrada
        self.carregar_hospedagens()
        super().showEvent(event)
        
    def carregar_hospedagens(self):
        self.table.setRowCount(0)  # Limpa os dados antes de carregar

        with Session() as session:
            hospedagens = session.query(Hospedagem).join(Hospede).all()

            self.table.setRowCount(len(hospedagens))

            for row, hospedagem in enumerate(hospedagens):
                self.table.setItem(row, 0, QTableWidgetItem(hospedagem.hospede.nome))
                self.table.setItem(row, 1, QTableWidgetItem(str(hospedagem.qtd_hospedes)))
                self.table.setItem(row, 2, QTableWidgetItem(hospedagem.data_entrada.strftime('%d/%m/%Y')))
                self.table.setItem(row, 3, QTableWidgetItem(hospedagem.data_saida.strftime('%d/%m/%Y')))
                self.table.setItem(row, 4, QTableWidgetItem(str(hospedagem.id_quarto)))


    def mostrar_info_hospede(self, row):
        with Session() as session:
            hospedagens = session.query(Hospedagem).join(Hospede).all()
            hospedagem = hospedagens[row]
            hospede = hospedagem.hospede
            
            dialog = QDialog(self)
            dialog.setWindowTitle("Informações do Hóspede")
            layout = QVBoxLayout()
            
            info_labels = [
                f"Nome: {hospede.nome}",
                f"CPF: {hospede.cpf}",
                f"Telefone: {hospede.telefone}",
                f"Diária:" f"R$ {hospedagem.valor_diaria:.2f}",
            ]
            
            for info in info_labels:
                label = QLabel(info)
                layout.addWidget(label)
            
            dialog.setLayout(layout)
            dialog.exec()
