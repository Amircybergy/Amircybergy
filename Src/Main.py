import sys
import openpyxl
#import minimalmodbus
import time
from PyQt5.QtWidgets import QLabel,QLineEdit, QApplication,QPushButton, QWidget,QFileDialog, QComboBox, QMainWindow, QStyle, QListWidget, QSlider, QTextEdit
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5 import QtGui
import sqlite3
import time
import datetime


# Window coordinates and dimensions
X = 300
Y = 100
WIDTH = 880
HEIGHT = 580

class FirstWindow(QWidget):
	switch_to_second = pyqtSignal()

	def __init__(self):
		super().__init__()
		self.createUI()

	# Called when exit button is clicked
	def on_exit_click(self):
		self.close()

	# Called when sign in is clicked
	def on_sign_in_click(self):
		user_id = self.user_id_entry.text()
		password = self.password_entry.text()

		if user_id and password:

			# Create a database or connect to one that exists
			conn = sqlite3.connect('database.db')

			# Create a cursor instance
			cursor = conn.cursor()

			sql = ("SELECT userid,password FROM users WHERE userid = ? AND password = ?")
			values = (user_id, password)

			cursor.execute(sql, values)

			records = cursor.fetchall()

			if len(records) > 0:
				controller.current_user = user_id

				self.switch_to_second.emit()
				self.close()

			else:
				messagebox = QMessageBox(self)
				messagebox.setIcon(QMessageBox.Information)
				messagebox.setText("Incorrect UserID or Password      ")
				messagebox.setWindowTitle("Login Failed")
				messagebox.show()
				self.user_id_entry.clear()
				self.password_entry.clear()

		else:
			messagebox = QMessageBox(self)
			messagebox.setIcon(QMessageBox.Information)
			messagebox.setText("Please fill in you UserID and Password      ")
			messagebox.setWindowTitle("Empty boxes")
			messagebox.show()


	# Function to create widgets
	def createUI(self):
		self.setGeometry(X,Y,WIDTH,HEIGHT)
		self.setWindowTitle("Login")

		self.user_id_label = QLabel(self)
		self.user_id_label.setText("User ID :")
		self.user_id_label.move(250,170)
		self.user_id_label.setStyleSheet("color: black; font-family: Bahnschrift SemiBold; font-size:13pt")

		self.user_id_entry = QLineEdit(self)
		self.user_id_entry.resize(400,50)
		self.user_id_entry.move(250,200)
		self.user_id_entry.setStyleSheet("background-color: white; font-size:11pt; padding-left: 5px")

		self.password_label = QLabel(self)
		self.password_label.setText("Password :")
		self.password_label.move(250,270)
		self.password_label.setStyleSheet("color: black; font-family: Bahnschrift SemiBold; font-size:13pt")

		self.password_entry = QLineEdit(self)
		self.password_entry.resize(400,50)
		self.password_entry.move(250,300)
		self.password_entry.setEchoMode(QLineEdit.Password)
		self.password_entry.setStyleSheet("background-color: white; font-size:11pt; padding-left: 5px")

		self.sign_in_button = QPushButton(self)
		self.sign_in_button.setText("Sign In")
		self.sign_in_button.resize(120,40)
		self.sign_in_button.move(330,390)
		self.sign_in_button.clicked.connect(self.on_sign_in_click)

		self.exit_button = QPushButton(self)
		self.exit_button.setText("Exit")
		self.exit_button.resize(120,40)
		self.exit_button.move(470,390)
		self.exit_button.clicked.connect(self.on_exit_click)

class SecondWindow(QWidget):
	switch_to_third = pyqtSignal()

	def __init__(self):
		super().__init__()
		self.createUI()

	def on_play_pause_button_click(self):
		if not controller.playing:
			controller.playing = True
			self.play_pause_button.setText("Pause")
			self.play_pause_button.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaPause))
			controller.start_time = time.time()
		else:
			controller.playing = False
			self.play_pause_button.setText("Play")
			self.play_pause_button.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaPlay))
			end_time = time.time()
			controller.time_elapsed += end_time - controller.start_time

	def on_next_window_button_click(self):
		self.switch_to_third.emit()
		self.hide()


	def createUI(self):
		self.setGeometry(X,Y,WIDTH,HEIGHT)
		self.setWindowTitle("Data")
		self.setFocus(Qt.NoFocusReason)

		self.play_pause_button = QPushButton(self)
		self.play_pause_button.resize(100,30)
		self.play_pause_button.move(340,470)
		self.play_pause_button.setStyleSheet("background-color:lightblue; color:black; border-radius: 5px; font-size:10pt")
		self.play_pause_button.clicked.connect(self.on_play_pause_button_click)
		if controller.playing:
			self.play_pause_button.setText("Pause")
			self.play_pause_button.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaPause))
		else:
			self.play_pause_button.setText("Play")
			self.play_pause_button.setIcon(QApplication.style().standardIcon(QStyle.SP_MediaPlay))

		self.next_window_button = QPushButton(self)
		self.next_window_button.setText("Next")
		self.next_window_button.resize(100,30)
		self.next_window_button.move(460,470)
		self.next_window_button.setStyleSheet("background-color:lightblue; color:black; border-radius: 5px; font-size:10pt")
		self.next_window_button.clicked.connect(self.on_next_window_button_click)
		self.next_window_button.setIcon(QApplication.style().standardIcon(QStyle.SP_ArrowRight))

class ThirdWindow(QWidget):
	switch_to_second = pyqtSignal()

	def __init__(self):
		super().__init__()
		self.createUI()

	def on_previous_window_button_click(self):
		
		self.switch_to_second.emit()
		self.hide()

	def show_time(self):
		if controller.playing:
			elapsed = time.time() - controller.start_time
			elapsed += controller.time_elapsed
			time_string = str(datetime.timedelta(seconds=elapsed))[0:7]
			self.time_counter.setText(time_string)
			controller.last_time = time_string

	def createUI(self):
		self.setGeometry(X,Y,WIDTH,HEIGHT)
		self.setWindowTitle("Data")
		self.setFocus(Qt.NoFocusReason)

		self.time_counter = QLabel(self)
		self.time_counter.setText(controller.last_time)
		self.time_counter.resize(100,30)
		self.time_counter.setStyleSheet("font-size:15pt;color:darkgreen")
		self.time_counter.move(415,470)

		self.timer=QTimer()
		self.timer.timeout.connect(self.show_time)
		self.timer.start(1000)

		self.previous_window_button = QPushButton(self)
		self.previous_window_button.setText("Back")
		self.previous_window_button.resize(100,30)
		self.previous_window_button.move(400,510)
		self.previous_window_button.setStyleSheet("background-color:lightblue; color:black; border-radius: 5px; font-size:10pt")
		self.previous_window_button.clicked.connect(self.on_previous_window_button_click)
		self.previous_window_button.setIcon(QApplication.style().standardIcon(QStyle.SP_ArrowLeft))


# Class to handle switching between windows 
class Controller():

	start_time = None 
	time_elapsed = 0
	playing = False
	last_time = "0:00:00"

	def show_first(self):
		self.first_screen = FirstWindow()
		self.first_screen.switch_to_second.connect(self.show_second)
		self.first_screen.show()

	def show_second(self):
		self.second_screen = SecondWindow()
		self.second_screen.switch_to_third.connect(self.show_third)
		self.second_screen.show()

	def show_third(self):
		self.third_screen = ThirdWindow()
		self.third_screen.switch_to_second.connect(self.show_second)
		self.third_screen.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	controller = Controller()
	controller.show_first()
	sys.exit(app.exec_())
