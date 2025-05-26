# PALETA DE CORES

#----- MENUS -----#
verde_escuro = "#05452f"
azul_escuro = "#2c3e50"

#----- BOTÕES -----#
btn_verde = "#4E9A06"
btn_vermelho = "#A52A2A"
btn_branco = "#ffffff"
btn_transparente = "transparent"

#----- BTN HOVER -----#
btn_verde_hover = "#09572a"
btn_vermelho_hover = "#800000"
btn_branco_hover = "#e0e0e0"
btn_transparente_hover = "#3d566e"

#----- BTN PRESSED -----#
btn_verde_pressed = "#219653"
btn_vermelho_pressed = "#a93226"
btn_branco_pressed = "#A9A9A9"
btn_transparente_pressed = "#0000007F"



def style_label_menu_lateral():
    return f"""
    QListWidget {{
        background-color: {azul_escuro};
        color: white;
        border: none;
        padding: 10px;
        font-size: 16px;
        outline: 0;
    }}

    QListWidget::item {{
        background-color: transparent;
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
    }}

    QListWidget::item:hover {{
        background-color: {btn_transparente_hover};
    }}
    QListWidget::item:selected {{
        background-color: {verde_escuro};
        border-bottom: 2px solid {btn_verde};
        color: white;
        border-radius: 0px;
        padding: 5px;
        outline: 0;
    }}
    """

def nome_menu_superior():
    return """
    QLabel {
        font-size: 22px;
        color: white;
        font-weight: bold;
        padding-left: 20px;
    }
    """

        # color: #ecf0f1;

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
    return f"""
        QPushButton {{
            background-color: {btn_vermelho};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {btn_vermelho_hover};
        }}
        QPushButton:pressed {{
            background-color: {btn_vermelho_pressed};
        }}
    """

def style_botao_verde():
    return f"""
        QPushButton {{
            background-color: {btn_verde};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {btn_verde_hover};
        }}
        QPushButton:pressed {{
            background-color: {btn_verde_pressed};
        }}
    """

def style_botao_branco():
    return f"""
        QPushButton {{
            background-color: {btn_branco};
            color: black;
            border: none;
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {btn_branco_hover};
        }}
        QPushButton:pressed {{
            background-color: {btn_branco_pressed};
        }}
    """

def style_botao_vermelho():
    return f"""
        QPushButton {{
            background-color: {btn_vermelho};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {btn_vermelho_hover};
        }}
        QPushButton:pressed {{
            background-color: {btn_vermelho_pressed};
        }}
    """

def style_botao_transparente():
    return f"""
        QPushButton {{
            background-color: {btn_transparente};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {verde_escuro};
        }}
        QPushButton:pressed {{
            background-color: {btn_transparente_pressed};
        }}
    """

def style_groupbox():
    return """
        QGroupBox {
            font-size: 16px;
            font-weight: bold;
            color: #fff;
            border: 1px solid white;
            border-radius: 0px;
            padding: 50px;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
    """

def style_groupbox_abrir():
    return """
        QGroupBox {
            font-size: 16px;
            font-weight: bold;
            color: #fff;
            border: 1px solid white;
            border-radius: 0px;
            padding: 10px;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }
    """

def style_groupbox_login():
    return """
        QGroupBox {
            font-size: 16px;
            font-weight: bold;
            color: #fff;
            border: 1px solid white;
            border-radius: 0px;
            padding: 10px;
            margin-left: 50px;
            margin-right: 50px;
            margin-top: 50px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            top: 40px;
            left: 60px;
        }
    """

def menu_superior_pages():
    return f"""
            QListWidget {{
                background-color: {azul_escuro};
                border: none;
                padding-left: 10px;
                outline: 0;
            }}
            QListWidget::item {{
                color: {btn_branco};
                padding: 0px 28px;
                border-bottom: 2px solid transparent;
            }}
            QListWidget::item:hover {{
                background-color: {btn_transparente_hover};
            }}
            QListWidget::item:selected {{
                border-bottom: 2px solid {btn_verde};
            }}
        """

def tabelas():
    return f"""
        QTableWidget{{
            outline: 0;
            background-color: {azul_escuro};
        }}
        QTableWidget::item{{
            background-color: {verde_escuro};
        }}
        QTableWidget::item:selected {{
            background-color: {btn_transparente_hover};
        }}
        QTableWidget::item:hover {{
            background-color: {btn_transparente_hover};
            color: white; 
        }}
        QHeaderView::section {{
            background-color: {azul_escuro};
            color: white;
            font-size: 14px;
            border: none;
        }}
    """

def tabela_listar():
    return f"""
        QTableWidget{{
            outline: 0;
        }}
        QTableWidget::item:hover {{
            background-color: {btn_transparente_hover};
            color: white;    
        }}
        QTableWidget::item:selected {{
            background-color: {btn_transparente_hover};
        }}
        """

def btn_quarto_livre():
    return f"""
        QPushButton {{
            background-color: {verde_escuro};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {btn_verde_hover};
        }}
        QPushButton:pressed {{
            background-color: {btn_verde_pressed};
        }}
    """

def btn_quarto_ocupado():
    return f"""
        QPushButton {{
            background-color: {btn_vermelho};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {btn_vermelho_hover};
        }}
        QPushButton:pressed {{
            background-color: {btn_vermelho_pressed};
        }}
    """