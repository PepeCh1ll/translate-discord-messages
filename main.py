from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from window import Ui_MainWindow
import sys
import requests
from googletrans import Translator
import json
import time
import logging
import traceback
from threading import Thread
import configparser

class mywindow(QtWidgets.QMainWindow):
	def translate(self):
		self.logger = logging.getLogger('Logs')
		self.logger.setLevel(logging.INFO)

		self.log = logging.FileHandler('logs.txt', encoding='utf-8')
		self.log.setFormatter(logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s'))

		self.logger.addHandler(self.log)

		self.ui.lineEdit.setReadOnly(True)
		self.ui.lineEdit_2.setReadOnly(True)
		self.ui.lineEdit_3.setReadOnly(True)
		self.ui.lineEdit_4.setReadOnly(True)

		self.chat_id = self.ui.lineEdit.text()
		self.author_id = self.ui.lineEdit_2.text()
		self.lang = self.ui.lineEdit_3.text()

		self.header = {'authorization': self.ui.lineEdit_4.text()}

		self.message_id = ''
		self.msg_id = ''

		self.t = Translator()

		try:
			with requests.Session() as self.s:
				self.r = self.s.get(f'https://discord.com/api/v9/channels/{self.chat_id}/messages?limit=3', headers=self.header)
				self.result = json.loads(self.r.text)
				for i in self.result:
					if i['author']['id'] == self.author_id:
						self.message = i['content']
						self.msg_id = i['id']
						break
				self.message_id = self.msg_id

				while True:
					self.r = self.s.get(f'https://discord.com/api/v9/channels/{self.chat_id}/messages?limit=3', headers=self.header)
					self.result = json.loads(self.r.text)
					for i in self.result:
						if i['author']['id'] == self.author_id:
							self.message = i['content']
							self.msg_id = i['id']
							break
					if self.msg_id == self.message_id:
						continue
					else:
						self.message_id = self.msg_id

					self.logger.info('Принято сообщение: ' + self.message)
					self.message = self.t.translate(self.message, dest=self.lang).text
					self.payload = {'content': self.message.capitalize()}
					self.r = self.s.patch(f'https://discord.com/api/v9/channels/{self.chat_id}/messages/{self.message_id}', headers=self.header, json=self.payload)
					self.logger.info('Сообщение переведено: ' + self.message)
					self.s.cookies.clear()

		except Exception as e:
			self.logger.error('Произошла ошибка: ' + traceback.format_exc())

			self.msg = QMessageBox()
			self.msg.setWindowTitle("Ошибка")
			self.msg.setText("Произошла ошибка, просмотрите файл logs.txt или обратитесь за помощью к сотруднику")
			self.msg.setIcon(QMessageBox.Critical)
			self.msg.exec_()
		finally:
			self.logger.info('Завершение потока')
			sys.exit()

	def __init__(self):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.p = [250, 210, 100, 30]
		self.w = [500, 250]
		self.btns = []

		self.ui.pushButton.clicked.connect(self.starting)
		self.th = Thread(target=self.translate, daemon=True)

		self.parser = configparser.ConfigParser()
		self.parser.read('users.ini')
		self.x = 100
		self.y = 170
		for el in self.parser.sections():
			if self.x == 500:
				self.x = 100
				self.y += 30
				self.p[1] += 30
				self.ui.pushButton.setGeometry(self.p[0], self.p[1], self.p[2], self.p[3]) 
				self.w[1] += 30
				self.setFixedSize(self.w[0], self.w[1])
			self.btn = QtWidgets.QPushButton(self)
			self.btn.setObjectName(el)
			self.btns.append(el)
			self.btn.setText(el)
			self.btn.setGeometry(self.x, self.y, 100, 30)
			self.btn.clicked.connect(self.account)
			self.x += 100
		self.ui.lineEdit.setText(self.parser['user1']['chat'])
		self.ui.lineEdit_2.setText(self.parser['user1']['auth'])
		self.ui.lineEdit_3.setText(self.parser['user1']['language'])
		self.ui.lineEdit_4.setText(self.parser['user1']['token'])

	def account(self, btns):
		self.button = QtWidgets.QApplication.instance().sender()
		self.ui.lineEdit.setText(self.parser[self.button.text()]['chat'])
		self.ui.lineEdit_2.setText(self.parser[self.button.text()]['auth'])
		self.ui.lineEdit_3.setText(self.parser[self.button.text()]['language'])
		self.ui.lineEdit_4.setText(self.parser[self.button.text()]['token'])

	def starting(self):
		self.th.start()

		self.msg = QMessageBox()
		self.msg.setWindowTitle("Внимание")
		self.msg.setText("Перевод запущен\nДля остановки просто закройте приложение\nНе нажимайте повторну кнопку Старт, это приведет к ошибке")
		self.msg.setIcon(QMessageBox.Information)
		self.msg.exec_()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())