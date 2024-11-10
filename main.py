from PyQt5 import QtCore, QtGui, QtWidgets
from lib.reassemblyWord import img2word, correction, genReading

class Ui_VOCA(object):
    def setupUi(self, VOCA):
        VOCA.setObjectName("VOCA")
        VOCA.resize(390, 779)
        VOCA.setAutoFillBackground(False)
        self.verticalLayoutWidget = QtWidgets.QWidget(VOCA)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 371, 761))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.btn_fun_FileLoad)
        self.verticalLayout.addWidget(self.pushButton)
        self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 367, 728))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 371, 731))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableView = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.tableView)
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget_2)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(VOCA)
        QtCore.QMetaObject.connectSlotsByName(VOCA)
        
    def btn_fun_FileLoad(self):
        fname=QtWidgets.QFileDialog.getOpenFileName(self.verticalLayoutWidget,'','','JPEG(*.jpeg),JPG(*.jpg)')

        if fname:
            self.tableView.setRowCount(1)
            self.tableView.setColumnCount(1)
            self.tableView.setItem(0, 0, QtWidgets.QTableWidgetItem("Reading your note..."))
            self.tableView.repaint()
            
            voca = correction(img2word(fname[0]), True)
            
            self.tableView.setRowCount(len(voca))
            self.tableView.setColumnCount(3)
            for i, w in enumerate(voca):
                ss = ''
                for ex in w['ex']:
                    ss += ex + "\n"
                
                self.tableView.setItem(i, 0, QtWidgets.QTableWidgetItem(w['word']))
                self.tableView.setItem(i, 1, QtWidgets.QTableWidgetItem(w['mean']))
                self.tableView.setItem(i, 2, QtWidgets.QTableWidgetItem(ss))
                self.tableView.repaint()
            
            reading = genReading(voca, self.textBrowser, log=True)
            
            
            

    def retranslateUi(self, VOCA):
        _translate = QtCore.QCoreApplication.translate
        VOCA.setWindowTitle(_translate("VOCA", "VOCA"))
        self.pushButton.setText(_translate("VOCA", "Read note"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_VOCA()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
