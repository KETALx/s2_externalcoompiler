from fileinput import filename

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QWindow

from ui import s2ec

class settingsGUI(QWidget):
    def __init__(self):
        super(settingsGUI,self).__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

class toolGUI(QMainWindow):

    def __init__(self):
        super(toolGUI,self).__init__()


    def OpenFileDialog(self):
        mapfilename = QFileDialog.getOpenFileName(self,
            "Open map file",
            "",
            "Source 2 map files (*.vmap);; All Files (*)",
        )
        map_file_path = mapfilename


    def OpenPathPreferences(self):
        pass


    def compileMap(self):
        print('compile')

def main():
    ui = s2ec.Ui_MainWindow()

    app = QApplication([])
    window = toolGUI()

    ui.setupUi(window)
    window.show()

    app.exec()


if __name__ == '__main__':
    main()