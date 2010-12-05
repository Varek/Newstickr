from PyQt4 import Qt, QtCore, QtGui
from Config import Config
from TwitterSearch import CombinedSearch
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
			self.emit(QtCore.SIGNAL('clearNews()'))
			tLines = []
			for line in Config.tagLines:
				if line != '':
					tLines.append(line)
			combinedSearch = CombinedSearch(tLines)
	
			try:
				combinedSearch.search()
				for field in combinedSearch.combinedSearchResults:
					self.emit(QtCore.SIGNAL('addNews(QString, QString)'), field.text, field.GetStatusUrl())
				self.emit(QtCore.SIGNAL('buildLabel()'))
			except (Exception, Error):
				pass
			time.sleep(Config.updateInterval)
			

	def finish(self):
		self.isRunning = False
