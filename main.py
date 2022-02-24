import sys
from PyQt6.QtCore import Qt, QSize, QObject, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import(
	QGridLayout, QLabel, QPushButton, QPlainTextEdit, QWidget, QApplication, QMainWindow, QStatusBar, QFrame
)
from cutlet import Cutlet

katsu = Cutlet()

class Worker(QObject):
	finished = pyqtSignal()
	
	def conv_job(self):
		global conv_out
		conv_out = katsu.romaji(conv_in)
		self.finished.emit()

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		
		self.setWindowTitle("Romaji Converter")
		
		layout = QGridLayout()
		font = QFont()
		font.setPointSize(11)
		
		self.info_label = QLabel("Convert Japanese Character to Romaji")
		self.info_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		self.convert_button = QPushButton("Convert to Romaji")
		self.convert_button.setStatusTip("Click to start conversion")
		self.convert_button.clicked.connect(self.convert_run)
		self.in_label = QLabel("Input")
		self.in_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		self.out_label = QLabel("Output")
		self.out_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		self.in_text = QPlainTextEdit()
		self.in_text.setStatusTip("Type Your Text Here")
		self.in_text.setMinimumSize(QSize(380, 430))
		self.out_text = QPlainTextEdit()
		self.out_text.setStatusTip("Converted romaji goes here")
		self.out_text.setMinimumSize(QSize(380, 430))
		
		#Layout Setting
		layout.addWidget(self.info_label, 1, 0, 1, 2)
		layout.addWidget(self.convert_button, 2, 0, 1, 2)
		layout.addWidget(self.in_label, 3, 0, 1, 1)
		layout.addWidget(self.out_label, 3, 1, 1, 1)
		layout.addWidget(self.in_text, 4, 0, 1, 1)
		layout.addWidget(self.out_text, 4, 1, 1, 1)
		
		widget = QWidget()
		widget.setLayout(layout)
		widget.setFont(font)
		self.setCentralWidget(widget)
		
		self.statusbar = QStatusBar()
		self.setStatusBar(self.statusbar)
		self.statuslabel = QLabel()
		self.statuslabel.setText("Ready")
		self.statusbar.addPermanentWidget(self.statuslabel)
		
	def convert_run(self):
		global conv_in
		conv_in = self.in_text.toPlainText()
		self.thread = QThread()
		self.worker = Worker()
		self.worker.moveToThread(self.thread)
		self.thread.started.connect(self.worker.conv_job)
		self.worker.finished.connect(self.thread.quit)
		self.worker.finished.connect(self.worker.deleteLater)
		self.thread.finished.connect(self.thread.deleteLater)
		
		self.thread.start()
		
		self.convert_button.setEnabled(False)
		self.statuslabel.setText("Converting")
		self.thread.finished.connect(lambda: self.statuslabel.setText("Ready"))
		self.thread.finished.connect(lambda: self.out_text.setPlainText(conv_out))
		self.thread.finished.connect(lambda: self.convert_button.setEnabled(True))
		
if __name__ == '__main__' :
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
