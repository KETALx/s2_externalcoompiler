import threading
from fileinput import filename
from os import cpu_count

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QWindow

from pyqt6_plugins.examplebuttonplugin import QtGui

from ui import s2ec

import os



class toolGUI(QMainWindow):

    def __init__(self):
        super(toolGUI,self).__init__()

        self.ui = s2ec.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.LoadVmap.clicked.connect(self.OpenMapFileDialog)
        self.ui.LoadVmap.setIcon(QIcon('icons/edit_in_place.png'))

        self.ui.buttonLoadCompilerPath.clicked.connect(self.GetResourceCompiler)
        self.ui.buttonLoadVpkOutputPath.clicked.connect(self.GetOutputDirectory)

        global map_file_path
        global vpk_output_folder
        global ResourceCompilerPath

        global MAX_CPU_THREADS
        MAX_CPU_THREADS = os.cpu_count()
        self.ui.cpu_threads_count.setValue(MAX_CPU_THREADS - 1)
        self.ui.cpu_threads_count.setMaximum(MAX_CPU_THREADS)
        self.ui.audio_threads_count.setValue(MAX_CPU_THREADS - 1)
        self.ui.audio_threads_count.setMaximum(MAX_CPU_THREADS)

    def GetOutputDirectory(self):
        vpk_output_folder = QFileDialog.getExistingDirectory(self, "Compiler")
        self.ui.VpkOutputText.setPlainText(vpk_output_folder)

    def GetResourceCompiler(self):
        ResourceCompilerPath = QFileDialog.getOpenFileName(self,
            "Open resource compiler",
            "",
            "Compiler executable (*.exe)",
        )[0]
        print(ResourceCompilerPath)
        self.ui.ResourceCompilerText.setPlainText(ResourceCompilerPath)

    def OpenMapFileDialog(self):
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