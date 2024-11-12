import threading
from fileinput import filename
from os import cpu_count
from subprocess import check_output

from PyQt6.QtCore import QProcess, QTimer
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QWindow
from pyqt6_plugins.examplebutton import QtWidgets

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

        self.ui.buttonLoadCompilerPath.setToolTip("Game folder path, ex: C:\SteamLibrary\steamapps\common\Counter-Strike Global Offensive")
        self.ui.buttonLoadCompilerPath.clicked.connect(self.GetResourceCompiler)
        self.ui.buttonLoadVpkOutputPath.clicked.connect(self.GetOutputDirectory)

        self.ui.pushButtonCompile.clicked.connect(self.CompileMap)
        self.ui.pushButtonCancelCompile.clicked.connect(self.CancelCompile)

        self.ui.comboLightRes.currentTextChanged.connect(self.ChangeLightRes)

        self.map_file_path = None
        self.vpk_output_folder = None
        self.resource_compiler_path = None
        self.addonsfolder = ""

        self.flags_world_buildworld = True
        self.flags_world_entsonly = False
        self.flags_world_presettlephys = False



        self.MAX_CPU_THREADS = os.cpu_count()
        self.ui.cpu_threads_count.setValue(self.MAX_CPU_THREADS - 1)
        self.ui.cpu_threads_count.setMaximum(self.MAX_CPU_THREADS)
        self.ui.audio_threads_count.setValue(self.MAX_CPU_THREADS - 1)
        self.ui.audio_threads_count.setMaximum(self.MAX_CPU_THREADS)

        self.process = QProcess()




    def GetOutputDirectory(self):
        self.vpk_output_folder = QFileDialog.getExistingDirectory(self, "Compiler")
        self.ui.VpkOutputText.setPlainText(self.vpk_output_folder)


    def GetResourceCompiler(self):
        self.resource_compiler_path = QFileDialog.getExistingDirectory(self,
            "Game folder path"
        )

        if self.resource_compiler_path != "":
            print(self.resource_compiler_path)
            self.addonsfolder = self.resource_compiler_path
            self.resource_compiler_path += "/game/bin/win64/resourcecompiler.exe"
            self.ui.ResourceCompilerText.setPlainText(self.resource_compiler_path)



    def OpenMapFileDialog(self):
        self.map_file_path = QFileDialog.getOpenFileName(self,
            "Open map file",
            self.addonsfolder,
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

        self.ui.pushButtonCompile.setEnabled(False)
        

        if self.ui.bBuildWorld.isChecked():
            Buildworld = "-fshallow", "-maxtextureres", "256", "-quiet", "-unbufferedio", "-noassert", "-world", "-retail",  "-breakpad",  "-nop4"
            strBuildWorld = ', '.join(Buildworld)
        else:
            strBuildWorld = ''

        if self.ui.bEntsOnly.isChecked():
            EntsOnly = "-fshallow", "-maxtextureres", "256", "-quiet", "-unbufferedio", "-noassert", "-world", "-retail",  "-breakpad",  "-nop4"
            strEntsOnly = ', '.join(EntsOnly)
        else:
            strEntsOnly = ''

        print(strBuildWorld)

        self.process = QProcess(self)
        self.process.start(self.resource_compiler_path, ["-i",self.map_file_path,
        "-outroot", self.vpk_output_folder,
        "-html",
        "-threads", str(self.ui.cpu_threads_count.value()),
        strBuildWorld, strEntsOnly
        ])
        print(self.process.arguments())
        self.process.readyReadStandardOutput.connect(self.clog)
        self.process.finished.connect(self.elog)


    def elog(self):
        print("Finished compile")
        self.ui.pushButtonCompile.setEnabled(True)
        

    def clog(self):
        self.log = self.process.readAllStandardOutput()
        self.stdout = bytes(self.log).decode("utf8")
        self.ui.textCompileOutput.append(self.stdout)

    def CancelCompile(self):
        if self.process.processId() > 0:
            print("terminated")
            self.process.kill()
            self.ui.textCompileOutput.append("Compile canceled")
            


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
