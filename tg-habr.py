from telethon import TelegramClient, sync, events
from telethon import connection
# import requests, socket, socks
import datetime
from utils import hours_difference, extract_token_from_text
from  binance_list import white_list
import redis
import csv


from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import datetime

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
csv_file = "PUMP.csv"

# TG
api_id = 27387257
api_hash = 'ec0f197d81e5f284b4781b6a40aee202'
CHAT_ID = -1001816116832

# Binance
# api_key = "4B3z89iUniT0dbwRS7wIOWqxzBV7yVgDd5BWsviXki3P4FuC4dSyihiLxi22Y0nu"
# api_secret = "IOyB6P2AgrbEBrtsS2ehYEitisTg51lhJhmzftwZbYDr927wiKo89bdFSMUyAODV"


# proxy_server = "149.154.167.40"
# proxy_port = 443
# proxy_key = "/srv/Projects/bin-dupm/tg-pb/test.key"
# proxy = (proxy_server, proxy_port, proxy_key)




def main():
    """
    Main function
    """
    # bin_client = Client(api_key, api_secret)    
    # # get all symbol prices
    # prices = bin_client.get_all_tickers()
    # print("------------------  Current Binance Ticked Prices:  ------------------ ")
    # print(prices)
    with open("classmates.csv", mode="w", encoding='utf-8') as f:
        file_writer = csv.writer(f, delimiter = "\t")
        file_writer.writerow(["date", "timeshtamp", "token", "price", "price-1%", "price-2%", "price+1% "])

    client = TelegramClient('session_name', api_id, api_hash)
    # client = TelegramClient('session_name', api_id, api_hash,
    #     connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
    #     proxy=proxy)
    print("------------------  Parser started  ------------------ ")
    @client.on(events.NewMessage(chats=CHAT_ID))
    async def normal_handler(event):
        # print(event.message)

        user_mess=event.message.to_dict()['message']
        mess_date=event.message.to_dict()['date']
        token = extract_token_from_text(user_mess)
        time_stamp = datetime.datetime.timestamp(mess_date)

        # print(mess_date.strftime("%d-%m-%Y %H:%M:%S")+"\n")


        if token: 
            if  white_list(token):
                if "PUMP" in user_mess:
                    last = r.get(token)
                    if last:
                        hours_diff = hours_difference(time_stamp,float(last))
                    else:
                        hours_diff = float('inf')
                    # hours_diff = hours_difference(time_stamp,all_pump.get(token,0))
                    if hours_diff >= 1:
                        # print(user_mess)
                        print("Reseive: ",mess_date)
                        print("Token - ", token )
                        print("Unix timestamp: ", time_stamp, "\n")
                        f.write(mess_date.strftime("%d-%m-%Y %H:%M:%S")+","+str(time_stamp)+","+token+"\n")
                        # f.write(user+"\n")
                        # f.write(user_mess+"\n\n")
                        f.flush()
                    else:
                        print(f"This PUMP of {token} was recently: {hours_diff}" )
                else:
                    print("Dump we ignore: ", token )
                # Add to dict
                r.set(token, time_stamp )
                # all_pump[token] = time_stamp
                # print(all_pump)
            else:
                print(f"This token {token} are not on Binance...")
        else:
            print("This token are not USDT...")

        


    client.start()

    # group='group_name'

    # participants = client.get_participants(group)
    # users={}

    # for partic in client.iter_participants(group):
    #     lastname=""
    #     if partic.last_name:
    #        lastname=partic.last_name
    #     users[partic.id]=partic.first_name+" "+lastname

    f=open('pump.csv', 'a') 
    client.run_until_disconnected()
    f.close()


if __name__ == "__main__":
    main()