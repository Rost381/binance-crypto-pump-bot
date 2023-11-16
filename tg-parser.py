import configparser
import json



from telethon.sync import TelegramClient
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest


# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

print(type(api_id), type(api_hash), type(username) )

client = TelegramClient(username, api_id, api_hash)

proxy_server = "149.154.167.40"
proxy_port = 443
proxy_key = "/srv/Projects/bin-dupm/tg-pb/test.key"

proxy = (proxy_server, proxy_port, proxy_key)

client = TelegramClient(username, api_id, api_hash,
    connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
    proxy=proxy)
print(client)
input()
