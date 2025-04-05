# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_cadastrar.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(1000, 655)
        self.widget = QWidget(Frame)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(240, 110, 671, 461))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label_cpf = QLabel(self.widget)
        self.label_cpf.setObjectName(u"label_cpf")
        self.label_cpf.setMinimumSize(QSize(100, 0))
        self.label_cpf.setMaximumSize(QSize(100, 16777215))
        font = QFont()
        font.setPointSize(14)
        self.label_cpf.setFont(font)
        self.label_cpf.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_cpf)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 30))
        self.lineEdit.setMaximumSize(QSize(145, 16777215))
        self.lineEdit.setFont(font)
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalSpacer_cpf = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_cpf)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_nome = QLabel(self.widget)
        self.label_nome.setObjectName(u"label_nome")
        self.label_nome.setMinimumSize(QSize(100, 0))
        self.label_nome.setMaximumSize(QSize(100, 16777215))
        self.label_nome.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_nome)

        self.lineEdit_2 = QLineEdit(self.widget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(0, 30))
        self.lineEdit_2.setMaximumSize(QSize(400, 16777215))
        self.lineEdit_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.lineEdit_2)

        self.horizontalSpacer_nome = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_nome)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_telefone = QLabel(self.widget)
        self.label_telefone.setObjectName(u"label_telefone")
        self.label_telefone.setMinimumSize(QSize(100, 0))
        self.label_telefone.setMaximumSize(QSize(100, 16777215))
        self.label_telefone.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_telefone)

        self.lineEdit_3 = QLineEdit(self.widget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(0, 30))
        self.lineEdit_3.setMaximumSize(QSize(145, 16777215))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(False)
        self.lineEdit_3.setFont(font1)
        self.lineEdit_3.setCursorPosition(0)
        self.lineEdit_3.setCursorMoveStyle(Qt.CursorMoveStyle.LogicalMoveStyle)

        self.horizontalLayout_3.addWidget(self.lineEdit_3)

        self.horizontalSpacer_telefone = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_telefone)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.comboBox = QComboBox(self.widget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setFont(font)

        self.horizontalLayout_6.addWidget(self.comboBox)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(24, 0))

        self.horizontalLayout_6.addWidget(self.label_2)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.lineEdit_5 = QLineEdit(self.widget)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMinimumSize(QSize(150, 0))
        self.lineEdit_5.setFont(font)

        self.horizontalLayout_6.addWidget(self.lineEdit_5)

        self.horizontalSpacer_endereco = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_endereco)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(100, 0))
        self.label_4.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_4 = QLineEdit(self.widget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMinimumSize(QSize(0, 30))
        self.lineEdit_4.setFont(font)

        self.horizontalLayout_4.addWidget(self.lineEdit_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_lbutton = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_lbutton)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFont(font)

        self.horizontalLayout_5.addWidget(self.pushButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.label_cpf.setText(QCoreApplication.translate("Frame", u"CPF:", None))
        self.lineEdit.setInputMask(QCoreApplication.translate("Frame", u"000.000.000-00;_", None))
        self.lineEdit.setText(QCoreApplication.translate("Frame", u"..-", None))
        self.label_nome.setText(QCoreApplication.translate("Frame", u"Nome:", None))
        self.label_telefone.setText(QCoreApplication.translate("Frame", u"Telefone:", None))
        self.lineEdit_3.setInputMask(QCoreApplication.translate("Frame", u"(00)00000-0000;_", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Frame", u"PI", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Frame", u"MA", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Frame", u"CE", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Frame", u"TO", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Frame", u"PA", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Frame", u"PR", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("Frame", u"BA", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("Frame", u"PB", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("Frame", u"SP", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("Frame", u"RJ", None))
        self.comboBox.setItemText(10, QCoreApplication.translate("Frame", u"GO", None))
        self.comboBox.setItemText(11, QCoreApplication.translate("Frame", u"DF", None))
        self.comboBox.setItemText(12, QCoreApplication.translate("Frame", u"--", None))

        self.label_2.setText("")
        self.label.setText("")
        self.lineEdit_5.setInputMask("")
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("Frame", u"Cidade", None))
        self.label_4.setText(QCoreApplication.translate("Frame", u"Empresa:", None))
        self.pushButton.setText(QCoreApplication.translate("Frame", u"Cadastrar", None))
    # retranslateUi

