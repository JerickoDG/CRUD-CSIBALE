from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu
import sys, bcrypt, main
from backend import *
from resources.loginUI import Ui_LoginWindow
from PyQt5.QtGui import *

dbInstance = DatabaseConnection()
dbInstance.setCursor()


class LoginWindow(SingletonClass, QWidget, Ui_LoginWindow):
	def __init__(self):
		super(LoginWindow, self).__init__()
		create_table(dbCon=dbInstance)
		self.setupUi(self)


		# Connects to the login function using the submit button
		self.submitBtn.clicked.connect(self.loginAutheticate)
		
		# Connects to login function when at password and username line and presses Enter/return
		self.username.returnPressed.connect(self.loginAutheticate)
		self.password.returnPressed.connect(self.loginAutheticate)
		
		# Closes the login window when the x button is clicked
		self.closeBtn.clicked.connect(self.closeLogin)

		# Drag the Login Window
		self.dragPos = QtCore.QPoint()

		self.loginStatus = False
		
		icon = QtGui.QIcon('./view.png')
		self.showPassAction = QtWidgets.QAction(icon, 'Show password', self)
		self.password.addAction(
            self.showPassAction, QtWidgets.QLineEdit.TrailingPosition)
		showPassButton = self.password.findChild(QtWidgets.QAbstractButton)
		showPassButton.pressed.connect(lambda: self.showPassword(True))
		showPassButton.released.connect(lambda: self.showPassword(False))
		
		
	def showPassword(self, show):
		self.password.setEchoMode(
        QtWidgets.QLineEdit.Normal if show else QtWidgets.QLineEdit.Password)


	# Method that Opens the main window of the application while closing the login window
	def openMainWindow(self):
		self.tomain = main.MainWindow()
		self.tomain.show()
		self.tomain.raise_()
		self.hide()

	# Method for Login Authentication
	def loginAutheticate(self):

		username = self.username.text()
		password = self.password.text()

		# Determines if there are blank lines
		if len(username)==0 or len(password)==0:
			self.loginMsg.setText("Please fill in all required fields.")

		else:
			
			# Getting the value of password from database
			# cur.execute("SELECT password FROM LOGIN_INFO")
			passresult, = returnOldPassword(dbCon=dbInstance)

			# Getting the value of username from database
			# cur.execute("SELECT username FROM LOGIN_INFO")
			userresult, = returnOldUsername(dbCon=dbInstance)
			
			# Decoding the password and matching them
			# inputBytes = password.encode('utf-8')
			# passwordMatching = bcrypt.checkpw(inputBytes, passresult)

			passwordMatching = passwordDecodeMatch(password=password, result=passresult)

			# Successful login when both password and username matches otherwise invalid
			if passwordMatching == True and userresult == username:
				self.loginStatus = True
				# print("Successfully logged in.")
				self.loginMsg.setText("")
				self.openMainWindow() # proceeds to the main window
			else:
				self.loginMsg.setText("Invalid username or password.")

				# resets input fields
				self.password.setText("") 
				self.username.setText("")
		
		# conn.close()
	
	# Method to be able to drag the Login Window
	def mousePressEvent(self, event):
		self.dragPos = event.globalPos()
		
	def mouseMoveEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton:
			self.move(self.pos() + event.globalPos() - self.dragPos)
			self.dragPos = event.globalPos()
			event.accept() 
	
	def closeLogin(self):
		# QApplication.instance().quit
		dbInstance.closeConnection()
		self.close()
	
		

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = LoginWindow()
	ui.show()

	sys.exit(app.exec_())# -*- coding: utf-8 -*-
