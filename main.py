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
        self.resource_compiler_path = None


        self.MAX_CPU_THREADS = os.cpu_count()
        self.ui.cpu_threads_count.setValue(self.MAX_CPU_THREADS - 1)
        self.ui.cpu_threads_count.setMaximum(self.MAX_CPU_THREADS)
        self.ui.audio_threads_count.setValue(self.MAX_CPU_THREADS - 1)
        self.ui.audio_threads_count.setMaximum(self.MAX_CPU_THREADS)

        self.UserSettings = {}
        self.LoadFromJson()
        if self.UserSettings["CompilerPath"] is not None:
            self.ui.ResourceCompilerText.setPlainText(self.UserSettings["CompilerPath"])




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
            self.ui.ResourceCompilerText.setPlainText(self.resource_compiler_path)
            self.WriteJson(comp_path=self.resource_compiler_path)


    def OpenMapFileDialog(self):
        self.map_file_path = QFileDialog.getOpenFileName(self,
            "Open map file",
            "",
            "Source 2 map files (*.vmap);; All Files (*)",
        )[0]
        self.ui.TextMapFilename.setPlainText(self.map_file_path)

    def ChangeLightRes(self):
        print(self.ui.comboLightRes.currentText())
        #self.WriteJson(lightres=self.ui.comboLightRes.currentText())

    def CompileMap(self):
        compile_params = ''
        #compile_params += f'"{self.UserSettings["CompilerPath"]}"'
        #compile_params = ' -threads 7 -fshallow -maxtextureres 256 -quiet -html -unbufferedio -i "d:/steamlibrary/steamapps/common/counter-strike global offensive/content/csgo_addons/sfmtest/maps/sfmtest.vmap"  -noassert  -world -nosettle -nolightmaps -retail  -breakpad  -nop4 -outroot "C:\\\\Users\\\\kirill\\\\AppData\\\\Local\\\\Temp\\\\valve\\\\hammermapbuild\\\\game"'
        print(self.UserSettings["CompilerPath"])

        self.process = QProcess(self)
        self.process.start(self.UserSettings["CompilerPath"], ["-i", "d:/steamlibrary/steamapps/common/counter-strike global offensive/content/csgo_addons/sfmtest/maps/sfmtest.vmap"])
        self.process.waitForFinished()
        self.log = self.process.readAllStandardOutput()
        self.stdout = bytes(self.log).decode("utf8")
        print(self.process.arguments())
        self.ui.textCompileOutput.append(self.stdout)



    def WriteJson(self,comp_path = "", lightres=2048):
        self.UserSettings = {
            "CompilerPath" : comp_path,
            "LightRes" : lightres
        }

        with open("user_settings.json", "w") as self.outfile:
            json.dump(self.UserSettings, self.outfile, ensure_ascii=False,indent=4)

    def LoadFromJson(self):

        with open('user_settings.json', 'r') as file:
            data = json.load(file)

        self.UserSettings = data


def main():

    app = QApplication([])
    window = toolGUI()

    window.show()
    app.exec()

if __name__ == '__main__':
    main()
