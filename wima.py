import json
import aiohttp

__TIMES__ = 10


async def wima():
    from lxml import etree
    conn = aiohttp.TCPConnector(ssl=False, ttl_dns_cache=30)
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout, connector=conn) as s:
        for idx in range(0, __TIMES__):
            r = await do(s, 'https://ipinfo.io/')
            x = etree.HTML(r).xpath('//script[@id="__NEXT_DATA__" and @type="application/json"]')
            if x:
                u_ip = json.loads(x[0].text)['props']['pageProps']['userIp']
                r = await do(s, 'https://ipinfo.io/widget/demo/%s' % u_ip)
                try:
                    d = json.loads(r)['data']
                    ip = d['ip']
                    network = d['abuse']['network'] if 'abuse' in d else None
                    city = d['city']
                    region = d['region']
                    country = d['country']
                    org = d['org']
                    print('ip: %s network: %s city: %s region: %s country: %s org: %s' % (
                        ip, network, city, region, country, org))
                except Exception as e:
                    exit(e)
            else:
                pass


async def do(session, url):
    headers = {
        'referer': 'https://ipinfo.io/',
        'User-Agent': random_ua()
    }
    async with session.get(url, headers=headers) as r:
        if 200 == r.status:
            r = await r.text()
            return r


def random_ua():
    import random
    return random.choice([
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
        'Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 '
        'Mobile/11A465 Safari/9537.53 BingPreview/1.0b',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/33.0.0.0 Safari/534.24'
    ])


if __name__ == '__main__':
    import asyncio
    import os

    if 'nt' == os.name:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(wima())
    else:
        asyncio.run(wima())
