# coding:utf-8
import PySide2.QtUiTools as QLoader
from PySide2 import QtWidgets
import os
import pymongo
import time as t

import user

#链接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["userdb"]

#获取C:\Users\用户名的路径
path = os.getcwd()

#Ui文件路径
managerWindow_ui = path + r"\Documents\houdini17.0\python\Resource_Manager\src\managerWindow.ui"

class managerWindow(QtWidgets.QWidget):
    def __init__(self,username):
        super(managerWindow, self).__init__()
        # 加载ui,并设置ui界面
        loader = QLoader.QUiLoader()
        self.ui = loader.load(managerWindow_ui)
        self.ui.setParent(self)

        # 设置窗口名称
        self.setWindowTitle("管理员界面")

        self.username = username
        self.newName = None

        # 获取UI控件
        self.btn_changuUsername = self.ui.findChild(QtWidgets.QPushButton, "btn_changuUsername")
        self.btn_changeID = self.ui.findChild(QtWidgets.QPushButton, "btn_changeID")
        self.btn_changeJurisdiction = self.ui.findChild(QtWidgets.QPushButton, "btn_changeJurisdiction")
        self.let_username = self.ui.findChild(QtWidgets.QLineEdit, "let_username")

        #设置控件默认值
        #self.let_username.setReadOnly(True)
        self.let_username.setText(self.username)

        #链接信号与槽
        self.btn_changuUsername.clicked.connect(lambda: self.changeUsername())
        self.btn_changeID.clicked.connect(lambda : self.changeID())
        self.btn_changeJurisdiction.clicked.connect(lambda : self.changeJurisdiction())

    def changeUsername(self):
        self.newName = self.let_username.text()
        if self.newName :
            user.changeUsername(self.username, self.newName)






    def changeID(self):
        pass

    def changeJurisdiction(self):
        pass