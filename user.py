# coding:utf-8
import pymongo

#创建数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
# dblist = client.list_database_names()
# if "userdb" not in dblist:
#     db = client["userdb"]
db = client["userdb"]


class user():
    """
    用户类
    """
    def __init__(self):

        #定义用户信息、权限等初始值
        self.userID = 1    #1为管理员，2为用户
        self.jurRead = True
        self.jurAlter = False
        self.jurUpload = False
        self.jurDownload = False
        self.username = "123"
        self.password = "123456"

#保存密码
def savePassword(username, password):
    col = db[username]
    dict = {"password": password}
    col.insert_one(dict)

    #保存身份
def saveUserID(username, userID):
    col = db[username]
    dict = {"userID": userID}
    col.insert_one(dict)

    #保存用户名
def saveUsername(username, newName):
    #创建集合
    col = db[username]
    dict = {"username": newName}
    x= col.insert_one(dict)

#保存权限
def saveUserJurisdiction(username, jurRead, jurAlter, jurUpload, jurDownload):
    col = db[username]
    dict = {"jurRead": jurRead, "jurAlter":jurAlter, "jurUpload":jurUpload, "jurDownload":jurDownload}
    col.insert_one(dict)

#保存操作记录
def saveUserOperate(username, operate, time):
    col = db[username]
    dict = {"operate": operate, "time":time}
    col.insert_one(dict)

#修改用户名
def changeUsername(username, newname):
    col = db[username]
    oldnameD = {"username":username}
    newnameD = { "$set": { "username": newname } }
    x = col.update_many(oldnameD,newnameD)
    print(x)
    print("**********")
    mycol = db[username]
    for x in mycol.find():
        print(x)
    print("**********")

def changePassword(username):
    pass

def changeID(username):
    pass

#修改权限
def changeJurisdiction(username):
    pass
