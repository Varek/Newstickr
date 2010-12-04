#!/usr/bin/env python

import sys
import time
from threading import Thread
from PyQt4 import QtGui, QtCore

class Config:
	SampleText = 'Laufschrift Newsticker +++ Lorem ipsum Newstickerum +++ tick tick tack +++ fooooooo +++ Erdbeben +++ Dinosaurier +++ Taliban +++ Katastrophe +++ '
	speed = 0.1

class UpdateThread(Thread):
	def __init__(self, label):
		Thread.__init__(self)
		self.label = label
		self.text = Config.SampleText
		self.isRunning = True

	def run(self):
		while self.isRunning:
			time.sleep(Config.speed)
			self.rotate()

	def rotate(self):
		if len(self.text) > 0:
			self.text = self.text[1:] + self.text[0]
				
		self.label.setText(self.text)

	def finish(self):
		self.isRunning = False

class NewstickrWindow(QtGui.QLabel):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setGeometry(0, 0, 400, 30)
		self.setWindowTitle('Newstickr')
		self.label = QtGui.QLabel(self)
		self.label.setGeometry(0, 0, 350, 20)
		self.updateThread = UpdateThread(self.label)
		self.updateThread.start()
	
	def mousePressEvent(self, event):
		print "clicked!"

	def resizeEvent(self, event):
		geo = self.geometry()
		self.label.setGeometry(0, 0, geo.width(), geo.height())

	def closeEvent(self, event):
		self.updateThread.finish()
		event.accept()

app = QtGui.QApplication(sys.argv)

newstickr = NewstickrWindow()
newstickr.show()

sys.exit(app.exec_())

