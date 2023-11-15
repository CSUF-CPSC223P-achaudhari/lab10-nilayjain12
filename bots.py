import threading
import json
from time import sleep

def bot_fetcher(items, cart, lock):#delay

    inventory = {}
    with open('inventory.dat', 'r') as f:
        inventory = json.load(f)

    for key in items:
        value = inventory[key]
        duration = value[1]
        item = value[0]
        sleep(duration)
        lock.acquire()
        cart.append([key, item])
        lock.release()

def bot_clerk(items):

    bot0 = []
    bot1 = []
    bot2 = []
    cart = []
    lock = threading.Lock()
    for n, key in enumerate(items):
        bot_num = n % 3
        if bot_num == 0:
            bot0.append(key)
        elif bot_num == 1:
            bot1.append(key)
        elif bot_num == 2:
            bot2.append(key)
    #print('bot0: ', bot0)
    #print('bot1: ', bot1)
    #print('bot2: ', bot2)

    threads = []
    if len(bot0) > 0:
        t = threading.Thread(target=bot_fetcher, args=(bot0, cart, lock))
        t.start()
        threads.append(t)
    if len(bot1) > 0:
        t = threading.Thread(target=bot_fetcher, args=(bot1, cart, lock))
        t.start()
        threads.append(t)
    if len(bot2) > 0:
        t = threading.Thread(target=bot_fetcher, args=(bot2, cart, lock))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return cart
