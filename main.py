from fileinput import filename

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QIcon


class toolGUI(QMainWindow):
    def __init__(self):
        super(toolGUI,self).__init__()
        uic.loadUi("ui/s2ec.ui",self)
        self.show()
        #self.setFixedSize(1000,800)
        self.setWindowIcon(QIcon("icons/run_map.png"))
        self.pushButtonCompile.clicked.connect(self.compileMap)
        self.actionLoad_map.triggered.connect(self.OpenFileDialog)

    def OpenFileDialog(self):
        mapfilename = QFileDialog.getOpenFileName(self,
            "Open map file",
            "",
            "Source 2 map files (*.vmap);; All Files (*)",
        )
        print(mapfilename)

    def compileMap(self):
        print('compile')

def main():
    app = QApplication([])
    window = toolGUI()

    app.exec()


if __name__ == '__main__':
    main()