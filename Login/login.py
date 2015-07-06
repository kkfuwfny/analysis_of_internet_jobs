#coding:utf-8
from PyQt4 import QtGui,QtCore
#setEchoMode
class login(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.textName = QtGui.QLineEdit(self)
        self.textPass = QtGui.QLineEdit(self)
	self.textPass.setEchoMode(QtGui.QLineEdit.Password)        
	self.buttonLogin = QtGui.QPushButton(u'登录', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
	self.setWindowTitle(u"管理员登录")        
	layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if (self.textName.text() == 'admin' and
            self.textPass.text() == 'lv'):
            self.accept() #关键
        else:
            QtGui.QMessageBox.warning(self, u'错误', u'帐号或密码错误')
