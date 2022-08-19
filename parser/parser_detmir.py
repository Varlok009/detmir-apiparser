from models import Product
from random import randint, choice
from add_to_db import add_product_to_db
import json
import time
import requests
from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout


user_agent_list = []
ip_list = []

with open('user_agents.txt', 'r') as ua:
    user_agents = ua.read().split('\n')
    user_agent_list.extend(user_agents)

with open('ip.txt', 'r') as ip:
    ips = ip.read().split('\n')
    ip_list.extend(ips)


def get_user_agent(user_agents: list) -> str:
    return choice(user_agents)


def get_proxy(ip_list: list) -> str:
    return choice(ip_list)


def get_products(limit=100, offset=0) -> json:
    session = requests.Session()
    link = f'https://api.detmir.ru/v2/products?filter=categories[].alias:lego&limit={limit}&offset={offset}'

    pr = get_proxy(ip_list)
    proxy = {
        'http': f'http://{pr}',
        'https': f'http://{pr}'
    }
    agent = {'User-Agent': get_user_agent(user_agent_list),
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
             'Referer': 'https://www.yandex.ru/',
             }
    session.proxies = proxy
    session.headers.update(agent)
    r = session.get(link, timeout=5)
    print(r.request.url, session.proxies)
    products = json.loads(r.text)
    return products


def parse_products(products: json) -> list[Product]:
    products_list = []
    for product in products:
        new_item = Product(**{
                    'product_id': product['id'],
                    'name': product['title'],
                    'price': product['old_price']['price'] if product['old_price'] else product['price']['price'],
                    'cities': json.dumps(product['available']['offline']['region_iso_codes']),
                    'promo_price': product['price']['price'] if product['old_price'] else None,
                    'link': product['link']['web_url'],
        })
        products_list.append(new_item)
    return products_list


if __name__ == '__main__':
    offset = 0
    step_offset = 100
    while True:
        try:
            products = get_products(offset=offset)
        except ProxyError:
            print('fail proxy')
            continue
        except ConnectTimeout:
            print('fail connect timeout')
            continue
        except ReadTimeout:
            print('fail read timeout')
            continue
        except:
            print('fail xz')
            continue

        products = parse_products(products)
        for product in products:
            try:
                add_product_to_db(product)
            except:
                print('error add to db')
                continue
        print('sliip')
        time.sleep(randint(15, 60))
        if len(products) == 0:
            print('end parsing')
            break
        offset += step_offset
