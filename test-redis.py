import redis
from utils import hours_difference
import pickle
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# t1 = input("first timestamp: ")
# r.set('foo', [t1,"ABC","ZXC"])
# t2 = float(input("Second timestamp: "))
# r.set('bar', t2)
# print(type(t2))
# rt1 = float(r.get('foo'))
# rt2 = float(r.get('bar'))


# result = hours_difference(rt1, rt2)
# print(f'Разница в часах: {result} часов')

rrr = r.get('fuck')
print(f'{rrr=}')


# tup1 = ['2011-04-05', 25.2390232323, 0.32093240923490, 'abc']
# t1 = pickle.dumps(tup1)
# print(t1)
# r.lpush('foo', tup1)
# v = r.lpop('foo')
# print(v)


