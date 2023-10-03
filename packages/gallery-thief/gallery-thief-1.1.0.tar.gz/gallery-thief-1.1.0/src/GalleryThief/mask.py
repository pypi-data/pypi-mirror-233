import random
import time
import requests
from typing import List, Dict
from numpy import random as rnd  # type: ignore
from fake_useragent import UserAgent  # type: ignore

Proxy = Dict[str, str]
ProxyList = List[Proxy]

refer = [
    "https://google.com",
    "https://ya.ru",
    "https://vk.com",
    "https://bing.com",
    "https://duckduckgo.com",
    "https://dzen.ru"
]


def check_proxy(ip: str, port: str) -> bool:
    try:
        response = requests.get(
            "https://example.com",
            proxies={"http": f"http://{ip}:{port}"}
        )
        if response.status_code != 200:
            return False
    except Exception:
        return False
    return True


class RobberMask():
    '''
    Implements captcha avoiding algorithm.
    '''

    def __init__(self, source: str, proxies_limit: int = 0) -> None:
        '''
        Initializing RobberMask and loading proxy servers list.

        source -> url of proxies list in txt format.\n
        proxies_limit -> how many servers must be checked.\n
                         if 0 or less then all of them in list.
        '''

        proxies_response = requests.get(source)
        proxies_txt = proxies_response.text
        proxies_list = proxies_txt.split('\n')
        if proxies_limit > 0:
            proxies_list = proxies_list[0:proxies_limit-1]
        unchecked = [
            {
                "ip": p.split(':')[0],
                "port": p.split(':')[1]
            } for p in proxies_list if p and ('#' not in p)
        ]

        self._proxies: ProxyList = [p for p in unchecked if check_proxy(**p)]
        self._current_proxy: Proxy = {}
        self._time_mark = 0

    def reach_out(self, url: str, params: Dict = {}) -> str:
        while self._time_mark > time.time():
            pass
        self._time_mark = time.time() + rnd.uniform(2.0, 4.0)
        if not self._proxies:
            raise Exception('No proxies available')
        while True:
            headers = {
                "User-Agent": UserAgent().random,
                "refer": random.choice(refer)
            }
            current_proxy = random.choice(self._proxies)
            ip = current_proxy['ip']
            port = current_proxy['port']
            response = requests.get(
                url,
                params=params,
                headers=headers,
                proxies={"http": f"http://{ip}:{port}"}
            )

            if response.ok:
                break

        return response.text
