#!/usr/bin/env python

import os
import sys
import time
from PyQt4 import QtGui, QtCore



class Config:
	SampleText = '<a href="http://www.twitter.com/">Twitter!</a> +++ Laufschrift Newsticker +++ Lorem ipsum Newstickerum +++ tick tick tack +++ fooooooo +++ Erdbeben +++ Dinosaurier +++ Taliban +++ Katastrophe +++ '
	speed = 0.1
	accel = 20
	iconName = 'newstickr.xpm'
	numTagLines = 3
	tagLines = ['', '', '']
	vspace = 30
	width = 800
	updateInterval = 10
	browser = 'chromium-browser'



class NTSettingsDialog(QtGui.QDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		self.setWindowTitle('Settings')
		self.setModal(True)
		self.textEdits = []
		for i in range(len(Config.tagLines)):
			self.initTagLine(i)
		acceptButton = QtGui.QPushButton(self)
		cancelButton = QtGui.QPushButton(self)
		acceptButton.setGeometry(0, Config.numTagLines * Config.vspace, 100, 30)	
		cancelButton.setGeometry(110, Config.numTagLines * Config.vspace, 100, 30)	
		acceptButton.setText('OK')
		cancelButton.setText('Cancel')
		self.connect(cancelButton, QtCore.SIGNAL('clicked()'), lambda: self.close())
		self.connect(acceptButton, QtCore.SIGNAL('clicked()'), lambda: self.accept())

	def initTagLine(self, anInteger):
		
		label = QtGui.QLabel(self)
		label.setText('Tag line ' + str(anInteger+1))
		label.setGeometry(0, Config.vspace * anInteger, 70, Config.vspace)
		edit = QtGui.QTextEdit(self)
		edit.setGeometry(100, Config.vspace * anInteger, 200, Config.vspace)
		edit.setText(Config.tagLines[anInteger])
		self.textEdits.append(edit)

	def accept(self):
		for line in Config.tagLines:
			line = ''
		i = 0
		for edit in self.textEdits:
			Config.tagLines[i] = edit.toPlainText()
			i += 1
		self.close()
		

		

class TrayIcon(QtGui.QSystemTrayIcon):
	def __init__(self, icon, parent=None):
		QtGui.QSystemTrayIcon.__init__(self, icon, parent)
		menu = QtGui.QMenu(parent)
		confDialogAction = menu.addAction("Settings")
		exitAction = menu.addAction("Exit")
		self.setContextMenu(menu)
		self.connect(exitAction, QtCore.SIGNAL('triggered()'), lambda: parent.close())
		self.connect(confDialogAction, QtCore.SIGNAL('triggered()'), lambda: self.showSettingsDialog())

	def showSettingsDialog(self):
		dialog = NTSettingsDialog()
		dialog.show()
		dialog.exec_()




class DataSourceThread(QtCore.QThread):
	def __init__(self, messageWidget):
		QtCore.QThread.__init__(self)
		self.messageWidget = messageWidget
		self.isRunning = True

	def run(self):
		while self.isRunning:
			time.sleep(Config.updateInterval)
			print "updating ..."

	def finish(self):
		self.isRunning = False

	


class UpdateThread(QtCore.QThread):
	def __init__(self, label):
		QtCore.QThread.__init__(self, label)
		self.label = label
		self.text = Config.SampleText
		self.isRunning = True
		self.isRotating = True

	def run(self):
		while self.isRunning:
			time.sleep(Config.speed)
			if self.isRotating:
				self.rotate()

	def rotate(self):
		self.emit(QtCore.SIGNAL('rotated()'))

	def finish(self):
		self.isRunning = False
	
	@QtCore.pyqtSignature('setRotating(bool)')
	def setRotating(self, aBoolean):
		self.isRotating = aBoolean




class NewsLabel(QtGui.QLabel):
	def __init__(self, parent=None):
		QtGui.QLabel.__init__(self, parent)
		self.url = ''
	
	def mousePressEvent(self, event):
		os.system(Config.browser + ' ' + self.url)




class NewsTickrMessage(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.newsLabels = []
		self.sizeInPixels = 0

	def addNews(self, text, url):
		label = NewsLabel(self)
		htmlText = '<qt>'
		if url != '':
			htmlText += '<a href="' + url + '">'
		htmlText += text
		if url != '':
			htmlText += '</a>'
		htmlText += '</qt>'
		label.setText(htmlText)
		label.url = url
		self.newsLabels.append(label)
	
	def clearNews(self):
		for item in self.newsLabels:
			item.hide()
			item.destroy()

	def buildLabel(self):
		self.sizeInPixels = 0
		for label in self.newsLabels:
			label.setGeometry(self.sizeInPixels, 0, len(label.text())*3, label.height())
			self.sizeInPixels += label.width() + 30
		return self.sizeInPixels 
	



class NewstickrWindow(QtGui.QWidget):
	def __init__(self, width, height, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
		self.setGeometry(0, height-30, width, 30)
		self.setWindowTitle('Newstickr')
		self.newsLabels = []
		self.ticks = 0
		self.message = NewsTickrMessage(self)
		self.updateThread = UpdateThread(self.message)
		QtCore.QObject.connect(self.updateThread, QtCore.SIGNAL('rotated()'), self, QtCore.SLOT('update()'))
		QtCore.QObject.connect(self, QtCore.SIGNAL('rotating(bool)'), self.updateThread, QtCore.SLOT('setRotating(bool)'))
		self.updateThread.start()
		self.dataSourceThread = DataSourceThread(self)
		self.dataSourceThread.start()
	
	#def mousePressEvent(self, event):
	#	print "clicked!"

	def resizeEvent(self, event):
		geo = self.geometry()
		self.message.setGeometry(0, 0, geo.width(), geo.height())

	@QtCore.pyqtSignature('setText(QString)')
	def setText(self, aString):
		self.label.setText(aString)

	def closeEvent(self, event):
		self.updateThread.finish()
		self.dataSourceThread.finish()
		time.sleep(0.2)
		event.accept()

	def enterEvent(self, event):
		self.emit(QtCore.SIGNAL('rotating(bool)'), False)

	def leaveEvent(self, event):
		self.emit(QtCore.SIGNAL('rotating(bool)'), True)

	def addNews(self, text, url):
		self.message.addNews(text, url)

	def clearNews(self):
		self.message = NewsTickrMessage()

	def buildLabel(self):
		self.labelSize = self.message.buildLabel()

	@QtCore.pyqtSignature('update()')
	def update(self):
		self.message.show()
		self.ticks += 1
		newX = Config.width - self.ticks * Config.accel
		self.message.setGeometry(newX, 0, self.message.width(), self.message.height())
		if newX < -self.labelSize:
			self.ticks = 0
			
			




app = QtGui.QApplication(sys.argv)

desktop = app.desktop()
Config.width = desktop.width()

newstickr = NewstickrWindow(desktop.width(), desktop.height())

newstickr.addNews('Google', 'http://www.google.com')
newstickr.addNews('Twitter', 'http://www.twitter.com')
newstickr.addNews('Veeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeryyyyyyyyyyyyy loooooooooooooooooooooooooooooooonnnnnnnnnnnnnngggggggggggggggggggggggg tteeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxtttttttttttttttttt', 'http://www.twitter.com')
newstickr.addNews('Twitter', 'http://www.twitter.com')
newstickr.buildLabel()
newstickr.show()

trayIcon = TrayIcon(QtGui.QIcon(Config.iconName), newstickr)
trayIcon.show()

sys.exit(app.exec_())

