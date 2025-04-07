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
def style_page_abrir_hospedagem():
    return """
        QWidget {
            background-color: #f7f7f7;
            font-family: 'Segoe UI';
        }

        QLabel {
            color: #333;
        }

        QLineEdit, QDateEdit, QSpinBox {
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 6px;
        }

        QLineEdit:focus, QDateEdit:focus, QSpinBox:focus {
            border: 1px solid #0078d7;
        }

        QPushButton {
            background-color: #0078d7;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
        }

        QPushButton:hover {
            background-color: #005a9e;
        }

        QTableWidget {
            background-color: #fff;
            alternate-background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-radius: 8px;
        }

        QHeaderView::section {
            background-color: #0078d7;
            color: white;
            padding: 4px;
            border: none;
        }

        QTableWidget::item:hover {
            background-color: #dbe9f7;
        }

        QFrame {
            background-color: transparent;
        }

        QScrollBar:vertical {
            background: #f0f0f0;
            width: 10px;
            margin: 0px 0px 0px 0px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical {
            background: #ccc;
            border-radius: 5px;
            min-height: 20px;
        }

        QScrollBar::handle:vertical:hover {
            background: #999;
        }
    """