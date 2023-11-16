import os
from dotenv import load_dotenv
import time
import asyncio
from binance import AsyncClient

load_dotenv()
api_key = os.getenv('api_key_read')
api_secret = os.getenv('api_secret_read')

async def main():
    client = await AsyncClient.create(api_key, api_secret)

    start = time.time()
    prices = await client.futures_symbol_ticker()
    # print(client.response.headers)
    end = time.time()
    print("The time of execution ALL program is :",   (end-start) * 10**3, "ms")

    start = time.time()
    prices = await client.futures_symbol_ticker(symbol="BTCUSDT")
    # print(client.response.headers)
    end = time.time()
    print("The time of execution of BTCUSDT program is :", (end-start) * 10**3, "ms")

    start = time.time()
    prices = await client.futures_symbol_ticker(symbol="LOOMUSDT")
    # print(client.response.headers)
    end = time.time()
    print("The time of execution of LOOMUSDT program is :", (end-start) * 10**3, "ms")

    start = time.time()
    res = await client.get_exchange_info()
    # print(client.response.headers)
    end = time.time()
    print("The time of ONLY REQUEST of above program is :", (end-start) * 10**3, "ms")

    await client.close_connection()

if __name__ == "__main__":

    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end = time.time()
    print("The time of execution of above program is :", (end-start) * 10**3, "ms")
