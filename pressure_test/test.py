from time import sleep

from requests import get
import random
import os
from threading import Thread

char_list = [str(i) for i in range(10)] +\
                         [chr(i + ord('a')) for i in range(26)] +\
                         [chr(i + ord('A')) for i in range(26)]
random.seed(os.urandom(16))
thread_cnt = 0
is_success = True


def fetch_random_url():
    """
    fetch a random url from short url server
    :return:
    """
    short_key = ''
    for i in range(6):
        short_key += random.choice(char_list)

    response = get("http://fuck.u:1234/" + short_key, timeout=5.)  # replace fuck.u with your own domain
    return response


def test_request():
    """
    request an short url from server and write result to is_success
    :return: None
    """
    global is_success

    try:
        response = fetch_random_url()
    except:
        # timeout or something are judged as server overload
        is_success = False
        return

    if response.status_code < 500:
        if response.status_code != 404:
            print(response.status_code, response.text)
    else:
        # HTTP code 5xx is judge as server overloaded
        is_success = False

adder = 1
while is_success:
    threads = []
    for i in range(thread_cnt + adder):
        threads.append(Thread(target=test_request))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    if is_success:
        # if success, do index increasing
        adder *= 2
    else:
        if adder == 1:
            # cannot add any more request concurrently
            break
        else:
            # begin next round of index increasing
            is_success = True
            thread_cnt, adder = thread_cnt + adder // 2, 1

print(thread_cnt)