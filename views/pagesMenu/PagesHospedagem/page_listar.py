from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QLabel, QPushButton, QLineEdit, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor
from datetime import datetime, timedelta
from views.PagesMenu.PagesHospedagem.page_hospedagem import Ui_page_hospedagem
from operations.Ui.hospedagem_operations import (
    hospedagens_ativas, atualiza_diarias,
    total_pessoas_hospedadas, saidas_amanha
)
from operations.Ui.reservas_operations import (
    reservas_ativas, reserva_para_hospedagem, pegar_id_reserva, deletar_reserva
)

from styles.styles import style_botao_verde, style_botao_vermelho


# Página de listagem de hospedagens e reservas
class Ui_page_listar_hospedagem(QWidget):
    def __init__(self):
        super().__init__()
        self.page_size = 20
        self.current_page = 0
        self.current_sort_column = None
        self.sort_order = 'asc'
        self.itens_visiveis = []  # Renomeado para ser mais genérico
        self.janelas_abertas = []

        self.setup_ui()
        # Timer para atualizar automaticamente a tabela a cada 2 segundos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ler_dados)  # Renomeado para ser mais genérico
        self.timer.start(2000)

    def setup_ui(self):
        # Layout vertical principal da página
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Layout horizontal para campo de busca
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por cliente ou empresa...")
        self.search_input.textChanged.connect(self.ler_dados)  # Renomeado para ser mais genérico
        filter_layout.addWidget(self.search_input)
        layout.addLayout(filter_layout)

        # Tabela de hospedagens e reservas
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

        # Conecta duplo clique para abrir ficha da hospedagem/reserva
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

        self.label_total_itens = QLabel("Total de itens: 0")  # Label genérico para total de itens
        self.label_total_itens.setContentsMargins(0, 0, 30, 0)
        self.label_total_itens.setFont(self.fonte_rodape)

        self.label_saidas_amanha = QLabel()
        self.label_saidas_amanha.setContentsMargins(0, 0, 30, 0)
        self.label_saidas_amanha.setFont(self.fonte_rodape)

        self.label_chegadas_amanha = QLabel("Chegadas amanhã: 0")
        self.label_chegadas_amanha.setContentsMargins(0, 0, 30, 0)
        self.label_chegadas_amanha.setFont(self.fonte_rodape)

        self.rodape_layout.addWidget(self.label_total_hospedes)
        self.rodape_layout.addWidget(self.label_total_itens)
        self.rodape_layout.addStretch()
        self.rodape_layout.addWidget(self.label_saidas_amanha)
        self.rodape_layout.addWidget(self.label_chegadas_amanha)

        layout.addWidget(self.rodape)

    def showEvent(self, event):
        """Atualiza os dados da tabela ao exibir a página"""
        self.ler_dados()  # Renomeado para ser mais genérico
        super().showEvent(event)

    def on_header_clicked(self, logical_index):
        """Ordena os dados da tabela com base na coluna clicada"""
        if self.current_sort_column == logical_index:
            self.sort_order = 'desc' if self.sort_order == 'asc' else 'asc'
        else:
            self.sort_order = 'asc'
        self.current_sort_column = logical_index
        self.ler_dados(page=self.current_page)  # Renomeado para ser mais genérico

    def ler_dados(self, page=0):
        """Carrega os dados de hospedagens e reservas ativas e atualiza a tabela"""
        atualiza_diarias()
        hospedagens = hospedagens_ativas()
        reservas = reservas_ativas()

        # Combine as listas de hospedagens e reservas, adicionando um 'tipo'
        itens = []
        for reserva in reservas:
            reserva.tipo = 'reserva'
            if reserva.data_entrada.date() <= datetime.now().date():
                itens.append(reserva)
        for hospedagem in hospedagens:
            hospedagem.tipo = 'hospedagem'
            itens.append(hospedagem)

        # Filtro de busca
        filtro = self.search_input.text().strip().lower()
        if filtro:
            itens = [
                item for item in itens
                if (hasattr(item, 'hospede') and
                    (filtro in item.hospede.nome.lower() or filtro in item.hospede.empresa.lower()))
            ]

        # Ordenação dinâmica
        column_map = {
            0: lambda item: item.id_quarto,
            1: lambda item: item.hospede.nome.lower() if hasattr(item, 'hospede') else '',
            2: lambda item: item.hospede.empresa.lower() if hasattr(item, 'hospede') else '',
            3: lambda item: item.qtd_hospedes,
            4: lambda item: item.data_entrada,
            5: lambda item: item.data_saida
        }
        if self.current_sort_column in column_map:
            key_func = column_map[self.current_sort_column]
            reverse = self.sort_order == 'desc'
            itens.sort(key=key_func, reverse=reverse)

        # Atualiza os rótulos de rodapé
        total_pessoas = total_pessoas_hospedadas()
        total_itens = len(itens)
        saidas = saidas_amanha()
        self.label_total_hospedes.setText(f"Total de hospedes: {total_pessoas}")
        self.label_total_itens.setText(f"Total de itens: {total_itens}")
        self.label_saidas_amanha.setText(f"Saidas amanhã: {saidas}")
        self.label_chegadas_amanha.setText(f"Chegadas amanhã: {len([r for r in reservas if r.data_entrada.date() == (datetime.now().date() + timedelta(days=1))])}")

        # Armazena os resultados visíveis
        self.itens_visiveis = itens
        self.table.setRowCount(len(itens))

        # Datas para destacar saídas
        today = datetime.now().date()
        cor_ocupado = QColor('#A52A2A')  # Vermelho claro
        cor_reservado = QColor('#FFA500')  # Laranja

        # Preenche as linhas da tabela com os dados combinados
        for row, item in enumerate(itens):
            self.table.setItem(row, 0, QTableWidgetItem(str(item.id_quarto)))
            if hasattr(item, 'hospede'):
                self.table.setItem(row, 1, QTableWidgetItem(item.hospede.nome))
                self.table.setItem(row, 2, QTableWidgetItem(item.hospede.empresa))
            else:
                self.table.setItem(row, 1, QTableWidgetItem(""))
                self.table.setItem(row, 2, QTableWidgetItem(""))
            self.table.setItem(row, 3, QTableWidgetItem(str(item.qtd_hospedes)))

            entrada_item = QTableWidgetItem(item.data_entrada.strftime('%d/%m/%Y %H:%M'))
            entrada_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, entrada_item)

            saida_item = QTableWidgetItem(item.data_saida.strftime('%d/%m/%Y'))
            saida_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 5, saida_item)

            # Aplica a cor de fundo com base no tipo de item
            if item.tipo == 'reserva':
                for col in range(6):
                    table_item = self.table.item(row, col)
                    if table_item:
                        table_item.setData(Qt.ItemDataRole.BackgroundRole, cor_reservado)
            elif item.tipo == 'hospedagem':
                saida_data = item.data_saida.date()
                if saida_data <= today:
                    for col in range(6):
                        table_item = self.table.item(row, col)
                        if table_item:
                            table_item.setData(Qt.ItemDataRole.BackgroundRole, cor_ocupado)

    def abrir_janela_hospedagem(self, hospedagem):
        """Abre a janela de ficha da hospedagem"""
        try:
            janela = Ui_page_hospedagem(hospedagem)
            self.janelas_abertas.append(janela)
            janela.setWindowModality(Qt.ApplicationModal)  # Para bloquear a janela principal
            janela.raise_()
            janela.activateWindow()
            janela.show()
        except Exception as e:
            print("Erro ao abrir ficha de hospedagem:", e)

    def abrir_reserva(self, reserva):
        """Abre a janela de confirmação para abrir ou cancelar a reserva"""
        try:
            id_reserva = reserva.id  # O ID da reserva já está no objeto 'reserva'

            # Criar o QMessageBox
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Gerenciar Reserva")
            msg_box.setText(f"Deseja abrir a hospedagem para a reserva do cliente '{reserva.hospede.nome}'?")
            msg_box.setIcon(QMessageBox.Question)

            # Botão "Cancelar Reserva" (vermelho)
            btn_cancelar = QPushButton("Cancelar Reserva")
            btn_cancelar.setStyleSheet(style_botao_vermelho())
            msg_box.addButton(btn_cancelar, QMessageBox.RejectRole)

            # Botão "Abrir Hospedagem" (verde)
            btn_abrir = QPushButton("Abrir Hospedagem")
            btn_abrir.setStyleSheet(style_botao_verde())
            msg_box.addButton(btn_abrir, QMessageBox.AcceptRole)

            # Botão "Fechar" (padrão)
            btn_fechar = QPushButton("Fechar")
            msg_box.addButton(btn_fechar, QMessageBox.NoRole)
            msg_box.setDefaultButton(btn_fechar)
            msg_box.setEscapeButton(btn_fechar)
            btn_fechar.setVisible(False)

            # Exibir o QMessageBox
            msg_box.exec()

            if msg_box.clickedButton() == btn_abrir:
                reserva_para_hospedagem(id_reserva)
                deletar_reserva(id_reserva)
                self.ler_dados()
            elif msg_box.clickedButton() == btn_cancelar:
                deletar_reserva(id_reserva)
                self.ler_dados()
        except Exception as e:
            print("Erro ao gerenciar reserva:", e)

    def handle_cell_double_clicked(self, row, column):
        """Dispara ao clicar duas vezes em uma linha da tabela"""
        try:
            item = self.itens_visiveis[row]
            if item.tipo != 'reserva':
                self.abrir_janela_hospedagem(item)
            else:
                self.abrir_reserva(item)
        except IndexError:
            print("Erro: índice fora do intervalo ao tentar abrir item.")