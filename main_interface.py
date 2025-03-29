from PySide6 import QtWidgets
from views.MainWindow import Ui_MainWindow as ui  

class MyApp(QtWidgets.QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyApp()
    window.show()
    app.exec_()