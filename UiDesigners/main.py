from PySide6 import QtWidgets
from MainWindow import Ui_MainWindow  # Substitua "arquivo" pelo nome do seu arquivo

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyApp()
    window.show()
    app.exec_()