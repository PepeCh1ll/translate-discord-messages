import requests
from googletrans import Translator
import json
import time
import logging
import traceback

logger = logging.getLogger('Logs')
logger.setLevel(logging.INFO)

log = logging.FileHandler('logs.txt', encoding='utf-8')
log.setFormatter(logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s'))

logger.addHandler(log)


chat_id = input('Введите ID канала на сервере: ')
author_id = input('Введите ID вашего аккаунта: ')
lang =input('Введите язык чата в формате \'ru\': ')

header = {'authorization': input('Введите токен вашего аккаунта: ')}

message_id = ''

t = Translator()

print('\nДля выхода из программы просто закройте её')

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

		logger.info('Старт программы')
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
	print(traceback.format_exc())
	input('Произошла ошибка, просмотрите файл logs.txt или обратитесь за помощью к сотруднику\nНажмите Enter для выхода')
	logger.error('Произошла ошибка: ' + traceback.format_exc())
finally:
	logger.info('Завершение программы')