# Автоматический перевод ваших сообщений в Discord
Скрипт, позволяющий автоматически переводить отправленные вами сообщения в Discord

## Инструкция
1. Установите Python на ваш ПК
2. Установить библиотеки командой `pip install -r requirements.txt`
3. Запустите `main.py`

## Q&A
### Как узнать ID канала?
1. Зайдите в настройки вашего аккаунта в Discord
2. Перейдите в "Расширенные"
3. Включите "Режим разработчика"
4. ПКМ по каналу, "Копировать ID"

### Как узнать ID своего аккаунта?
1. Зайдите в настройки вашего аккаунта в Discord
2. Перейдите в "Расширенные"
3. Включите "Режим разработчика"
4. ПКМ по нику в любом чате, "Копировать ID"

### Как узнать токен?
1. Откройте Web Версию Discord
2. Нажмите Ctrl+Shift+I
3. Перейдите во вкладку "Network" ("Сеть")
4. Пропишите в графе "Фильтр" -> "api"
5. Перезагрузите страницу с помощью Ctrl+R
6. Нажмите по любой из появившихся белых надписей
7. Проскрольте до графы "Заголовки запроса"
8. Найдите параметр "authorization"
9. Всё, что идёт после двоеточия - ваш токен
10. Скопируйте с помощью ПКМ -> Копировать значение
