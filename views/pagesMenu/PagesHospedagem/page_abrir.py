# ui_page_abrir.py

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from models.models import Hospedagem, Hospede, Quarto, db
from operations.Ui.hospedagem_operations import create_hospedagem
from sqlalchemy.orm import sessionmaker
from datetime import datetime

class Ui_page_abrir(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, page_abrir):
        if not page_abrir.objectName():
            page_abrir.setObjectName("page_abrir")

        # Layout principal da página
        layout = QHBoxLayout(self)

        # Widget base
        self.widget = QWidget(page_abrir)
        layout.addWidget(self.widget)

        # Layout horizontal que segura os dois lados da interface
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setAlignment(Qt.AlignCenter)

        # Fonte base usada na maioria dos elementos
        font = QFont()
        font.setPointSize(14)

        # ========== LADO ESQUERDO: ABERTURA DE HOSPEDAGEM ==========

        self.verticalLayout_abrir = QVBoxLayout()

        # CPF do hóspede
        self.label_cpf = QLabel("CPF:", self.widget)
        self.label_cpf.setFont(font)
        self.verticalLayout_abrir.addWidget(self.label_cpf)

        self.lineEdit_cpf = QLineEdit(self.widget)
        self.lineEdit_cpf.setInputMask("000.000.000-00;_")
        self.lineEdit_cpf.setPlaceholderText("000.000.000-00")
        self.lineEdit_cpf.setFont(font)
        self.lineEdit_cpf.setMinimumSize(150, 0)
        self.lineEdit_cpf.setMaximumSize(150, 16777215)
        self.verticalLayout_abrir.addWidget(self.lineEdit_cpf)

        # Coloca o cursor no início ao focar no campo
        def cpf_focus_in_event(event):
            QLineEdit.focusInEvent(self.lineEdit_cpf, event)
            QTimer.singleShot(0, lambda: self.lineEdit_cpf.setCursorPosition(0))

        # Atualiza o texto do label ao lado do CPF com o nome do hóspede
        def update_cpf_label():
            cpf = self.lineEdit_cpf.text()
            if len(cpf) == 14:
                Session = sessionmaker(bind=db.engine)
                with Session() as session:
                    hospede = session.query(Hospede).filter(Hospede.cpf == cpf).first()
                    self.label_cpf.setText(f"CPF: {hospede.nome}" if hospede else "CPF: Nenhum encontrado")

        self.lineEdit_cpf.focusInEvent = cpf_focus_in_event
        self.lineEdit_cpf.textChanged.connect(update_cpf_label)

        # Quantidade de hóspedes
        self.label_qtd_hospedes = QLabel("Quantidade de hospedes:", self.widget)
        self.label_qtd_hospedes.setFont(font)
        self.verticalLayout_abrir.addWidget(self.label_qtd_hospedes)

        self.spinBox_qtd_hospedes = QSpinBox(self.widget)
        self.spinBox_qtd_hospedes.setFont(font)
        self.spinBox_qtd_hospedes.setMaximumWidth(80)
        self.spinBox_qtd_hospedes.setRange(1, 5)
        self.spinBox_qtd_hospedes.setValue(1)
        self.verticalLayout_abrir.addWidget(self.spinBox_qtd_hospedes)

        # Data de previsão de saída
        self.label_prev_saida = QLabel("Prev. Saída:", self.widget)
        self.label_prev_saida.setFont(font)
        self.verticalLayout_abrir.addWidget(self.label_prev_saida)

        self.dateEdit_prev_saida = QDateEdit(QDate.currentDate(), self.widget)
        self.dateEdit_prev_saida.setMaximumWidth(150)
        self.dateEdit_prev_saida.setFont(font)
        self.verticalLayout_abrir.addWidget(self.dateEdit_prev_saida)

        # Tabela de quartos disponíveis
        self.label_quartos = QLabel("Quartos disponíveis:", self.widget)
        self.label_quartos.setFont(font)
        self.verticalLayout_abrir.addWidget(self.label_quartos)

        self.tableWidget_quartos = QTableWidget(0, 2, self.widget)
        self.tableWidget_quartos.setHorizontalHeaderLabels(["Nº", "Tipo"])
        self.tableWidget_quartos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_quartos.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget_quartos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_quartos.setAlternatingRowColors(True)
        self.tableWidget_quartos.setColumnWidth(0, 50)
        self.tableWidget_quartos.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_abrir.addWidget(self.tableWidget_quartos)

        # Carrega a tabela com os quartos disponíveis
        self.update_quartos()

        # Botão para abrir hospedagem
        self.pushButton_abrir = QPushButton("Abrir", self.widget)
        self.pushButton_abrir.setFont(font)
        self.pushButton_abrir.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_abrir.setMaximumWidth(150)
        self.pushButton_abrir.clicked.connect(self.button_abrir_clicked)

        abrir_layout = QHBoxLayout()
        abrir_layout.addStretch()
        abrir_layout.addWidget(self.pushButton_abrir)
        abrir_layout.addStretch()
        self.verticalLayout_abrir.addLayout(abrir_layout)

        self.horizontalLayout.addLayout(self.verticalLayout_abrir)

        # ========== LINHA DIVISÓRIA ==========
        self.line_separador = QFrame(self.widget)
        self.line_separador.setFrameShape(QFrame.VLine)
        self.line_separador.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout.addWidget(self.line_separador)

        # ========== LADO DIREITO: BUSCA DE HÓSPEDES EXISTENTES ==========

        self.verticalLayout_buscar = QVBoxLayout()

        # Título da seção
        self.label_buscar = QLabel("Buscar", self.widget)
        self.label_buscar.setFont(font)
        self.label_buscar.setAlignment(Qt.AlignCenter)
        self.verticalLayout_buscar.addWidget(self.label_buscar)

        self.line_separador_busca = QFrame(self.widget)
        self.line_separador_busca.setFrameShape(QFrame.HLine)
        self.line_separador_busca.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_buscar.addWidget(self.line_separador_busca)

        # Campo para buscar pelo nome
        self.lineEdit_nome = QLineEdit(self.widget)
        self.lineEdit_nome.setPlaceholderText("Nome do hóspede")
        self.lineEdit_nome.setFont(font)
        self.lineEdit_nome.returnPressed.connect(self.search_hospedes)
        self.verticalLayout_buscar.addWidget(self.lineEdit_nome)

        # Botão de procurar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.pushButton_procurar = QPushButton("Procurar", self.widget)
        self.pushButton_procurar.setFont(font)
        self.pushButton_procurar.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_procurar.setMinimumWidth(150)
        self.pushButton_procurar.clicked.connect(self.search_hospedes)
        btn_layout.addWidget(self.pushButton_procurar)
        btn_layout.addStretch()
        self.verticalLayout_buscar.addLayout(btn_layout)

        # Tabela com os hóspedes encontrados
        self.tableWidget_hospedes = QTableWidget(0, 3, self.widget)
        self.tableWidget_hospedes.setHorizontalHeaderLabels(["Nome", "Telefone", "CPF"])
        self.tableWidget_hospedes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_hospedes.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget_hospedes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_hospedes.setAlternatingRowColors(True)
        self.tableWidget_hospedes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalLayout_buscar.addWidget(self.tableWidget_hospedes)

        # Quando clica em um hóspede, o CPF dele é colocado no campo da esquerda
        self.tableWidget_hospedes.cellClicked.connect(self.pegar_cpf)

        self.verticalLayout_buscar.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.horizontalLayout.addLayout(self.verticalLayout_buscar)

        # Conecta os elementos automaticamente
        QMetaObject.connectSlotsByName(page_abrir)

    # Atualiza a tabela com quartos disponíveis
    def update_quartos(self):
        self.tableWidget_quartos.setRowCount(0)
        with sessionmaker(bind=db.engine)() as session:
            quartos = session.query(Quarto).filter(Quarto.disponivel == True).all()
            for quarto in quartos:
                row = self.tableWidget_quartos.rowCount()
                self.tableWidget_quartos.insertRow(row)
                self.tableWidget_quartos.setItem(row, 0, QTableWidgetItem(str(quarto.numero)))
                self.tableWidget_quartos.setItem(row, 1, QTableWidgetItem(quarto.tipo))

    # Ação ao clicar no botão "Abrir"
    def button_abrir_clicked(self):
        row = self.tableWidget_quartos.currentRow()
        cpf = self.lineEdit_cpf.text()

        if row == -1 or cpf == "..-":
            QMessageBox.warning(self, "Erro", "Selecione todas as opções para continuar")
            return

        # Dados da hospedagem
        quarto_num = self.tableWidget_quartos.item(row, 0).text()
        qtd_hospedes = self.spinBox_qtd_hospedes.value()
        data_saida = self.dateEdit_prev_saida.date().toPython()

        with sessionmaker(bind=db.engine)() as session:
            hospede = session.query(Hospede).filter(Hospede.cpf == cpf).first()
            if not hospede:
                QMessageBox.warning(self, "Erro", "Hóspede não encontrado.")
                return

            # Cria a hospedagem
            QMessageBox.information(self, "Sucesso", f"Hospedagem criada para {hospede.nome}")
            create_hospedagem(cpf, quarto_num, data_saida, qtd_hospedes)

        # Limpa os campos e atualiza os quartos disponíveis
        self.lineEdit_cpf.setText("..-")
        self.dateEdit_prev_saida.setDate(QDate.currentDate())
        self.spinBox_qtd_hospedes.setValue(1)
        self.update_quartos()

    # Busca hóspedes pelo nome
    def search_hospedes(self):
        self.tableWidget_hospedes.setRowCount(0)
        nome = self.lineEdit_nome.text()

        with sessionmaker(bind=db.engine)() as session:
            hospedes = session.query(Hospede).filter(Hospede.nome.ilike(f"%{nome}%")).all()
            for hospede in hospedes:
                row = self.tableWidget_hospedes.rowCount()
                self.tableWidget_hospedes.insertRow(row)
                self.tableWidget_hospedes.setItem(row, 0, QTableWidgetItem(hospede.nome))
                self.tableWidget_hospedes.setItem(row, 1, QTableWidgetItem(hospede.telefone))
                self.tableWidget_hospedes.setItem(row, 2, QTableWidgetItem(hospede.cpf))

    # Ao clicar em um hóspede na tabela, preenche o CPF no campo da esquerda
    def pegar_cpf(self, row):
        cpf = self.tableWidget_hospedes.item(row, 2).text()
        self.lineEdit_cpf.setText(cpf)
