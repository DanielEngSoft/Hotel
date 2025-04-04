# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_abrir.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_page_abrir(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def setupUi(self, page_abrir):
        if not page_abrir.objectName():
            page_abrir.setObjectName(u"page_abrir")
        page_abrir.resize(776, 473)
        page_abrir.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        page_abrir.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.widget = QWidget(page_abrir)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(40, 50, 721, 400))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_abrir = QVBoxLayout()
        self.verticalLayout_abrir.setObjectName(u"verticalLayout_abrir")
        self.label_cpf = QLabel(self.widget)
        self.label_cpf.setObjectName(u"label_cpf")
        font = QFont()
        font.setPointSize(14)
        self.label_cpf.setFont(font)

        self.verticalLayout_abrir.addWidget(self.label_cpf)

        self.lineEdit_cpf = QLineEdit(self.widget)
        self.lineEdit_cpf.setObjectName(u"lineEdit_cpf")
        self.lineEdit_cpf.setMinimumSize(QSize(150, 0))
        self.lineEdit_cpf.setMaximumSize(QSize(150, 16777215))
        self.lineEdit_cpf.setFont(font)
        from PySide6.QtCore import QTimer
        def cpf_focus_in_event(event):
            QLineEdit.focusInEvent(self.lineEdit_cpf, event)
            # Espera 0ms e só então move o cursor (depois do clique)
            QTimer.singleShot(0, lambda: self.lineEdit_cpf.setCursorPosition(0))

        self.lineEdit_cpf.focusInEvent = cpf_focus_in_event

        self.verticalLayout_abrir.addWidget(self.lineEdit_cpf)
        self.label_prev_saida = QLabel(self.widget)
        self.label_prev_saida.setObjectName(u"label_prev_saida")
        self.label_prev_saida.setFont(font)

        self.verticalLayout_abrir.addWidget(self.label_prev_saida)

        self.dateEdit_prev_saida = QDateEdit(self.widget)
        self.dateEdit_prev_saida.setObjectName(u"dateEdit_prev_saida")
        self.dateEdit_prev_saida.setFont(font)

        self.verticalLayout_abrir.addWidget(self.dateEdit_prev_saida)

        self.label_quartos = QLabel(self.widget)
        self.label_quartos.setObjectName(u"label_quartos")
        self.label_quartos.setFont(font)

        self.verticalLayout_abrir.addWidget(self.label_quartos)

        self.tableWidget_quartos = QTableWidget(self.widget)
        if (self.tableWidget_quartos.columnCount() < 2):
            self.tableWidget_quartos.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.tableWidget_quartos.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignTrailing|Qt.AlignVCenter);
        self.tableWidget_quartos.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tableWidget_quartos.rowCount() < 5):
            self.tableWidget_quartos.setRowCount(5)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_quartos.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_quartos.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_quartos.setVerticalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_quartos.setVerticalHeaderItem(3, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_quartos.setVerticalHeaderItem(4, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_quartos.setItem(0, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_quartos.setItem(0, 1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_quartos.setItem(1, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_quartos.setItem(1, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_quartos.setItem(2, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_quartos.setItem(2, 1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_quartos.setItem(3, 0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_quartos.setItem(3, 1, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_quartos.setItem(4, 0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_quartos.setItem(4, 1, __qtablewidgetitem16)
        self.tableWidget_quartos.setObjectName(u"tableWidget_quartos")
        self.tableWidget_quartos.setMinimumSize(QSize(0, 0))
        self.tableWidget_quartos.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout_abrir.addWidget(self.tableWidget_quartos)

        self.pushButton_abrir = QPushButton(self.widget)
        self.pushButton_abrir.setObjectName(u"pushButton_abrir")
        self.pushButton_abrir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout_abrir.addWidget(self.pushButton_abrir)


        self.horizontalLayout.addLayout(self.verticalLayout_abrir)

        self.line_separador = QFrame(self.widget)
        self.line_separador.setObjectName(u"line_separador")
        self.line_separador.setFrameShape(QFrame.Shape.VLine)
        self.line_separador.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_separador)

        self.verticalLayout_buscar = QVBoxLayout()
        self.verticalLayout_buscar.setObjectName(u"verticalLayout_buscar")
        self.label_buscar = QLabel(self.widget)
        self.label_buscar.setObjectName(u"label_buscar")
        self.label_buscar.setFont(font)

        self.verticalLayout_buscar.addWidget(self.label_buscar)

        self.line_separador_busca = QFrame(self.widget)
        self.line_separador_busca.setObjectName(u"line_separador_busca")
        self.line_separador_busca.setFrameShape(QFrame.Shape.HLine)
        self.line_separador_busca.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_buscar.addWidget(self.line_separador_busca)

        self.label_nome = QLabel(self.widget)
        self.label_nome.setObjectName(u"label_nome")
        self.label_nome.setFont(font)

        self.verticalLayout_buscar.addWidget(self.label_nome)

        self.lineEdit_nome = QLineEdit(self.widget)
        self.lineEdit_nome.setObjectName(u"lineEdit_nome")
        self.lineEdit_nome.setMinimumSize(QSize(0, 0))
        self.lineEdit_nome.setMaximumSize(QSize(9999, 16777215))
        self.lineEdit_nome.setFont(font)

        self.verticalLayout_buscar.addWidget(self.lineEdit_nome)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_procurar = QPushButton(self.widget)
        self.pushButton_procurar.setObjectName(u"pushButton_procurar")
        self.pushButton_procurar.setMaximumSize(QSize(100, 16777215))
        self.pushButton_procurar.setFont(font)
        self.pushButton_procurar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.pushButton_procurar)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_buscar.addLayout(self.horizontalLayout_2)

        self.tableWidget_hospedes = QTableWidget(self.widget)
        if (self.tableWidget_hospedes.columnCount() < 3):
            self.tableWidget_hospedes.setColumnCount(3)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_hospedes.setHorizontalHeaderItem(0, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_hospedes.setHorizontalHeaderItem(1, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_hospedes.setHorizontalHeaderItem(2, __qtablewidgetitem19)
        if (self.tableWidget_hospedes.rowCount() < 1):
            self.tableWidget_hospedes.setRowCount(1)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget_hospedes.setVerticalHeaderItem(0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget_hospedes.setItem(0, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget_hospedes.setItem(0, 1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget_hospedes.setItem(0, 2, __qtablewidgetitem23)
        self.tableWidget_hospedes.setObjectName(u"tableWidget_hospedes")
        self.tableWidget_hospedes.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout_buscar.addWidget(self.tableWidget_hospedes)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_buscar.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_buscar)


        self.retranslateUi(page_abrir)

        QMetaObject.connectSlotsByName(page_abrir)
    # setupUi

    def retranslateUi(self, page_abrir):
        page_abrir.setWindowTitle(QCoreApplication.translate("page_abrir", u"Form", None))
        self.label_cpf.setText(QCoreApplication.translate("page_abrir", u"CPF:", None))
        self.lineEdit_cpf.setInputMask(QCoreApplication.translate("page_abrir", u"000.000.000-00;_", None))
        self.lineEdit_cpf.setText(QCoreApplication.translate("page_abrir", u"..-", None))
        self.lineEdit_cpf.setPlaceholderText(QCoreApplication.translate("page_abrir", u"000.000.000-00", None))
        self.label_prev_saida.setText(QCoreApplication.translate("page_abrir", u"Prev. Sa\u00edda:", None))
        self.label_quartos.setText(QCoreApplication.translate("page_abrir", u"Quartos disponiveis:", None))
        ___qtablewidgetitem = self.tableWidget_quartos.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("page_abrir", u"N\u00b0", None));
        ___qtablewidgetitem1 = self.tableWidget_quartos.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("page_abrir", u"Tipo", None));

        __sortingEnabled = self.tableWidget_quartos.isSortingEnabled()
        self.tableWidget_quartos.setSortingEnabled(False)
        ___qtablewidgetitem2 = self.tableWidget_quartos.item(0, 0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("page_abrir", u"01", None));
        ___qtablewidgetitem3 = self.tableWidget_quartos.item(0, 1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("page_abrir", u"Casal + Solteiro", None));
        ___qtablewidgetitem4 = self.tableWidget_quartos.item(1, 0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("page_abrir", u"02", None));
        ___qtablewidgetitem5 = self.tableWidget_quartos.item(1, 1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("page_abrir", u"Caslal", None));
        ___qtablewidgetitem6 = self.tableWidget_quartos.item(2, 0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("page_abrir", u"03", None));
        ___qtablewidgetitem7 = self.tableWidget_quartos.item(2, 1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("page_abrir", u"3 Solteiro", None));
        ___qtablewidgetitem8 = self.tableWidget_quartos.item(3, 0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("page_abrir", u"109", None));
        ___qtablewidgetitem9 = self.tableWidget_quartos.item(3, 1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("page_abrir", u"Casal + 2 Solteiro", None));
        ___qtablewidgetitem10 = self.tableWidget_quartos.item(4, 0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("page_abrir", u"110", None));
        ___qtablewidgetitem11 = self.tableWidget_quartos.item(4, 1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("page_abrir", u"Casal", None));
        self.tableWidget_quartos.setSortingEnabled(__sortingEnabled)

        self.pushButton_abrir.setText(QCoreApplication.translate("page_abrir", u"Abrir", None))
        self.label_buscar.setText(QCoreApplication.translate("page_abrir", u"Buscar", None))
        self.label_nome.setText(QCoreApplication.translate("page_abrir", u"Nome:", None))
        self.pushButton_procurar.setText(QCoreApplication.translate("page_abrir", u"Procurar", None))
        ___qtablewidgetitem12 = self.tableWidget_hospedes.horizontalHeaderItem(0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("page_abrir", u"Nome", None));
        ___qtablewidgetitem13 = self.tableWidget_hospedes.horizontalHeaderItem(1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("page_abrir", u"Telefone", None));
        ___qtablewidgetitem14 = self.tableWidget_hospedes.horizontalHeaderItem(2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("page_abrir", u"CPF", None));

        __sortingEnabled1 = self.tableWidget_hospedes.isSortingEnabled()
        self.tableWidget_hospedes.setSortingEnabled(False)
        ___qtablewidgetitem15 = self.tableWidget_hospedes.item(0, 0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("page_abrir", u"Daniel", None));
        ___qtablewidgetitem16 = self.tableWidget_hospedes.item(0, 1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("page_abrir", u"(89)99906-3568", None));
        ___qtablewidgetitem17 = self.tableWidget_hospedes.item(0, 2)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("page_abrir", u"050.897.993-50", None));
        self.tableWidget_hospedes.setSortingEnabled(__sortingEnabled1)

    # retranslateUi

