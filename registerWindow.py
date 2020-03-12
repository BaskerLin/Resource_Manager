# coding:utf-8
import PySide2.QtUiTools as QLoader
from PySide2 import QtWidgets,QtCore
import os
import time as t
import pymongo

import user as um
reload(um)

#链接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["userdb"]

#获取C:\Users\用户名的路径
path = os.getcwd()

#Ui文件路径
signUpWindow_ui = path + r"\Documents\houdini17.0\python\Resource_Manager\src\signUpWindow.ui"
signUpManagerWindow_ui = path + r"\Documents\houdini17.0\python\Resource_Manager\src\signUpManagerWindow.ui"

class registerWindow(QtWidgets.QWidget):
    """
    注册窗口类
    """
    def __init__(self):
        super(registerWindow, self).__init__()
        # 加载ui,并设置ui界面
        loader = QLoader.QUiLoader()
        self.ui = loader.load(signUpWindow_ui)
        self.ui.setParent(self)

        # 设置窗口名称
        self.setWindowTitle("注册")

        #管理员认证窗口
        self.signUoManagerWin = signUpManagerWindow()

        self.username = None
        self.password = None
        self.rePassword = None
        self.WM = False


        #获取控件
        self.let_username = self.ui.findChild(QtWidgets.QLineEdit, "let_username")
        self.let_password = self.ui.findChild(QtWidgets.QLineEdit, "let_password")
        self.let_rePassword = self.ui.findChild(QtWidgets.QLineEdit, "let_rePassword")

        self.rbtn_ordinaryUser = self.ui.findChild(QtWidgets.QRadioButton, "rbtn_ordinaryUser")
        self.rbtn_manager = self.ui.findChild(QtWidgets.QRadioButton, "rbtn_manager")

        self.btn_signUp = self.ui.findChild(QtWidgets.QPushButton, "btn_signUp")

        #设置默认值
        self.let_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.let_rePassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.rbtn_ordinaryUser.setChecked(True)

        #链接信号与槽函数
        self.btn_signUp.clicked.connect(lambda: self.signUp())
        self.rbtn_manager.toggled.connect(lambda :self.selectManager())

        self.signUoManagerWin.manager_signal.connect(lambda :self.setWM())

    def signUp(self):

        self.username = self.let_username.text()
        self.password = self.let_password.text()
        self.rePassword = self.let_rePassword.text()

        if not self.username:
            return 0
        if not self.password:
            return 0

        #判断该用户是否已存在
        collist = db.list_collection_names()
        if self.username in collist:
            print("The user already exists")
            return 0

        if not self.password == self.rePassword:
            print("The two passwords are inconsistent")
            return 0
        else:
            #self.user = um.user()
            #保存数据
            um.saveUsername(self.username, self.username)
            um.savePassword(self.username, self.password)

            time = t.strftime('%Y-%m-%d %H:%M:%S',t.localtime(t.time()))
            um.saveUserOperate(self.username,"register",time)

            if self.rbtn_manager.isChecked() and self.WM:
                um.saveUserJurisdiction(self.username, True, True, True, True)
                um.saveUserID(self.username, 1)
            elif self.rbtn_ordinaryUser.isChecked():
                um.saveUserJurisdiction(self.username, True, False, False, False)
                um.saveUserID(self.username, 2)
            self.close()

    def selectManager(self):

        self.signUoManagerWin.show()


    def setWM(self):
        self.WM = True
        print("WM = True")

class signUpManagerWindow(QtWidgets.QWidget):
    """
    注册管理员窗口
    """
    manager_signal = QtCore.Signal()
    def __init__(self):
        super(signUpManagerWindow, self).__init__()
        # 加载ui,并设置ui界面
        loader = QLoader.QUiLoader()
        self.ui = loader.load(signUpManagerWindow_ui)
        self.ui.setParent(self)

        # 设置窗口名称
        self.setWindowTitle("注册管理员")

        self.key = None

        #获取控件
        self.let_key = self.ui.findChild(QtWidgets.QLineEdit, "let_key")
        self.btn_cancel = self.ui.findChild(QtWidgets.QPushButton, "btn_cancel")
        self.btn_ok = self.ui.findChild(QtWidgets.QPushButton, "btn_ok")

        #链接信号与槽函数
        self.btn_cancel.clicked.connect(lambda :self.close())
        self.btn_ok.clicked.connect(lambda :self.ok())

    def ok(self):
        self.key = self.let_key.text()

        if self.key == "IDO":
            self.manager_signal.emit()
            self.close()

