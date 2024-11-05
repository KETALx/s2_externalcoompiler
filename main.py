import threading
from fileinput import filename
from os import cpu_count
from subprocess import check_output

from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QWindow

from ui import s2ec

import os
import json
import subprocess


class toolGUI(QMainWindow):

    def __init__(self):
        super(toolGUI,self).__init__()



        self.ui = s2ec.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.LoadVmap.clicked.connect(self.OpenMapFileDialog)
        self.ui.LoadVmap.setIcon(QIcon('icons/edit_in_place.png'))

        self.ui.buttonLoadCompilerPath.clicked.connect(self.GetResourceCompiler)
        self.ui.buttonLoadVpkOutputPath.clicked.connect(self.GetOutputDirectory)

        self.ui.pushButtonCompile.clicked.connect(self.CompileMap)

        self.ui.comboLightRes.currentTextChanged.connect(self.ChangeLightRes)

        self.map_file_path = None
        self.vpk_output_folder = None
        self.resource_compiler_path = "D:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\game\\bin\\win64\\resourcecompiler.exe"

        self.flags_world_buildworld = True
        self.flags_world_entsonly = False
        self.flags_world_presettlephys = False



        self.MAX_CPU_THREADS = os.cpu_count()
        self.ui.cpu_threads_count.setValue(self.MAX_CPU_THREADS - 1)
        self.ui.cpu_threads_count.setMaximum(self.MAX_CPU_THREADS)
        self.ui.audio_threads_count.setValue(self.MAX_CPU_THREADS - 1)
        self.ui.audio_threads_count.setMaximum(self.MAX_CPU_THREADS)






    def GetOutputDirectory(self):
        self.vpk_output_folder = QFileDialog.getExistingDirectory(self, "Compiler")
        self.ui.VpkOutputText.setPlainText(self.vpk_output_folder)


    def GetResourceCompiler(self):
        self.resource_compiler_path = QFileDialog.getOpenFileName(self,
            "Open resource compiler",
            "",
            "Compiler executable (*.exe)",
        )[0]

        if self.resource_compiler_path != "":
            print("FOUND")
            self.ui.ResourceCompilerText.setPlainText(self.resource_compiler_path)



    def OpenMapFileDialog(self):
        self.map_file_path = QFileDialog.getOpenFileName(self,
            "Open map file",
            "",
            "Source 2 map files (*.vmap);; All Files (*)",
        )[0]
        self.ui.TextMapFilename.setPlainText(self.map_file_path)

    def ChangeLightRes(self):
        print(self.ui.comboLightRes.currentText())


    def CompileMap(self):

        if self.resource_compiler_path is None or not str(self.resource_compiler_path).endswith("resourcecompiler.exe"):
            self.ShowErrorMessage("compiler not found, configure in path settings")
            return

        if self.vpk_output_folder is None:
            print("TEST")
            self.ShowErrorMessage("Output folder not found")
            return

        if self.ui.bBuildWorld.isChecked():
            Buildworld = "-fshallow", "-maxtextureres", "256", "-quiet", "-unbufferedio", "-noassert", "-world", "-retail",  "-breakpad",  "-nop4"
            strBuildWorld = ', '.join(Buildworld)
        else:
            strBuildWorld = ''

        print(strBuildWorld)

        self.process = QProcess(self)
        self.process.start(self.resource_compiler_path, ["-i",self.map_file_path,
        "-outroot", self.vpk_output_folder,
        "-html",
        "-threads", str(self.ui.cpu_threads_count.value()),
        strBuildWorld,
        ])
        print(self.process.arguments())
        self.process.finished.connect(self.clog)


    def clog(self):
        self.log = self.process.readAllStandardOutput()
        self.stdout = bytes(self.log).decode("utf8")
        print(self.process.arguments())
        self.ui.textCompileOutput.append(self.stdout)

    def ShowErrorMessage(self, error = ""):
        cMessageBox = QMessageBox()
        cMessageBox.setWindowTitle("Error")
        cMessageBox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        cMessageBox.setText(error)
        cMessageBox.exec()






def main():

    app = QApplication([])
    window = toolGUI()


    window.show()
    app.exec()

if __name__ == '__main__':
    main()
