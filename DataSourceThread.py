from PyQt4 import Qt, QtCore, QtGui
from Config import Config
import time

class DataSourceThread(QtCore.QThread):
	def __init__(self, messageWindow):
		QtCore.QThread.__init__(self)
		self.messageWindow = messageWindow
		self.isRunning = True
		QtCore.QObject.connect(self, QtCore.SIGNAL('clearNews()'), self.messageWindow, QtCore.SLOT('clearNews()'))
		QtCore.QObject.connect(self, QtCore.SIGNAL('addNews(QString, QString)'), self.messageWindow, QtCore.SLOT('addNews(QString, QString)'))
		QtCore.QObject.connect(self, QtCore.SIGNAL('buildLabel()'), self.messageWindow, QtCore.SLOT('buildLabel()'))
		

	def run(self):
		while self.isRunning:
			print "updating"
			self.emit(QtCore.SIGNAL('clearNews()'))
			self.emit(QtCore.SIGNAL('addNews(QString, QString)'), 'Google', 'http://www.google.com')
			self.emit(QtCore.SIGNAL('addNews(QString, QString)'), 'Twitter', 'http://www.twitter.com')
			self.emit(QtCore.SIGNAL('addNews(QString, QString)'), 'Veeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeryyyyyyyyyyyyy loooooooooooooooooooooooooooooooonnnnnnnnnnnnnngggggggggggggggggggggggg tteeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeexxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxtttttttttttttttttt', 'http://www.twitter.com')
			self.emit(QtCore.SIGNAL('buildLabel()'))
			time.sleep(Config.updateInterval)
			

	def finish(self):
		self.isRunning = False
