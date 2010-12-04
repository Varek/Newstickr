#!/usr/bin/env python

import sys
import time
from PyQt4 import QtGui, QtCore

class Config:
	SampleText = '<a href="http://www.twitter.com/">Twitter!</a> +++ Laufschrift Newsticker +++ Lorem ipsum Newstickerum +++ tick tick tack +++ fooooooo +++ Erdbeben +++ Dinosaurier +++ Taliban +++ Katastrophe +++ '
	speed = 0.1

class UpdateThread(QtCore.QThread):
	def __init__(self, label):
		QtCore.QThread.__init__(self, label)
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
		self.emit(QtCore.SIGNAL('textRotated(QString)'), \
				'<qt>' + self.text + '</qt>')

	def finish(self):
		self.isRunning = False


class NewstickrWindow(QtGui.QWidget):
	def __init__(self, width, height, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
		self.setGeometry(0, height-30, width, 30)
		self.setWindowTitle('Newstickr')
		self.label = QtGui.QLabel(self)
		self.label.setGeometry(0, 0, 350, 20)
		self.updateThread = UpdateThread(self.label)
		QtCore.QObject.connect(self.updateThread, QtCore.SIGNAL('textRotated(QString)'), self, QtCore.SLOT('setText(QString)'))
		self.updateThread.start()
	
	def mousePressEvent(self, event):
		print "clicked!"
		self.close()

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

app = QtGui.QApplication(sys.argv)

desktop = app.desktop()
newstickr = NewstickrWindow(desktop.width(), desktop.height())
newstickr.show()

sys.exit(app.exec_())

