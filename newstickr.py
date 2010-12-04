#!/usr/bin/env python

import sys
import time
from PyQt4 import QtGui, QtCore

class Config:
	SampleText = '<a href="http://www.twitter.com/">Twitter!</a> +++ Laufschrift Newsticker +++ Lorem ipsum Newstickerum +++ tick tick tack +++ fooooooo +++ Erdbeben +++ Dinosaurier +++ Taliban +++ Katastrophe +++ '
	speed = 0.1
	iconName = 'newstickr.xpm'
	numTagLines = 3
	tagLines = ['', '', '']
	vspace = 30

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




class NewstickrWindow(QtGui.QWidget):
	def __init__(self, width, height, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
		self.setGeometry(0, height-30, width, 30)
		self.setWindowTitle('Newstickr')
		self.label = QtGui.QLabel(self)
		self.updateThread = UpdateThread(self.label)
		QtCore.QObject.connect(self.updateThread, QtCore.SIGNAL('rotated()'), self, QtCore.SLOT('update()'))
		QtCore.QObject.connect(self, QtCore.SIGNAL('rotating(bool)'), self.updateThread, QtCore.SLOT('setRotating(bool)'))
		self.newsLabels = []
		self.updateThread.start()
	
	#def mousePressEvent(self, event):
	#	print "clicked!"

	def resizeEvent(self, event):
		geo = self.geometry()
		self.label.setGeometry(0, 0, geo.width(), geo.height())

	@QtCore.pyqtSignature('setText(QString)')
	def setText(self, aString):
		self.label.setText(aString)

	def closeEvent(self, event):
		self.updateThread.finish()
		time.sleep(0.2)
		event.accept()

	def enterEvent(self, event):
		self.emit(QtCore.SIGNAL('rotating(bool)'), False)

	def leaveEvent(self, event):
		self.emit(QtCore.SIGNAL('rotating(bool)'), True)

	def clearNews(self):
		for item in self.newsLabels:
			item.hide()
			item.destroy()

	def addNews(self, text, url):
		label = QtGui.QLabel(self)
		htmlText = '<qt>'
		if url != '':
			htmlText += '<a href="' + url + '">'
		htmlText += text
		if url != '':
			htmlText += '</a>'
		htmlText += '</qt>'
		label.setText(htmlText)
		self.update()

	@QtCore.pyqtSignature('update()')
	def update(self):
		print 'update'
			




app = QtGui.QApplication(sys.argv)

desktop = app.desktop()

newstickr = NewstickrWindow(desktop.width(), desktop.height())
newstickr.show()
trayIcon = TrayIcon(QtGui.QIcon(Config.iconName), newstickr)
trayIcon.show()

sys.exit(app.exec_())

