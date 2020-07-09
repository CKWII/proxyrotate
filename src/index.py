import requests, time
from random import choice
from bs4 import BeautifulSoup
import html5lib
import re
from itertools import cycle
import traceback
# LEARNED:
# for k,v in enumerate(pets):
# "ph1{} ph2{}".format("test","test2")

def PROXYROTATOR():
    # Regexes for data extraction.
    ipRegex = '(?!=\<td\>)(\d+\.\d+\.\d+\.\d+)(?=\<\/td>)'
    portRegex = '(?!=\<td\>)(\d+)(?=\<\/td>)'


    # Get available proxies.
    def get_proxies():
        proxies = []
        response = requests.get("https://sslproxies.org/")
        pageSoup = BeautifulSoup(response.content, 'html5lib')

        rawProxyRows = pageSoup.select('#proxylisttable tr')[1:20]

        for proxyRow in rawProxyRows:
            ip = re.search(ipRegex, str(proxyRow.contents[0])).group(1)
            port = re.search(portRegex, str(proxyRow.contents[1])).group(1)
            proxies.append(ip + ":" + port)

        return proxies


    # Random proxies so not straining the same one.
    def randomise(proxies):
        return choice(proxies)


    # Would improve script to keep track of proxy health status for swapping etc.

    proxies = get_proxies()
    proxy_pool = cycle(proxies)

    url = 'https://httpbin.org/ip'
    for i in range(1, 11):
        # Get a proxy from the pool
        proxy = next(proxy_pool)
        print("Request #%d" % i)
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy})
            print(response.json())
            time.sleep(1)
        except:
            print("Skipping. Connnection error")
            time.sleep(1)

    PROXYROTATOR()

PROXYROTATOR()
