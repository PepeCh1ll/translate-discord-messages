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

class mywindow(QtWidgets.QMainWindow):
	def translate(self):
		logger = logging.getLogger('Logs')
		logger.setLevel(logging.INFO)

		log = logging.FileHandler('logs.txt', encoding='utf-8')
		log.setFormatter(logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s'))

		logger.addHandler(log)

		self.ui.lineEdit.setReadOnly(True)
		self.ui.lineEdit_2.setReadOnly(True)
		self.ui.lineEdit_3.setReadOnly(True)
		self.ui.lineEdit_4.setReadOnly(True)

		chat_id = self.ui.lineEdit.text()
		author_id = self.ui.lineEdit_2.text()
		lang = self.ui.lineEdit_3.text()

		header = {'authorization': self.ui.lineEdit_4.text()}

		message_id = ''

		t = Translator()

		try:
			with requests.Session() as s:
				r = s.get(f'https://discord.com/api/v9/channels/{chat_id}/messages?limit=3', headers=header)
				result = json.loads(r.text)
				for i in result:
					if i['author']['id'] == author_id:
						message = i['content']
						msg_id = i['id']
						break
				message_id = msg_id

				logger.info('Старт потока')
				while True:
					r = s.get(f'https://discord.com/api/v9/channels/{chat_id}/messages?limit=3', headers=header)
					result = json.loads(r.text)
					for i in result:
						if i['author']['id'] == author_id:
							message = i['content']
							msg_id = i['id']
							break
					if msg_id == message_id:
						continue
					else:
						message_id = msg_id

					logger.info('Принято сообщение: ' + message)
					message = t.translate(message, dest=lang).text
					payload = {'content': message.capitalize()}
					r = s.patch(f'https://discord.com/api/v9/channels/{chat_id}/messages/{message_id}', headers=header, json=payload)
					logger.info('Сообщение переведено: ' + message)

					time.sleep(0.3)

		except Exception as e:
			logger.error('Произошла ошибка: ' + traceback.format_exc())

			self.msg = QMessageBox()
			self.msg.setWindowTitle("Ошибка")
			self.msg.setText("Произошла ошибка, просмотрите файл logs.txt или обратитесь за помощью к сотруднику")
			self.msg.setIcon(QMessageBox.Critical)
			self.msg.exec_()
		finally:
			logger.info('Завершение потока')
			sys.exit()

	def __init__(self):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.ui.pushButton.clicked.connect(self.starting)
		self.th = Thread(target=self.translate, daemon=True)

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