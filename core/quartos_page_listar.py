# core/hotel_core.py

# Supondo que 'operations' seja um pacote com os módulos de operações
from operations.Ui.quartos_operations import listar_quartos as _listar_quartos_db
from operations.Ui.hospedagem_operations import listar_hospedagens as _listar_hospedagens_db

class Core_page_listar:
    def __init__(self):
        pass

    def listar_quartos(self):
        """Busca a lista de quartos."""
        return _listar_quartos_db()

    def listar_hospedagens(self):
        """Busca a lista de hospedagens."""
        return _listar_hospedagens_db()