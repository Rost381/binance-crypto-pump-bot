import os
from dotenv import load_dotenv
import csv
import time
import asyncio
from aiohttp import ClientSession

load_dotenv()
api_key = os.getenv('api_key_read')
api_secret = os.getenv('api_secret_read')

def time_counter(f):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        c = f(*args, **kwargs)
        request_time = time.perf_counter() - start
        print(f"Request completed in {request_time} sec")
        return c
    return inner

@time_counter
def mult(x,y):
    time.sleep(5)
    print("I am MULT")
    return x**y

print(mult(3,5000))

async def get_weather(city):
    async with ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            print(f'{city}: {weather_json["weather"][0]["main"]}')


async def main(cities_):
    tasks = []
    for city in cities_:
        tasks.append(asyncio.create_task(get_weather(city)))

    for task in tasks:
        await task


cities = ['Moscow', 'St. Petersburg', 'Rostov-on-Don', 'Kaliningrad', 'Vladivostok',
          'Minsk', 'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York']

print(time.strftime('%X'))
start = time.perf_counter()

asyncio.run(main(cities))

request_time = time.perf_counter() - start
print("Request completed in {0:.000f}ms".format(request_time))
print(time.strftime('%X'))



'''
async def fun1(x):
    print(x**2)
    await asyncio.sleep(3)
    print('fun1 завершена')


async def fun2(x):
    print(x**0.5)
    await asyncio.sleep(3)
    print('fun2 завершена')


async def main():
    task1 = asyncio.create_task(fun1(4))
    task2 = asyncio.create_task(fun2(4))

    await task1
    await task2


print(time.strftime('%X'))

asyncio.run(main())

print(time.strftime('%X'))
'''