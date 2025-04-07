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