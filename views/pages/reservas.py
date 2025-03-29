from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class PageReservas(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        label = QLabel("<H1>Reservas</H1>")
        layout.addWidget(label)
        
        # Adicione mais widgets conforme necessário
        self.setLayout(layout)