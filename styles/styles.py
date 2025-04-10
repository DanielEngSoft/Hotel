def style_label_menu_lateral():
    return """
    QListWidget {
        background-color: #2c3e50;
        color: white;
        border: none;
        padding: 10px;
        font-size: 16px;
    }

    QListWidget::item {
        background-color: transparent;
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
    }

    QListWidget::item:selected {
        background-color: #34495e;
        color: #ffffff;
    }

    QListWidget::item:hover {
        background-color: #3d566e;
    }
    QListWidget::item:selected {
        background-color: #4E9A06;
        color: white;
        border-radius: 5px;
        padding: 5px;
    }
    """


def nome_menu_superior():
    return """
    QLabel {
        font-size: 22px;
        font-weight: bold;
        color: #ecf0f1;
        padding-left: 20px;
    }
    """


def data_menu_superior():
    return """
    QLabel {
        font-size: 14px;
        color: #bdc3c7;
    }
    """


def hora_menu_superior():
    return """
    QLabel {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
    }
    """
def style_botao_sair():
    return """
        QPushButton {
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #c0392b;
        }
        QPushButton:pressed {
            background-color: #a93226;
        }
    """

def style_botao_verde():
    return """
        QPushButton {
            background-color: #2ecc71;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #27ae60;
        }
        QPushButton:pressed {
            background-color: #219653;
        }
    """
def style_botao_branco():
    return """
        QPushButton {
            background-color: #fff;
            color: black;
            border: none;
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #27ae60;
        }
        QPushButton:pressed {
            background-color: #219653;
        }
    """

def style_groupbox():
    return """
        QGroupBox {
            font-size: 16px;
            font-weight: bold;
            color: #fff;
            border: 1px solid #bdc3c7;
            border-radius: 10px;
            padding: 50px;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
    """
