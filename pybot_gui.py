# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Pybot_GUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import design

class ExampleApp(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.actionSelect_Client.triggered.connect(self.select_client_btn)

    def select_client_btn(self):
        print("hello world")


def main():
    app = QtGui.QApplication([1])
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
