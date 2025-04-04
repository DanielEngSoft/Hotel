from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from models.models import Hospedagem, Hospede, db
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db)

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
        self.table.setRowCount(0)  # Limpa os dados antes de carregar

        with Session() as session:
            hospedagens = session.query(Hospedagem).join(Hospede).all()  # Busca as hospedagens com join em hospedes

            self.table.setRowCount(len(hospedagens))  # Define o número de linhas

            for row, hospedagem in enumerate(hospedagens):
                self.table.setItem(row, 0, QTableWidgetItem(str(hospedagem.id)))
                self.table.setItem(row, 1, QTableWidgetItem(hospedagem.hospede.nome))
                self.table.setItem(row, 2, QTableWidgetItem(str(hospedagem.qtd_hospedes)))
                self.table.setItem(row, 3, QTableWidgetItem(hospedagem.data_entrada.strftime('%d/%m/%Y')))
                self.table.setItem(row, 4, QTableWidgetItem(hospedagem.data_saida.strftime('%d/%m/%Y')))
                self.table.setItem(row, 5, QTableWidgetItem(str(hospedagem.id_quarto)))

        # Conecta o evento de clique na tabela
        self.table.cellClicked.connect(self.mostrar_info_hospede)

    # melhorar depois
    def mostrar_info_hospede(self, row):
        with Session() as session:
            hospedagem = session.query(Hospedagem).join(Hospede).all()[row]
            hospede = hospedagem.hospede
            
            # Cria uma nova janela com as informações do hóspede
            from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout
            dialog = QDialog(self)
            dialog.setWindowTitle("Informações do Hóspede")
            layout = QVBoxLayout()
            
            # Adiciona as informações do hóspede
            info_labels = [
                f"Nome: {hospede.nome}",
                f"CPF: {hospede.cpf}",
                f"Telefone: {hospede.telefone}"
            ]
            
            for info in info_labels:
                label = QLabel(info)
                layout.addWidget(label)
            
            dialog.setLayout(layout)
            dialog.exec()