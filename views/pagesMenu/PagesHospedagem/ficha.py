from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class JanelaHospedagem(QWidget):
    def __init__(self, hospedagem, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Hospedagem - Quarto {getattr(hospedagem.quarto, 'numero', 'Desconhecido')}")
        self.setMinimumSize(350, 200)
        self.setAttribute(Qt.WA_DeleteOnClose)  # Libera memória ao fechar

        print(f"JanelaHospedagem: {hospedagem.id}")
        layout = QVBoxLayout(self)

        nome_hospede = getattr(hospedagem.hospede, "nome", "Desconhecido")
        layout.addWidget(QLabel(f"Hóspede: {nome_hospede}"))

        entrada = hospedagem.data_entrada.strftime('%d/%m/%Y') if hospedagem.data_entrada else "Não informado"
        saida = hospedagem.data_saida.strftime('%d/%m/%Y') if hospedagem.data_saida else "Não informado"
        layout.addWidget(QLabel(f"Check-in: {entrada}"))
        layout.addWidget(QLabel(f"Check-out: {saida}"))

        numero_quarto = getattr(hospedagem.quarto, "numero", "Desconhecido")
        tipo_quarto = getattr(hospedagem.quarto, "tipo", "Não informado")
        layout.addWidget(QLabel(f"Quarto: {numero_quarto} ({tipo_quarto})"))

        layout.addStretch()
