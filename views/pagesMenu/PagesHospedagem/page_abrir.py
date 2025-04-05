from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

from models.models import Hospedagem, Hospede, Quarto, db
from operations.Ui.hospedagem_operations import create_hospedagem
from sqlalchemy.orm import sessionmaker
from PySide6.QtCore import QTimer
from datetime import datetime
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal

class Ui_page_abrir(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, page_abrir):
        if not page_abrir.objectName():
            page_abrir.setObjectName(u"page_abrir")
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Criando o widget central------------------------------------------------
        self.widget = QWidget(page_abrir)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, page_abrir.width(), page_abrir.height()))
        # Criando o layout horizontal principal ----------------------------------
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # Tamanho das fontes
        font = QFont()
        font.setPointSize(14)

        self.verticalLayout_abrir = QVBoxLayout()
        self.verticalLayout_abrir.setObjectName(u"verticalLayout_abrir")

        # Label e LineEdit para CPF--------------------------------------------------
        self.label_cpf = QLabel(self.widget)
        self.label_cpf.setObjectName(u"label_cpf")
        self.label_cpf.setFont(font)

        self.verticalLayout_abrir.addWidget(self.label_cpf)
        self.lineEdit_cpf = QLineEdit(self.widget)
        self.lineEdit_cpf.setObjectName(u"lineEdit_cpf")
        self.lineEdit_cpf.setMinimumSize(QSize(150, 0))
        self.lineEdit_cpf.setMaximumSize(QSize(150, 16777215))
        self.lineEdit_cpf.setFont(font)

        def cpf_focus_in_event(event):
            QLineEdit.focusInEvent(self.lineEdit_cpf, event)
            # Espera 0ms e só então move o cursor (depois do clique)
            QTimer.singleShot(0, lambda: self.lineEdit_cpf.setCursorPosition(0))

        self.lineEdit_cpf.focusInEvent = cpf_focus_in_event
        self.verticalLayout_abrir.addWidget(self.lineEdit_cpf)

        # Label e SpinBox para quantidade de hospedes-------------------------------
        self.label_qtd_hospedes = QLabel(self.widget)
        self.label_qtd_hospedes.setObjectName(u"label_qtd_hospedes")
        self.label_qtd_hospedes.setFont(font)
        self.label_qtd_hospedes.setText('Quantidade de hospedes:')
        self.verticalLayout_abrir.addWidget(self.label_qtd_hospedes)

        self.spinBox_qtd_hospedes = QSpinBox(self.widget)
        self.spinBox_qtd_hospedes.setObjectName(u"spinBox_qtd_hospedes")
        self.spinBox_qtd_hospedes.setMaximumWidth(80)
        self.spinBox_qtd_hospedes.setFont(font)
        self.spinBox_qtd_hospedes.setMinimum(1)  # Define o valor mínimo
        self.spinBox_qtd_hospedes.setMaximum(5)  # Define o valor máximo
        self.spinBox_qtd_hospedes.setValue(1)  # Define o valor padrão
        self.verticalLayout_abrir.addWidget(self.spinBox_qtd_hospedes)

        # Label e DateEdit para data de saída----------------------------------------
        self.label_prev_saida = QLabel(self.widget)
        self.label_prev_saida.setObjectName(u"label_prev_saida")
        self.label_prev_saida.setFont(font)

        self.verticalLayout_abrir.addWidget(self.label_prev_saida)

        self.dateEdit_prev_saida = QDateEdit(self.widget)
        self.dateEdit_prev_saida.setObjectName(u"dateEdit_prev_saida")
        self.dateEdit_prev_saida.setMaximumWidth(150)
        self.dateEdit_prev_saida.setDate(QDate.currentDate())
        self.dateEdit_prev_saida.setFont(font)

        self.verticalLayout_abrir.addWidget(self.dateEdit_prev_saida)

        # Label e Tabela para quartos disponíveis--------------------------------
        self.label_quartos = QLabel(self.widget)
        self.label_quartos.setObjectName(u"label_quartos")
        self.label_quartos.setFont(font)

        self.verticalLayout_abrir.addWidget(self.label_quartos)

        # Cria um layout para a tabela de quartos disponíveis
        self.tableWidget_quartos = QTableWidget(self.widget)
        self.tableWidget_quartos.setObjectName(u"tableWidget_quartos")
        self.tableWidget_quartos.setColumnCount(2) # Define o número de colunas
        self.tableWidget_quartos.setRowCount(0)  # Inicialmente sem linhas
        self.tableWidget_quartos.setColumnWidth(0, 50)  # Ajusta a largura da primeira coluna
        self.tableWidget_quartos.horizontalHeader().setStretchLastSection(True)  # Faz coluna tipo preencher o espaço
        self.tableWidget_quartos.setHorizontalHeaderLabels(['Nº', 'Tipo']) # Define os rótulos das colunas
        self.tableWidget_quartos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Seleciona linhas inteiras
        self.tableWidget_quartos.setSelectionMode(QTableWidget.SelectionMode.SingleSelection) # Seleciona apenas uma linha
        self.tableWidget_quartos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Desabilita edição
        self.tableWidget_quartos.setAlternatingRowColors(True)  # Cores alternadas para as linhas
        # Get available rooms directly from database
        Session = sessionmaker(bind=db.engine)
        session = Session()
        quartos = session.query(Quarto).filter(Quarto.disponivel == True).all()
        session.close()

        # Add rooms to the table
        for quarto in quartos:
            row = self.tableWidget_quartos.rowCount()
            self.tableWidget_quartos.insertRow(row)
            self.tableWidget_quartos.setItem(row, 0, QTableWidgetItem(str(quarto.numero)))
            self.tableWidget_quartos.setItem(row, 1, QTableWidgetItem(quarto.tipo))

        self.verticalLayout_abrir.addWidget(self.tableWidget_quartos)

        # Add "Abrir" button with horizontal centering
        horizontalLayout_abrir = QHBoxLayout()
        horizontalLayout_abrir.addStretch() # Adiciona espaçador à esquerda
        
        self.pushButton_abrir = QPushButton(self.widget)
        self.pushButton_abrir.setObjectName(u"pushButton_abrir")
        self.pushButton_abrir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_abrir.setMaximumWidth(150)
        self.pushButton_abrir.setFont(font)

        self.pushButton_abrir.clicked.connect(self.button_abrir_clicked)  # Conecta o botão à função de abrir
        
        horizontalLayout_abrir.addWidget(self.pushButton_abrir)
        horizontalLayout_abrir.addStretch()# Adiciona espaçador à direita
        
        self.verticalLayout_abrir.addLayout(horizontalLayout_abrir)
        
        self.verticalLayout_abrir.addWidget(self.pushButton_abrir)
        self.horizontalLayout.addLayout(self.verticalLayout_abrir)


        # Separador da tela de abrir | tela de buscar-----------------------------------------------------
        self.line_separador = QFrame(self.widget)
        self.line_separador.setObjectName(u"line_separador")
        self.line_separador.setFrameShape(QFrame.Shape.VLine)
        self.line_separador.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_separador)
        
        # ----------------------------Cria um layout para buscar hospedes------------------------------------
        ## Cria um layout vertical para a busca de hospedes
        self.verticalLayout_buscar = QVBoxLayout()
        self.verticalLayout_buscar.setObjectName(u"verticalLayout_buscar")

        # Label buscar hospedes----------------------------------
        self.label_buscar = QLabel(self.widget)
        self.label_buscar.setObjectName(u"label_buscar")
        self.label_buscar.setFont(font)
        self.label_buscar.setAlignment(Qt.AlignCenter)

        # Adiciona a label ao layout
        self.verticalLayout_buscar.addWidget(self.label_buscar)

        # Linha de separação 
        self.line_separador_busca = QFrame(self.widget)
        self.line_separador_busca.setObjectName(u"line_separador_busca")
        self.line_separador_busca.setFrameShape(QFrame.Shape.HLine)
        self.line_separador_busca.setFrameShadow(QFrame.Shadow.Sunken)
        
        # Adiciona a linha de separação ao layout
        self.verticalLayout_buscar.addWidget(self.line_separador_busca)

        # Line edit para por o nome do hospede a ser buscado ----------------------
        self.lineEdit_nome = QLineEdit(self.widget)
        self.lineEdit_nome.setObjectName(u"lineEdit_nome")
        self.lineEdit_nome.setPlaceholderText('Nome do hospede')
        self.lineEdit_nome.setFont(font)

        # Adicionando o line edit ao layout
        self.verticalLayout_buscar.addWidget(self.lineEdit_nome)

        # Layout do botão procurar
        self.horizontalLayout_2 = QHBoxLayout()

        # Adicionando um espaço a esquerda do botao
        self.horizontalLayout_2.addStretch()

        # Cria botão procurar
        self.pushButton_procurar = QPushButton(self.widget)
        self.pushButton_procurar.setObjectName(u"pushButton_procurar")
        self.pushButton_procurar.setMaximumSize(QSize(100, 16777215))
        self.pushButton_procurar.setMinimumWidth(150)
        self.pushButton_procurar.setFont(font)
        self.pushButton_procurar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Adicionando o botão ao layout
        self.horizontalLayout_2.addWidget(self.pushButton_procurar)

        # Adicionando um espaço a direita do botao
        self.horizontalLayout_2.addStretch()

        # Adiciona o layout do botão procurar ao layout vertical
        self.verticalLayout_buscar.addLayout(self.horizontalLayout_2)

        # ----------------------------------------------ARRUMAR-----------------------------------------------------------------------
        # Criar tabela de hospedes encontrados
        self.tableWidget_hospedes = QTableWidget(self.widget)
        self.tableWidget_hospedes.setObjectName(u"tableWidget_hospedes")
        self.tableWidget_hospedes.setColumnCount(3) # Define o número de colunas
        self.tableWidget_hospedes.setRowCount(0) # Inicialmente sem linhas
        self.tableWidget_hospedes.horizontalHeader().setStretchLastSection(True) # Faz coluna cpf preencher o espaço
        self.tableWidget_hospedes.setHorizontalHeaderLabels(['Nome', 'Telefone', 'CPF'])
        self.tableWidget_hospedes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Seleciona linhas inteiras
        self.tableWidget_hospedes.setSelectionMode(QTableWidget.SelectionMode.SingleSelection) # Seleciona apenas uma linha
        self.tableWidget_hospedes.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Desabilita edição
        self.tableWidget_hospedes.setAlternatingRowColors(True) # Cores alternadas para as linhas
        self.tableWidget_hospedes.setSortingEnabled(True) # Habilita a ordenação da tabela
        # Ajusta o tamanho das colunas
        header = self.tableWidget_hospedes.horizontalHeader()
        for i in range(5):
            header.setSectionResizeMode(i, QHeaderView.Stretch)  

        # Adiciona a tabela de hospedes ao layout
        self.verticalLayout_buscar.addWidget(self.tableWidget_hospedes)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_buscar.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_buscar)


        self.retranslateUi(page_abrir)

        QMetaObject.connectSlotsByName(page_abrir)

        layout.addWidget(self.widget)
    # setupUi

    def retranslateUi(self, page_abrir):
        self.label_cpf.setText(QCoreApplication.translate("page_abrir", u"CPF:", None))
        self.lineEdit_cpf.setInputMask(QCoreApplication.translate("page_abrir", u"000.000.000-00;_", None))
        self.lineEdit_cpf.setText(QCoreApplication.translate("page_abrir", u"..-", None))
        self.lineEdit_cpf.setPlaceholderText(QCoreApplication.translate("page_abrir", u"000.000.000-00", None))
        self.label_prev_saida.setText(QCoreApplication.translate("page_abrir", u"Prev. Sa\u00edda:", None))
        self.label_quartos.setText(QCoreApplication.translate("page_abrir", u"Quartos disponiveis:", None))

        self.pushButton_abrir.setText(QCoreApplication.translate("page_abrir", u"Abrir", None))
        self.label_buscar.setText(QCoreApplication.translate("page_abrir", u"Buscar", None))
        self.pushButton_procurar.setText(QCoreApplication.translate("page_abrir", u"Procurar", None))

    def button_abrir_clicked(self):
        # Pega o quarto selecionado
        row = self.tableWidget_quartos.currentRow()
        if row == -1:
            return
        quarto_num = self.tableWidget_quartos.item(row, 0).text()

        # Pega o CPF do hospede
        cpf = self.lineEdit_cpf.text()

        # Pega a data de saída
        data_saida = self.dateEdit_prev_saida.date()
        data_saida = datetime(data_saida.year(), data_saida.month(), data_saida.day())
        # Converte a data para o formato correto
        data_saida = data_saida.strftime('%Y-%m-%d')
        data_saida = datetime.strptime(data_saida, '%Y-%m-%d')

        # Pega a quantidade de hospedes
        qtd_hospedes = self.spinBox_qtd_hospedes.value()

        # Cria uma nova hospedagem
        with sessionmaker(bind=db.engine)() as session:
            hospede = session.query(Hospede).filter(Hospede.cpf == cpf).first()
            if not hospede:
                QMessageBox.warning(self, "Erro", "Hóspede não encontrado.")
                return
            # Mensagem de confirmação
            nome = hospede.nome
            QMessageBox.information(self, "Sucesso", f"Hospedagem criada para {nome}")
            create_hospedagem(cpf, quarto_num, data_saida, qtd_hospedes)

        # Atualiza a tabela de quartos disponíveis
        # Limpar entradas
        self.lineEdit_cpf.setText("..-")
        self.dateEdit_prev_saida.setDate(QDate.currentDate())
        self.spinBox_qtd_hospedes.setValue(1)

        # Obter os nomes dos hospedes para atualizar a tabela
        with sessionmaker(bind=db.engine)() as session:
            # Update available rooms table
            self.tableWidget_quartos.setRowCount(0)
            quartos = session.query(Quarto).filter(Quarto.disponivel == True).all()
            for quarto in quartos:
                row = self.tableWidget_quartos.rowCount()
                self.tableWidget_quartos.insertRow(row)
                self.tableWidget_quartos.setItem(row, 0, QTableWidgetItem(str(quarto.numero)))
                self.tableWidget_quartos.setItem(row, 1, QTableWidgetItem(quarto.tipo))