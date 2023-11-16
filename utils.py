from datetime import datetime

import re

def extract_token_from_text(text):
    """Extract Tokeen from string"""
    pattern = re.compile(r'https://www.bybit.com/trade/usdt/(\w+)')
    match = pattern.search(text)
    
    if match:
        return match.group(1)
    else:
        return None

def f_write(mess_date, token, time_stamp):
    f.write(mess_date.strftime("%d-%m-%Y %H:%M:%S")+"\n")
    f.write(token, +"\n")
    f.write(time_stamp, +"\n\n")
    # f.write(user+"\n")
    # f.write(user_mess+"\n\n")
    f.flush()

def hours_difference(now, last):
    # Преобразование timestamp обратно в объект datetime
    now = datetime.utcfromtimestamp(now)
    last = datetime.utcfromtimestamp(last)
    
    # Вычисление разницы во времени
    time_difference = now - last
    
    # Получение разницы в часах
    hours = time_difference.total_seconds() / 3600
    
    return hours


def main():
# Пример использования:
    timestamp1 = 1641456399.0  # Замените это значением вашего первого timestamp
    timestamp2 = 0 # Замените это значением вашего второго timestamp

    result = hours_difference(timestamp1, timestamp2)
    print(f'Разница в часах: {result} часов')

if __name__ == "__main__":
    main()
