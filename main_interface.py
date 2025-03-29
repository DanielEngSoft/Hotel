from PySide6 import QtWidgets
from views.MainWindow import Ui_MainWindow as ui  

class MyApp(QtWidgets.QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # # Adicione aqui o código para interagir com os elementos da interface
        # # Conectando botões do menu lateral às páginas
        # self.btn_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_home))
        # self.btn_cadastro.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_cadastro))
        # self.btn_contatos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_contatos))
        # self.btn_sobre.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_sobre))

        # # Define a página inicial
        # self.stackedWidget.setCurrentWidget(self.page_home)
        
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyApp()
    window.show()
    app.exec_()