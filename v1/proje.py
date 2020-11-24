# Imports for PyQt5 Lib and Functions to be used
# -*- coding: utf-8 -*-
import sys
import os,io
import logging
import json, requests
from pytodb2 import define_error
from cevapVer import Chat
from datetime import datetime
from PyQt5.QtSql import QSqlDatabase
from sqlDialog import SqlKonusmaModeli
from cevapVer import pairs, reflections
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt,QModelIndex, QDir, QFile, QUrl, Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor,QIcon,QBrush,QGuiApplication, QFont, QTextCursor, QIcon
from PyQt5.QtWidgets import QWidget,QApplication, QTextEdit, QPushButton, QLabel, QDesktopWidget, QMainWindow, QAbstractItemView


logging.basicConfig(filename="chat.log", level=logging.DEBUG)
logger = logging.getLogger("logger")

def veritabaniBaglan():
    veritabani = QSqlDatabase.database()
    if not veritabani.isValid():
        veritabani = QSqlDatabase.addDatabase("QSQLITE")
        if not veritabani.isValid():
            logger.error("Veritabanı Eklenemedi !")

    yaz_dir = QDir()
    if not yaz_dir.mkpath("."):
        logger.error("Yazılabilir dizin oluşturulamadı !")

    # Erişilebilir bir veritabanı dosyası oluşturulmuştur.
    dosyaAdi = "{}/chat-database.sqlite3".format(yaz_dir.absolutePath())

    # Veritabanı mevcut değilse open() fonksiyonu SQLite'ı oluşturacaktır.
    veritabani.setDatabaseName(dosyaAdi)
    if not veritabani.open():
        logger.error("Veritabanı Açılamadı")
        QFile.remove(dosyaAdi)


#region interfaceCodes

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 754)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 750))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 600))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setMinimumSize(QtCore.QSize(300, 500))
        self.treeView.setMaximumSize(QtCore.QSize(350, 16777215))
        self.treeView.setStyleSheet("QTreeView {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: 1px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"    border-radius: 8px 8px 8px 8px;\n"
"    padding: 10px;\n"
"    outline: 0px;\n"
"    font:   rgb(255, 255, 255);\n"
"    font:  16pt \"MS Shell Dlg 2\";\n"
"}\n"
"\n"
"QTreeView::item {\n"
"         border-radius: 10px 10px 10px 10px;       \n"
"         border: 3px solid  rgb(0, 170, 255);                \n"
"         height: 50px;                            \n"
"         padding-left: 20px;                      \n"
"         margin:10px;       \n"
"          /*#B3E5FC;#b9e6fb;   */\n"
"         background-color:  #b9e6fb;\n"
"         color: rgb(0, 170, 255);      \n"
"    }\n"
"\n"
"QTreeView::item::hover {\n"
"       background-color:  rgb(255, 255, 255);\n"
"}\n"
"\n"
"QTreeView::branch:has-siblings:!adjoins-item {\n"
"    border-image: url(:/icon/images/vline.png) 0;\n" 
"}\n"
"\n"
"QTreeView::branch:has-siblings:adjoins-item {\n"
"    border-image: url(:/icon/images/branch-more.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:!has-children:!has-siblings:adjoins-item {\n"
"    border-image: url(:/icon/images/branch-end.png) 0;\n"
"}\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed,\n"
"QTreeView::branch:closed:has-children:has-siblings {\n"
"        border-image: none;\n"
"        image: url(:/icon/images/branch-closed.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings,\n"
"QTreeView::branch:open:has-children:has-siblings  {\n"
"        border-image: none;\n"
"        image: url(:/icon/images/branch-open.png);\n"
"}\n"
"\n"
"QTreeView::item:!has-children{\n"
"\n"
"      border-radius: 0px 0px 0px 0px;\n"
"      border:3px solid  #e7a61a;  \n"
"      height: 50px;\n"
"      padding-left: 20px;                      \n"
"      margin:10px;                      \n"
"      background-color: #e7a61a;        \n"
"      color: rgb(255, 255, 255);\n"
"\n"
"}\n"
"QTreeView::item:!has-children::hover {\n"
"      border-radius: 0px 0px 0px 0px;\n"
"      border: 3px solid #e7a61a;\n"
"      height: 50px;                        \n"
"      padding-left: 20px;                      \n"
"      margin:10px;                      \n"
"      background-color:  rgb(255, 255, 255); \n"
"      color: #e7a61a;\n"
"}\n"
"\n"
"\n"
"")
        self.treeView.setItemsExpandable(True)
        self.treeView.setObjectName("treeView")
        self.horizontalLayout.addWidget(self.treeView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit_kodBlogu = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_kodBlogu.setMinimumSize(QtCore.QSize(500, 100))
        self.textEdit_kodBlogu.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textEdit_kodBlogu.setStyleSheet("border: 1px solid;\n"
"font: 16pt \"MS Shell Dlg 2\";\n"
"border-radius: 8px 8px 8px 8px;\n"
"background-color: palette(base);\n"
"color: rgb(102, 102, 102);\n"
"border-color: rgb(255, 255, 255);")
        self.textEdit_kodBlogu.setLineWidth(1)
        self.textEdit_kodBlogu.setObjectName("textEdit_kodBlogu")
        self.verticalLayout.addWidget(self.textEdit_kodBlogu)
        self.textEdit_console = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_console.setMinimumSize(QtCore.QSize(500, 0))
        self.textEdit_console.setMaximumSize(QtCore.QSize(16777215, 200))
        self.textEdit_console.setStyleSheet("border: 1px solid;\n"
"font: 16pt \"MS Shell Dlg 2\";\n"
"border-radius: 8px 8px 8px 8px;\n"
"background-color: palette(base);\n"
"color: rgb(170, 0, 127);\n"
"border-color: rgb(255, 255, 255);")
        self.textEdit_console.setObjectName("textEdit_console")
        self.verticalLayout.addWidget(self.textEdit_console)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.frame_sagMenuParent = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_sagMenuParent.sizePolicy().hasHeightForWidth())
        self.frame_sagMenuParent.setSizePolicy(sizePolicy)
        self.frame_sagMenuParent.setMinimumSize(QtCore.QSize(325, 0))
        self.frame_sagMenuParent.setMaximumSize(QtCore.QSize(325, 16777215))
        self.frame_sagMenuParent.setStyleSheet("background-color: #cad7e0;\n"
                                               "    border-radius: 8px 8px 8px 8px;")

        self.frame_sagMenuParent.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_sagMenuParent.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sagMenuParent.setObjectName("frame_sagMenuParent")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_sagMenuParent)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_sagMenu = QtWidgets.QVBoxLayout()
        self.verticalLayout_sagMenu.setObjectName("verticalLayout_sagMenu")
        self.frame_sagMenu2 = QtWidgets.QFrame(self.frame_sagMenuParent)
        self.frame_sagMenu2.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_sagMenu2.setStyleSheet("background-color: #008efe;")
        self.frame_sagMenu2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_sagMenu2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sagMenu2.setObjectName("frame_sagMenu2")
        self.label_robot = QtWidgets.QLabel(self.frame_sagMenu2)
        self.label_robot.setGeometry(QtCore.QRect(20, 0, 91, 71))
        self.label_robot.setStyleSheet("image: url(:/icon/images/robot.png);\n"
                                          "background-color: transparent;")
        self.label_robot.setText("")
        self.label_robot.setObjectName("label_robot")

        self.verticalLayout_sagMenu.addWidget(self.frame_sagMenu2)

        self.textEdit_message = QtWidgets.QTextEdit(self.frame_sagMenuParent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_message.sizePolicy().hasHeightForWidth())
        self.textEdit_message.setSizePolicy(sizePolicy)
        self.textEdit_message.setMinimumSize(QtCore.QSize(300, 200))
        self.textEdit_message.setStyleSheet("font-family: \"Verdana\"; \n"
                                            "    font-size: 10pt; \n"
                                            "    font-weight: 475;\n"
                                            "    text-align: right;   \n"
                                            "    background-color: #cad7e0;\n"  
                                            "    border:0;  /* kenarlık olmasın */\n"
                                            "")
        self.textEdit_message.setObjectName("textEdit_message")
        self.verticalLayout_sagMenu.addWidget(self.textEdit_message)
        self.frame_sagMenu3 = QtWidgets.QFrame(self.frame_sagMenuParent)
        self.frame_sagMenu3.setMinimumSize(QtCore.QSize(0, 75))
        self.frame_sagMenu3.setStyleSheet("    background-color: #cad7e0 ;\n")
        self.frame_sagMenu3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_sagMenu3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sagMenu3.setObjectName("frame_sagMenu3")
        self.lineEdit_sendMessage = QtWidgets.QLineEdit(self.frame_sagMenu3)
        self.lineEdit_sendMessage.setGeometry(QtCore.QRect(0, 20, 307, 55))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_sendMessage.sizePolicy().hasHeightForWidth())
        self.lineEdit_sendMessage.setSizePolicy(sizePolicy)
        self.lineEdit_sendMessage.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEdit_sendMessage.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lineEdit_sendMessage.setStyleSheet("    font-family: \"Verdana\";\n"
                                                "    font-size: 10pt;\n"
                                                "    font-weight: 475; \n"
                                                "    text-align: left;\n"
                                                "    background-color: #ffffff;\n"
                                                "    border:0;  /* kenarlık olmasın */\n"
                                                "    height: 33px; /* metin kutusunun yüksekliği yazı boyutundan daha fazla olsun */\n"
                                                "    border-radius: 25px 25px 25px 25px;\n"
                                                "padding-left:70px;")
        self.lineEdit_sendMessage.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_sendMessage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.lineEdit_sendMessage.setObjectName("lineEdit_sendMessage")
        self.pushButton_smile = QtWidgets.QPushButton(self.frame_sagMenu3)
        self.pushButton_smile.setGeometry(QtCore.QRect(0, 18, 60, 60))
        self.pushButton_smile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_smile.setStyleSheet("background-color: transparent;")
        self.pushButton_smile.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/images/happy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_smile.setIcon(icon)
        self.pushButton_smile.setIconSize(QtCore.QSize(45, 45))
        self.pushButton_smile.setObjectName("pushButton_smile")
        self.verticalLayout_sagMenu.addWidget(self.frame_sagMenu3)
        self.gridLayout_2.addLayout(self.verticalLayout_sagMenu, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_sagMenuParent, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame_sagMenuParent)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(0, 70))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.textEdit_searchEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit_searchEdit.setGeometry(QtCore.QRect(0, 10, 250, 45))
        self.textEdit_searchEdit.setStyleSheet("border: 1px solid;\n"
"font: 16pt \"MS Shell Dlg 2\";\n"
"border-color: rgb(156, 156, 156);\n"
"border-radius: 8px 8px 8px 8px;\n"
"background-color: palette(base);\n"
"color: rgb(102, 102, 102)")
        self.textEdit_searchEdit.setObjectName("textEdit_searchEdit")
        self.pushButton_searchEdit = QtWidgets.QPushButton(self.frame)
        self.pushButton_searchEdit.setGeometry(QtCore.QRect(250, 10, 50, 45))
        self.pushButton_searchEdit.setStyleSheet("background-image:url(:/icon/search.png);\n"
"background-repeat: no-repeat;\n")
        self.pushButton_searchEdit.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/images/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_searchEdit.setIcon(icon)
        self.pushButton_searchEdit.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_searchEdit.setObjectName("pushButton_searchEdit")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(360, -11, 261, 91))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_add = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_add.setStyleSheet("QPushButton {\n"
"    background-color: transparent;\n"
"    background-repeat: no-repeat;\n"
" }")
        self.pushButton_add.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/images/add_dark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_add.setIcon(icon1)
        self.pushButton_add.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_add.setCheckable(True)
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout_2.addWidget(self.pushButton_add)
        self.pushButton_document = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_document.setStyleSheet("background-image: url(:/icon/images/document.png);\n"
"background-color: transparent;\n"
"background-repeat: no-repeat;")
        self.pushButton_document.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/images/document_dark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_document.setIcon(icon2)
        self.pushButton_document.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_document.setCheckable(True)
        self.pushButton_document.setObjectName("pushButton_document")
        self.horizontalLayout_2.addWidget(self.pushButton_document)
        self.pushButton_play = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_play.setStyleSheet("background-color: transparent;\n"
"background-repeat: no-repeat;\n"
"background-image: url(:/icon/images/play.png);")
        self.pushButton_play.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/images/play_dark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_play.setIcon(icon3)
        self.pushButton_play.setIconSize(QtCore.QSize(64, 64))
        self.pushButton_play.setCheckable(True)
        self.pushButton_play.setObjectName("pushButton_play")
        self.horizontalLayout_2.addWidget(self.pushButton_play)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)
        self.frame_header = QtWidgets.QFrame(self.centralwidget)
        self.frame_header.setMinimumSize(QtCore.QSize(0, 125))
        self.frame_header.setStyleSheet("background-color:  #b9e6fb;")
        self.frame_header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_header.setObjectName("frame_header")
        self.label_baslik = QtWidgets.QLabel(self.frame_header)
        self.label_baslik.setGeometry(QtCore.QRect(-649, 30, 1721, 111))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_baslik.sizePolicy().hasHeightForWidth())
        self.label_baslik.setSizePolicy(sizePolicy)
        self.label_baslik.setMaximumSize(QtCore.QSize(16777215, 111))
        self.label_baslik.setStyleSheet("\n"
"image: url(:/icon/images/logoyazi.png);\n")
        self.label_baslik.setText("")
        self.label_baslik.setObjectName("label_baslik")
        self.label_logo = QtWidgets.QLabel(self.frame_header)
        self.label_logo.setGeometry(QtCore.QRect(6, 0, 140, 131))
        self.label_logo.setStyleSheet("image: url(:/icon/images/logo.png);")
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")
        self.gridLayout.addWidget(self.frame_header, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.treeView.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:48pt; font-weight:600;\">asasas</span></p></body></html>"))
        self.textEdit_kodBlogu.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textEdit_console.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&gt;&gt;&gt;</p></body></html>"))



ballon="""
<table border="0" cellpadding="0" cellspacing="0">
      <tr>
         <td><img src=":/icon/images/sol_ust_beyaz.gif"></td>
         <td bgcolor="#ffffff"></td>
         <td><img src=":/icon/images/sag_ust_beyaz.gif"></td>
		 <td width="40"><img src=":/icon/images/transparent.gif"></td>
      </tr>
      <tr>
         <td background=":/icon/images/sol_orta_beyaz.gif">&nbsp;</td>
         <td bgcolor="#ffffff" style="">{}<div align="right" style="font-size: 9px;color: #1BA44C;">{}</div></td>
         <td bgcolor="#ffffff">&nbsp;</td>
		 <td width="40"><img src=":/icon/images/transparent.gif"></td>
      </tr>
      <tr>
         <td><img src=":/icon/images/sol_alt_beyaz.gif"></td>
         <td bgcolor="#ffffff"><img src=":/icon/images/transparent.gif"></td>
         <td><img src=":/icon/images/sag_alt_beyaz.gif"></td>
		 <td width="40"><img src=":/icon/images/transparent.gif"></td>
      </tr>
</table>
"""

ballon_Kullanici="""
<table border="0" cellpadding="0" cellspacing="0" align="right">
      <tr>
         <td width="40"><img src=":/icon/images/transparent.gif"></td>
		 <td><img src=":/icon/images/sol_ust_yesil.gif"></td>
         <td bgcolor="#e9fedd"><img src=":/icon/images/transparent.gif"></td>
         <td><img src=":/icon/images/sag_ust_yesil.gif"></td>
      </tr>
      <tr >
		 <td width="40"><img src=":/icon/images/transparent.gif"></td>
         <td bgcolor="#e9fedd">&nbsp;</td>
         <td bgcolor="#e9fedd" style="">{}<div align="right" style="font-size: 9px;color: #1BA44C;">{}</div></td>
         </td>
         <td background=":/icon/images/sag_orta_yesil.gif">&nbsp;</td>
      </tr>
      <tr>
		 <td width="40"><img src=":/icon/images/transparent.gif"></td>
         <td><img src=":/icon/images/sol_alt_yesil.gif"></td>
         <td bgcolor="#e9fedd"><img src=":/icon/images/transparent.gif"></td>
         <td><img src=":/icon/images/sag_alt_yesil.gif"></td>
      </tr>
</table>
"""



import icons_rc

#endregion


class SecondWindow(QtWidgets.QDialog):
    def __init__(self):
        super(SecondWindow, self).__init__()
        self.setUI()

    def setUI(self):
        centerPoint = QDesktopWidget().availableGeometry().center()
        self.setGeometry(centerPoint.x() - 180, centerPoint.y() + 96, 270, 157)
        self.setMinimumSize(QSize(270, 157))
        self.setMaximumSize(QSize(270, 157))
        self.setWindowTitle("Emojiler")
        self.setWindowIcon(QIcon(':/icon/images/smile.png'))

        """
            Emojiye tıklanıldığında fonksiyon, emojinin karşılığını password adında görünmeyen bir label'a yazıyor. Dialog bittiğinde ise
            label'daki yazı userinput'a gönderiliyor. Farklı yollar denedik. Direkt olarak butona tıklandığında ana pencere sınıfına ulaşıp orada
            setText yapmayı denedik ama userinput değiştiği halde ekrana yazdırmıyordu. Userinputun değiştiğini ise konsola yazdırarak kontrol etmiştik.
            Signal kullanmayı da denedik. Emojiye tıklanıldığında direkt kapanmasından dolayı QDialog kullanmaya karar verdik.
        """

        self.password = QtWidgets.QLineEdit(self)
        self.password.setGeometry(200, 300, 50, 30)

        self.gulucuk = QPushButton(self)
        self.gulucuk.setStyleSheet(
            "background-image: url(:/icon/images/smile.png);background-repeat: no-repeat;border: none;outline: none;")
        self.gulucuk.setGeometry(5, 5, 70, 60)
        self.gulucuk.clicked.connect(self.gulucukKoy)

        self.uzgun = QPushButton(self)
        self.uzgun.setStyleSheet(
            "background-image: url(:/icon/images/uzgun.png);background-repeat: no-repeat;border: none;outline: none;")
        self.uzgun.setGeometry(95, 5, 70, 60)
        self.uzgun.clicked.connect(self.uzgunSuratKoy)

        self.gulme = QPushButton(self)
        self.gulme.setStyleSheet(
            "background-image: url(:/icon/images/gulme.png);background-repeat: no-repeat;border: none;outline: none;")
        self.gulme.setGeometry(185, 5, 70, 60)
        self.gulme.clicked.connect(self.gul)

        self.gozKirpma = QPushButton(self)
        self.gozKirpma.setStyleSheet(
            "background-image: url(:/icon/images/kırp.png);background-repeat: no-repeat;border: none;outline: none;")
        self.gozKirpma.setGeometry(5, 80, 70, 60)
        self.gozKirpma.clicked.connect(self.gozKirp)

        self.duzSurat = QPushButton(self)
        self.duzSurat.setStyleSheet(
            "background-image: url(:/icon/images/duz.png);background-repeat: no-repeat;border: none;outline: none;")
        self.duzSurat.setGeometry(95, 80, 70, 60)
        self.duzSurat.clicked.connect(self.duzSuratKoy)

        self.sasirma = QPushButton(self)
        self.sasirma.setStyleSheet(
            "background-image: url(:/icon/images/sasirma.png);background-repeat: no-repeat;border: none;outline: none;")
        self.sasirma.setGeometry(185, 80, 70, 60)
        self.sasirma.clicked.connect(self.sasirmaKoy)

    def gulucukKoy(self):
        self.password.setText(":) ")
        self.accept()

    def gul(self):
        self.password.setText(":D ")
        self.accept()

    def uzgunSuratKoy(self):
        self.password.setText(":( ")
        self.accept()

    def sasirmaKoy(self):
        self.password.setText(":O ")
        self.accept()

    def duzSuratKoy(self):
        self.password.setText(":| ")
        self.accept()

    def gozKirp(self):
        self.password.setText(";) ")
        self.accept()


class proje(QMainWindow):
    childNodes = []
    roots = []
    colors = ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0', '#f0027f', '#bf5b17', '#666666']
    words = ["abs", "print", "while", "max", "for"]

    acikNodes =[]
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.ReadFromJsonApi()
        self.ReadFromFile()
        self.show()
        self.ui.treeView.setDragDropMode(QAbstractItemView.DragOnly)
        self.ui.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.treeView.clicked.connect(self.expanded)
        self.ui.treeView.doubleClicked.connect(self.collapsed)
        self.ui.pushButton_play.pressed.connect(self.PlayButtonPressed)
        self.ui.pushButton_play.released.connect(self.PlayButtonReleased)
        self.ui.pushButton_add.pressed.connect(self.AddButtonPressed)
        self.ui.pushButton_add.released.connect(self.AddButtonReleased)
        self.ui.pushButton_smile.clicked.connect(self.emojiPage)
        self.ui.pushButton_document.pressed.connect(self.DocumentButtonPressed)
        self.ui.pushButton_document.released.connect(self.DocumentButtonReleased)
        self.ui.pushButton_play.clicked.connect(self.PlayButtonClick)
        self.ui.pushButton_add.clicked.connect(self.AddButtonClick)
        self.ui.pushButton_document.clicked.connect(self.DocumentButtonClick)
        self.ui.pushButton_searchEdit.clicked.connect(self.SearchButtonClick)
        self.setAcceptDrops(True)

        now = datetime.now()
        zaman = now.strftime("%H:%M")
        karsilama_metni = "Nasıl yardımcı olabilirim?"
        karsilama = ballon.format(karsilama_metni, zaman)
        self.ui.textEdit_message.append(karsilama)
        self.ui.textEdit_message.append("\n")

        self.ui.textEdit_message.setReadOnly(True)
        self.setWindowTitle("Python Kod Editörü")
        self.setWindowIcon(QIcon(':/icon/images/logo.png'))
        self.ui.lineEdit_sendMessage.returnPressed.connect(self.AddToChatLogUser)
        self.ui.lineEdit_sendMessage.setEnabled(True)
        self.ui.lineEdit_sendMessage.setFocus()
    # butona tıklandığında hem ikinici ekranı göstersin hem de tıklanılan emojiyi lineEdit_sendMessage yazsın
    def emojiPage(self):
        self.SW = SecondWindow()
        if self.SW.exec_():
            self.ui.lineEdit_sendMessage.setText(self.ui.lineEdit_sendMessage.text() + " " + self.SW.password.text())
        self.ui.lineEdit_sendMessage.setFocus()

    def UpdateCycle(self):
        '''
        Retrieves a new bot message and appends to the chat log.
        '''
        bmsg = self.v.getBotMessage()
        self.chatlog.setAlignment(Qt.AlignRight)
        [self.chatlog.append(m) for m in bmsg]
        self.userinput.setFocus()

    def ReplaceToEmoji(self, mesaj):
        yeniMesaj = mesaj
        if (":)" in mesaj):
            yeniMesaj = yeniMesaj.replace(':)', ' &#128522; ')
        if (":(" in mesaj):
            yeniMesaj = yeniMesaj.replace(':(', ' &#128542; ')
        if (":D" in mesaj):
            yeniMesaj = yeniMesaj.replace(':D', ' &#128516; ')
        if (":O" in mesaj):
            yeniMesaj = yeniMesaj.replace(':O', ' &#128558; ')
        if (";)" in mesaj):
            yeniMesaj = yeniMesaj.replace(';)', ' &#128521; ')
        if (":|" in mesaj):
            yeniMesaj = yeniMesaj.replace(':|', ' &#128528; ')
        return yeniMesaj

    def AddToChatLogUser(self):
        '''
        Takes guest's entry and appends to the chatlog
        '''
        mesaj = self.ui.lineEdit_sendMessage.text()
        if mesaj is not '':
            umsg = Chat(mesaj, pairs, reflections)
            umsg.converse(mesaj, quit='tamam')
            sql_konusma_modeli.mesaj_ekle(mesaj, umsg.__repr__())
            self.ui.textEdit_message.setAlignment(Qt.AlignLeft)
            now = datetime.now()
            zaman = now.strftime("%H:%M")
            ballonmesaj = ballon.format(umsg.__repr__(), zaman)
            splitting = self.ReplaceToEmoji(
                mesaj)  # Mesajın içerisinde emojisi simgesi bulunup bulunmadığını kontrol et.
            ballonKullanici = ballon_Kullanici.format(splitting, zaman)
            self.ui.textEdit_message.append(ballonKullanici)
            self.ui.textEdit_message.append("\n")
            self.ui.textEdit_message.setAlignment(Qt.AlignRight)
            self.ui.textEdit_message.append(ballonmesaj)
            self.ui.textEdit_message.append("\n")
            self.ui.textEdit_message.moveCursor(QtGui.QTextCursor.End)
            self.ui.lineEdit_sendMessage.setText("")

    # region TreeviewOperations
    def expanded(self, index):
         if not self.ui.treeView.isExpanded(index):
             if self.roots.__contains__(index.data()):
                 if len(self.acikNodes) > 0:
                     for item in self.acikNodes:
                         if item.data != index.data:
                             self.ui.treeView.collapse(item)
                             if self.acikNodes.__contains__(item.data()):
                                self.acikNodes.remove(item)
                 self.ui.treeView.expand(index)
                 self.acikNodes.append(index)
             else:
                 self.ui.treeView.expand(index)
                 self.acikNodes.append(index)
         else:
            self.ui.treeView.collapse(index)
            if self.acikNodes.__contains__(index):
                self.acikNodes.remove(index)


    def collapsed(self, item):
        i=1
        #self.ui.treeView.collapse(item)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        for ix in self.ui.treeView.selectedIndexes():
            text = ix.data(Qt.DisplayRole)
        if text in self.childNodes:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for ix in self.ui.treeView.selectedIndexes():
            text = ix.data(Qt.DisplayRole)  # or ix.data()
            self.colorTheText(text)

    def colorTheText(self, text):
        data = text.replace('<', "&lt;")
        data = data.replace("(", "<span style=\"color:#0000ff;\">(</span>")
        data = data.replace(")", "<span style=\" color:#0000ff;\">)</span>")
        data = data.replace("\n", "<br/>")

        for word in self.words:
            data = data.replace(word, "<span style=\" color:#aa007f;\">" + word + "</span>")

        data = data.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        self.ui.textEdit_kodBlogu.append(data)

    def ReadFromFile(self):
        with open(os.path.abspath('solmenu.json'), encoding='utf-8') as f:
            data = json.load(f)
        model = QStandardItemModel(0, 1, self.ui.treeView)
        model.setHeaderData(0, Qt.Horizontal, None)
        self.ui.treeView.setModel(model)
        self.TreeViewFill(model, data)

    def ReadFromJsonApi(self):
        payload = [{"__class__": "ServerRequest", "requestData": [], "requestClass": "TradeService",
                    "requestMethod": "getTradeOffers", "requestId": 83}]
        res = requests.request(method='GET', url='https://api.mocki.io/v1/ce5f60e2').text
        data = json.loads(res)
        model = QStandardItemModel(0, 1, self.ui.treeView)
        model.setHeaderData(0, Qt.Horizontal, None)
        self.ui.treeView.setModel(model)
        self.TreeViewFill(model, data)

    def TreeViewFill(self, model, data):
        i = 0
        for root, children in data.items():
            parent = QStandardItem(root)

            self.AddChild(children, parent)
            model.setItem(i, 0, parent)
            self.ui.treeView.setFirstColumnSpanned(i, self.ui.treeView.rootIndex(), True)

            self.roots.append(root)
            i += 1

    def AddChild(self, children, parent):
        if isinstance(children, dict):
            for item, items in children.items():
                child = QStandardItem(item)
                parent.appendRow(child)
                self.AddChild(items, child)
        elif children is not None:  # if there is one node
            node = QStandardItem(children)
            self.childNodes.append(children)
            parent.appendRow(node)





    # endregion

    #Region EXPERIMENTAL
    
    def addtochat(self, msg):
        now = datetime.now()
        zaman = now.strftime("%H:%M")
        ballonmesaj = ballon.format(msg, zaman) 
        self.ui.textEdit_message.setAlignment(Qt.AlignRight)
        self.ui.textEdit_message.append(ballonmesaj)
        self.ui.textEdit_message.append("\n")
        self.ui.textEdit_message.moveCursor(QtGui.QTextCursor.End)

    # region ButtonClick
    def PlayButtonClick(self):
        code = self.ui.textEdit_kodBlogu.toPlainText()
        
        if code:
            f = open("temp.txt", "w")
            f.write(code)
            f.close()
            hata_listesi = define_error("temp.txt")
            os.remove("temp.txt")
            if(len(hata_listesi) == 0):
                old_stdout = sys.stdout
                new_stdout = io.StringIO()
                sys.stdout = new_stdout
                exec(code)
                result = sys.stdout.getvalue().strip()
                sys.stdout = old_stdout
                self.ui.textEdit_console.setText(str(result))
            else:
                self.addtochat(str(hata_listesi))
        else:
            self.ui.textEdit_console.setText(">>> ")

    def AddButtonClick(self):
        b = 1


    def DocumentButtonClick(self):
        b=1


    def SearchButtonClick(self):
        # aranan = self.ui.textEdit_searchEdit.toPlainText()


        a = self.ui.treeView.keyboardSearch('a')

        #obj_type = type('Döngüler')
        #idx = self.sourceModel().index(sourceRow, 0, sourceParent)
        #a = self.ui.treeView.findChildren(str, 'a')
        print(str(a))


    # endregion

    # region PressedReleasedCodes

    def AddButtonPressed(self):
        self.ui.addButton.setIcon(QIcon(":/icon/images/add_light.png"))
    def AddButtonReleased(self):
        self.ui.addButton.setIcon(QIcon(":/icon/images/add_dark.png"))
    def PlayButtonPressed(self):
        if self.ui.textEdit_kodBlogu.toPlainText():
            self.ui.pushButton_play.setIcon(QIcon(":/icon/images/play_light.png"))
    def PlayButtonReleased(self):
        self.ui.pushButton_play.setIcon(QIcon(":/icon/images/play_dark.png"))
    def DocumentButtonPressed(self):
        self.ui.pushButton_document.setIcon(QIcon(":/icon/images/document_light.png"))
    def DocumentButtonReleased(self):
        self.ui.pushButton_document.setIcon(QIcon(":/icon/images/document_dark.png"))
    #endregion




if __name__ == "__main__":
    uygulama = QApplication([])
    veritabaniBaglan()
    sql_konusma_modeli = SqlKonusmaModeli()
    pencere = proje()
    pencere.show()
    uygulama.exec_()
