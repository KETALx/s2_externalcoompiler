from fileinput import filename

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QWindow

from ui import s2ec


class toolGUI(QMainWindow):

    def __init__(self):
        super(toolGUI,self).__init__()

        self.ui = s2ec.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.LoadVmap.clicked.connect(self.OpenFileDialog)
        self.ui.LoadVmap.setIcon(QIcon('icons/edit_in_place.png'))


        global map_file_path


    def OpenFileDialog(self):
        mapfilename = QFileDialog.getOpenFileName(self,
            "Open map file",
            "",
            "Source 2 map files (*.vmap);; All Files (*)",
        )
        map_file_path = mapfilename[0]
        self.ui.TextMapFilename.setPlainText(map_file_path)
        print(map_file_path)


    def OpenPathPreferences(self):
        print("pref")


    def compileMap(self):
        print('compile')

def main():

    app = QApplication([])
    window = toolGUI()

    window.show()



    app.exec()


if __name__ == '__main__':
    main()