# coding:utf-8
import PySide2.QtUiTools as QLoader
from PySide2 import QtWidgets
import os
import pymongo
import time as t

import mainWindow

import user as um
reload(um)

import registerWindow
reload(registerWindow)
import managerWindow
reload(managerWindow)

#链接数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["userdb"]

#获取C:\Users\用户名的路径
path = os.getcwd()

#Ui文件路径
loginWindow_ui = path + r"\Documents\houdini17.0\python\Resource_Manager\src\loginWindow.ui"

class loginWindow(QtWidgets.QWidget):
    """
    登录窗口类
    """
    def __init__(self):
        super(loginWindow, self).__init__()
        # 加载ui,并设置ui界面
        loader = QLoader.QUiLoader()
        self.ui = loader.load(loginWindow_ui)
        self.ui.setParent(self)

        # 设置窗口名称
        self.setWindowTitle("登录")

        self.username = None
        self.password = None

        #获取UI控件
        self.btn_register = self.ui.findChild(QtWidgets.QPushButton, "btn_register")
        self.btn_login = self.ui.findChild(QtWidgets.QPushButton, "btn_login")
        self.let_userName = self.ui.findChild(QtWidgets.QLineEdit, "let_userName")
        self.let_password = self.ui.findChild(QtWidgets.QLineEdit, "let_password")

        self.let_password.setEchoMode(QtWidgets.QLineEdit.Password)

        #链接信号与槽
        self.btn_register.clicked.connect(lambda: self.register())
        self.btn_login.clicked.connect(lambda: self.login())

    def login(self):

        self.username = self.let_userName.text()
        self.password = self.let_password.text()

        print("**********")
        mycol = db[self.username]
        for x in mycol.find():
            print(x)
        print("**********")
        # x = mycol.delete_many({})
        # print(x.deleted_count)
        # w = mycol.drop()
        # if w:
        #     print("delete successfully")
        # else:
        #     print("delete failed")

        if not self.username:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText(u'请输入用户名！')
            msgBox.exec_()
            return 0
        if not self.password:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText(u'请输入密码！')
            msgBox.exec_()
            return 0


        collist = db.list_collection_names()
        if self.username in collist:  # 判断该用户是否存在
            colUser = db[self.username]

            #从数据库提取密码
            for x in colUser.find({},{"password":1}):
                if "password" in x:
                    password = x["password"]
            if not password:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText(u'错误！找不到密码！')
                msgBox.exec_()
                return 0

            #判断密码是否正确
            if self.password == password:

                msgBox = QtWidgets.QMessageBox()
                msgBox.setText(u'登陆成功！')
                msgBox.exec_()

                managerWin = managerWindow.managerWindow(self.username)
                managerWin.show()

                #录入登陆时间
                time = t.strftime('%Y-%m-%d %H:%M:%S', t.localtime(t.time()))
                um.saveUserOperate(self.username, "login", time)


            else:
                #print("Password is wrong")
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText(u'密码错误！')
                msgBox.exec_()
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText(u'用户不存在！')
            msgBox.exec_()



    def register(self):

        self.registerWin = registerWindow.registerWindow()
        self.registerWin.show()


