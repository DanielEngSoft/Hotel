import sys
from models.models import db, Quarto
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db)
session = Session()
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QStackedWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Horizonte Prime")
        self.setGeometry(100, 100, 800, 600) # posição x, posição y, largura, altura
        self.setMinimumSize(700, 500)
        # self.showMaximized()

        # Widget central principal
        central_widget = QWidget()
        # central_widget.setStyleSheet("background-color: red;")
        self.setCentralWidget(central_widget)

        # Layout principal: Menu Lateral + Conteúdo
        main_layout = QHBoxLayout() # Onde tudo será adicionado
        central_widget.setLayout(main_layout)

        # Menu Lateral
        self.menu_lateral = QListWidget()
        self.menu_lateral.setMaximumWidth(150)
        self.menu_lateral.addItems(["Hospedagem", "Quartos", "Hospedes", "Relatorios"])
        self.menu_lateral.currentRowChanged.connect(self.mudar_pagina)

        # Adicionando as páginas ao StackedWidget
        self.tela_conteudo = QStackedWidget()

        # Criando as Páginas
                # Página de Hospedagem
        pagina_hospedagem = QWidget()
        layout_hospedagem = QVBoxLayout()
        label_hospedagem = QLabel("<H1>Página de Hospedagem</H1>")
        layout_hospedagem.addWidget(label_hospedagem)
        pagina_hospedagem.setLayout(layout_hospedagem)

                # Página de Quartos
        pagina_quartos = QWidget()
        layout_quartos = QVBoxLayout()
        label_quartos = QLabel("Página de Quartos")
        label_quartos.setMaximumSize(150, 150)
        layout_quartos.addWidget(label_quartos)
        pagina_quartos.setLayout(layout_quartos)
        
                # Grid de quartos
        grid_quartos = QWidget()
        grid_layout = QHBoxLayout()
        grid_quartos.setLayout(grid_layout)
        layout_quartos.addWidget(grid_quartos)

        # Buscar quartos do banco de dados
        quartos = session.query(Quarto).all()
        
        # Criar layout para cada linha de 7 quartos
        linha_atual = QHBoxLayout()
        contador = 0
        
        for quarto in quartos:
            # Criar widget para o quarto
            quarto_widget = QWidget()
            quarto_layout = QVBoxLayout()
            quarto_widget.setLayout(quarto_layout)
            
            # Adicionar informações do quarto
            numero = QLabel(f"Quarto {quarto.numero}")
            tipo = QLabel(quarto.tipo)
            
            
            quarto_layout.addWidget(numero)
            quarto_layout.addWidget(tipo)
            
            # Estilizar o widget do quarto
            quarto_widget.setStyleSheet("""
                QWidget {
                    background-color: green;
                    border: 1px solid #ccc;
                    padding: 5px;
                    margin: 5px;
                }
            """)
            
            # Adicionar à linha atual
            linha_atual.addWidget(quarto_widget)
            contador += 1
            
            # Se completou 7 quartos, criar nova linha
            if contador % 7 == 0:
                container = QWidget()
                container.setLayout(linha_atual)
                layout_quartos.addWidget(container)
                linha_atual = QHBoxLayout()
        
        # Adicionar última linha se não estiver completa
        if contador % 7 != 0:
            container = QWidget()
            container.setLayout(linha_atual)
            layout_quartos.addWidget(container)
        

                # Página de Hospedes
        pagina_hospedes = QWidget()
        layout_hospedes = QVBoxLayout()
        label_hospedes = QLabel("Página de Hospedes")
        layout_hospedes.addWidget(label_hospedes)
        pagina_hospedes.setLayout(layout_hospedes)

                # Página de Relatórios
        pagina_relatorios = QWidget()
        layout_relatorios = QVBoxLayout()
        label_relatorios = QLabel("Página de Relatórios")
        layout_relatorios.addWidget(label_relatorios)
        pagina_relatorios.setLayout(layout_relatorios)

        # Adicionando as páginas ao StackedWidget
        self.tela_conteudo.addWidget(pagina_hospedagem)
        self.tela_conteudo.addWidget(pagina_quartos)
        self.tela_conteudo.addWidget(pagina_hospedes)
        self.tela_conteudo.addWidget(pagina_relatorios)

        # Definir a pagina quqe será aberta ao iniciar o programa
        self.menu_lateral.setCurrentRow(0) #Adicionar somente depois de criar as páginas

        main_layout.addWidget(self.menu_lateral)
        main_layout.addWidget(self.tela_conteudo)

    # Conectando o clique do menu lateral à mudança de página
    def mudar_pagina(self, index):
        self.tela_conteudo.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()