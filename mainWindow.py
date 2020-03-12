# coding:utf-8
import PySide2.QtUiTools as QLoader
from PySide2 import QtWidgets,QtGui,QtCore
import os,json
import time



#获取C:\Users\用户名的路径
path = os.getcwd()

#获取资源文件路径
file_path = path + r"\Documents\houdini17.0\python\Resource_Manager\src"

#加载ui
manager_ui = file_path + r"\MainWindow.ui"




