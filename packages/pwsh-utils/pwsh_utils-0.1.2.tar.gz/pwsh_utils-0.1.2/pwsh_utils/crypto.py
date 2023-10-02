import os

import requests


def btc_etc()->str:
    proxies = None
    my_proxy = os.getenv('MY_PROXY')
    if my_proxy is not None:
        proxies = {"http": my_proxy, "https": my_proxy, }

    resp = requests.get("https://api.binance.com/api/v3/ticker/price?symbols=[%22BTCUSDT%22,%22ETHUSDT%22]",
                        proxies=proxies)

    p = []
    for item in resp.json():
        p.append(format(float(item["price"]), '.2f'))

    return '🍕'.join(p)