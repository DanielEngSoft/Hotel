# ui_page_abrir.py

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from models.models import Hospedagem, Hospede, Quarto, db
from operations.Ui.hospedagem_operations import create_hospedagem
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from styles.styles import style_botao_verde


class Ui_page_abrir(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, page_abrir):
        if not page_abrir.objectName():
            page_abrir.setObjectName("page_abrir")

        layout = QHBoxLayout(self)

        self.widget = QWidget(page_abrir)
        layout.addWidget(self.widget)

        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setPointSize(14)

        # ========== LADO ESQUERDO ==========

        self.verticalLayout_abrir = QVBoxLayout()

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

        def cpf_focus_in_event(event):
            QLineEdit.focusInEvent(self.lineEdit_cpf, event)
            QTimer.singleShot(0, lambda: self.lineEdit_cpf.setCursorPosition(0))

        def update_cpf_label():
            cpf = self.lineEdit_cpf.text()
            if len(cpf) == 14:
                Session = sessionmaker(bind=db.engine)
                with Session() as session:
                    hospede = session.query(Hospede).filter(Hospede.cpf == cpf).first()
                    self.label_cpf.setText(f"CPF: {hospede.nome}" if hospede else "CPF: Nenhum encontrado")

        self.lineEdit_cpf.focusInEvent = cpf_focus_in_event
        self.lineEdit_cpf.textChanged.connect(update_cpf_label)
        self.lineEdit_cpf.editingFinished.connect(update_cpf_label)

        self.label_qtd_hospedes = QLabel("Quantidade de hospedes:", self.widget)
        self.label_qtd_hospedes.setFont(font)
        self.verticalLayout_abrir.addWidget(self.label_qtd_hospedes)

        qtd_layout = QHBoxLayout()

        self.spinBox_qtd_hospedes = QSpinBox(self.widget)
        self.spinBox_qtd_hospedes.setFont(font)
        self.spinBox_qtd_hospedes.setMaximumWidth(80)
        self.spinBox_qtd_hospedes.setRange(1, 5)
        self.spinBox_qtd_hospedes.setValue(1)
        qtd_layout.addWidget(self.spinBox_qtd_hospedes)

        self.label_preco = QLabel("R$ 100", self.widget)
        self.label_preco.setFont(font)
        self.label_preco.setStyleSheet("color: green; font-weight: bold;")
        qtd_layout.addWidget(self.label_preco)

        self.verticalLayout_abrir.addLayout(qtd_layout)

        self.spinBox_qtd_hospedes.valueChanged.connect(self.atualizar_preco)

        self.label_prev_saida = QLabel("Prev. Saída:", self.widget)
        self.label_prev_saida.setFont(font)
        self.verticalLayout_abrir.addWidget(self.label_prev_saida)

        self.dateEdit_prev_saida = QDateEdit(QDate.currentDate(), self.widget)
        self.dateEdit_prev_saida.setMaximumWidth(150)
        self.dateEdit_prev_saida.setFont(font)
        self.verticalLayout_abrir.addWidget(self.dateEdit_prev_saida)

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

        self.update_quartos()

        self.pushButton_abrir = QPushButton("Abrir", self.widget)
        self.pushButton_abrir.setFont(font)
        self.pushButton_abrir.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_abrir.setMaximumWidth(150)
        self.pushButton_abrir.setStyleSheet(style_botao_verde())
        self.pushButton_abrir.clicked.connect(self.button_abrir_clicked)

        abrir_layout = QHBoxLayout()
        abrir_layout.addStretch()
        abrir_layout.addWidget(self.pushButton_abrir)
        abrir_layout.addStretch()
        self.verticalLayout_abrir.addLayout(abrir_layout)

        self.horizontalLayout.addLayout(self.verticalLayout_abrir)

        self.line_separador = QFrame(self.widget)
        self.line_separador.setFrameShape(QFrame.VLine)
        self.line_separador.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout.addWidget(self.line_separador)

        # ========== LADO DIREITO ==========

        self.verticalLayout_buscar = QVBoxLayout()

        self.label_buscar = QLabel("Buscar", self.widget)
        self.label_buscar.setFont(font)
        self.label_buscar.setAlignment(Qt.AlignCenter)
        self.verticalLayout_buscar.addWidget(self.label_buscar)

        self.line_separador_busca = QFrame(self.widget)
        self.line_separador_busca.setFrameShape(QFrame.HLine)
        self.line_separador_busca.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_buscar.addWidget(self.line_separador_busca)

        self.lineEdit_nome = QLineEdit(self.widget)
        self.lineEdit_nome.setPlaceholderText("Nome do hóspede")
        self.lineEdit_nome.setFont(font)
        self.lineEdit_nome.returnPressed.connect(self.search_hospedes)
        self.verticalLayout_buscar.addWidget(self.lineEdit_nome)

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

        self.tableWidget_hospedes = QTableWidget(0, 3, self.widget)
        self.tableWidget_hospedes.setHorizontalHeaderLabels(["Nome", "Empresa", "CPF"])
        self.tableWidget_hospedes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget_hospedes.setSelectionMode(QTableWidget.SingleSelection)
        self.tableWidget_hospedes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget_hospedes.setAlternatingRowColors(True)
        self.tableWidget_hospedes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalLayout_buscar.addWidget(self.tableWidget_hospedes)

        self.tableWidget_hospedes.cellClicked.connect(self.pegar_cpf)

        self.verticalLayout_buscar.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.horizontalLayout.addLayout(self.verticalLayout_buscar)

        QMetaObject.connectSlotsByName(page_abrir)

    def update_quartos(self):
        self.tableWidget_quartos.setRowCount(0)
        with sessionmaker(bind=db.engine)() as session:
            quartos = session.query(Quarto).filter(Quarto.disponivel == True).all()
            for quarto in quartos:
                row = self.tableWidget_quartos.rowCount()
                self.tableWidget_quartos.insertRow(row)
                item_num = QTableWidgetItem(str(quarto.numero))
                item_num.setTextAlignment(Qt.AlignCenter)
                self.tableWidget_quartos.setItem(row, 0, item_num)
                self.tableWidget_quartos.setItem(row, 1, QTableWidgetItem(quarto.tipo))

    def button_abrir_clicked(self):
        row = self.tableWidget_quartos.currentRow()
        cpf = self.lineEdit_cpf.text()

        if row == -1 or len(cpf) != 14:
            QMessageBox.warning(self, "Erro", "Selecione todas as opções para continuar")
            return

        quarto_num = self.tableWidget_quartos.item(row, 0).text()
        qtd_hospedes = self.spinBox_qtd_hospedes.value()
        data_saida = self.dateEdit_prev_saida.date().toPython()

        with sessionmaker(bind=db.engine)() as session:
            hospede = session.query(Hospede).filter(Hospede.cpf == cpf).first()
            if not hospede:
                QMessageBox.warning(self, "Erro", "Hóspede não encontrado.")
                return

            QMessageBox.information(self, "Sucesso", f"Hospedagem criada para {hospede.nome}")
            create_hospedagem(cpf, quarto_num, data_saida, qtd_hospedes)

        self.lineEdit_cpf.setText("..-")
        self.dateEdit_prev_saida.setDate(QDate.currentDate())
        self.spinBox_qtd_hospedes.setValue(1)
        self.atualizar_preco(1)
        self.update_quartos()

    def search_hospedes(self):
        self.tableWidget_hospedes.setRowCount(0)
        nome = self.lineEdit_nome.text()

        with sessionmaker(bind=db.engine)() as session:
            hospedes = session.query(Hospede).filter(Hospede.nome.ilike(f"%{nome}%")).all()
            for hospede in hospedes:
                row = self.tableWidget_hospedes.rowCount()
                self.tableWidget_hospedes.insertRow(row)
                self.tableWidget_hospedes.setItem(row, 0, QTableWidgetItem(hospede.nome))
                self.tableWidget_hospedes.setItem(row, 1, QTableWidgetItem(hospede.empresa))
                self.tableWidget_hospedes.setItem(row, 2, QTableWidgetItem(hospede.cpf))

    def pegar_cpf(self, row):
        cpf = self.tableWidget_hospedes.item(row, 2).text()
        self.lineEdit_cpf.setText(cpf)
        self.lineEdit_cpf.setFocus()

    def atualizar_preco(self, valor):
        precos = {1: 100, 2: 150, 3: 200, 4: 250, 5: 300}
        preco = precos.get(valor, 0)
        self.label_preco.setText(f"R$ {preco}")
