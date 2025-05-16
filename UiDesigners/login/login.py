# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(571, 376)
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(80, 50, 411, 231))
        font = QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_usuario = QLabel(self.groupBox)
        self.label_usuario.setObjectName(u"label_usuario")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_usuario)

        self.lineEdit__usuario = QLineEdit(self.groupBox)
        self.lineEdit__usuario.setObjectName(u"lineEdit__usuario")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit__usuario)

        self.label_senha = QLabel(self.groupBox)
        self.label_senha.setObjectName(u"label_senha")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_senha)

        self.lineEdit_senha = QLineEdit(self.groupBox)
        self.lineEdit_senha.setObjectName(u"lineEdit_senha")
        self.lineEdit_senha.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_senha)


        self.verticalLayout.addLayout(self.formLayout)

        self.label_feedbeck = QLabel(self.groupBox)
        self.label_feedbeck.setObjectName(u"label_feedbeck")
        self.label_feedbeck.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_feedbeck)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_sair = QPushButton(self.groupBox)
        self.pushButton_sair.setObjectName(u"pushButton_sair")
        self.pushButton_sair.setFont(font)
        self.pushButton_sair.setStyleSheet(u"background-color: rgb(170, 0, 0);")

        self.horizontalLayout.addWidget(self.pushButton_sair)

        self.pushButton__entrar = QPushButton(self.groupBox)
        self.pushButton__entrar.setObjectName(u"pushButton__entrar")
        self.pushButton__entrar.setFont(font)
        self.pushButton__entrar.setStyleSheet(u"background-color: rgb(0, 85, 0);")

        self.horizontalLayout.addWidget(self.pushButton__entrar)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Horizonte Prime", None))
        self.label_usuario.setText(QCoreApplication.translate("Form", u"Usu\u00e1rio:", None))
        self.lineEdit__usuario.setPlaceholderText("")
        self.label_senha.setText(QCoreApplication.translate("Form", u"Senha:", None))
        self.lineEdit_senha.setInputMask("")
        self.lineEdit_senha.setPlaceholderText("")
        self.label_feedbeck.setText("")
        self.pushButton_sair.setText(QCoreApplication.translate("Form", u"Sair", None))
        self.pushButton__entrar.setText(QCoreApplication.translate("Form", u"Entrar", None))
    # retranslateUi

