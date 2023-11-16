import os
from dotenv import load_dotenv
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import datetime
import time

load_dotenv()
api_key = os.getenv('api_key_read')
api_secret = os.getenv('api_secret_read')


client = Client(api_key, api_secret)

# get all symbol prices
# prices = client.get_all_tickers()

# resived_time = datetime.datetime.now()
# resived_timestamp = datetime.datetime.timestamp(resived_time)

# expand_price = {}
# for price in prices:
#     price["date"] = resived_time
#     price["timestamp"] = resived_timestamp

# print(prices)

#--------
start = time.time()

prices = client.futures_symbol_ticker()

end = time.time()
print("The time of execution of above program is :",   (end-start) * 10**3, "ms")

#---------
start = time.time()

prices = client.futures_symbol_ticker(symbol="BTCUSDT")

end = time.time()
print("The time of execution of above program is :", (end-start) * 10**3, "ms")

#---------
start = time.time()
prices = client.futures_symbol_ticker(symbol="LOOMUSDT")
end = time.time()
print("The time of execution of above program is :", (end-start) * 10**3, "ms")

#---------


start = time.time()
res = client.get_exchange_info()
end = time.time()
print("The time of execution of above program is :", (end-start) * 10**3, "ms")


print(client.response.headers)

# input("Press 'Enter' to continue")
# f=open('coins.csv', 'a') 
# for price in prices:
#     print(price["symbol"])
#     f.write("\""+price['symbol']+"\","+"\n")
#     # f.write(user+"\n")
#     # f.write(user_mess+"\n\n")
#     f.flush()
# f.close()
# print(len(prices))





# for price in prices:
#     if "WBTCUSDT" in price["symbol"]:
#         print(price)


