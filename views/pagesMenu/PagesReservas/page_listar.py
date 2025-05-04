from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QSpinBox,
    QLabel, QLineEdit, QScrollArea, QGroupBox
)
from PySide6.QtGui import QPalette
from PySide6.QtCore import Qt
import sys
# ====== CLASSE PRINCIPAL DA PÁGINA ABRIR HOSPEDAGEM ======
class Ui_page_abrir2(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout principal
        main_layout = QVBoxLayout(self)
        # SpinBox para quantidade de pessoas
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(1)
        self.spinbox.setValue(1)
        self.spinbox.valueChanged.connect(self.update_form)

        # Formulário para os acompanhantes
        self.form_group = QGroupBox("Acompanhantes")
        self.form_layout = QFormLayout()
        palette = self.form_group.palette()
        bg_color = palette.color(QPalette.Base)  # Cor de fundo das células
        print(bg_color.name())
        self.form_group.setLayout(self.form_layout)

        # Adiciona os widgets ao layout principal
        main_layout.addStretch()
        main_layout.addWidget(QLabel("Quantidade de pessoas:"))
        main_layout.addWidget(self.spinbox)
        main_layout.addWidget(self.form_group)
        main_layout.addStretch()

        # Armazena os campos dinâmicos
        self.acompanhantes = []

    def update_form(self, value):
        # Limpa os campos antigos
        for label, line_edit in self.acompanhantes:
            self.form_layout.removeWidget(label)
            self.form_layout.removeWidget(line_edit)
            label.deleteLater()
            line_edit.deleteLater()
        self.acompanhantes.clear()

        # Adiciona novos campos com base em value - 1
        for i in range(value - 1):
            label = QLabel(f"Acompanhante {i + 1}:")
            line_edit = QLineEdit()
            self.form_layout.addRow(label, line_edit)
            self.acompanhantes.append((label, line_edit))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
