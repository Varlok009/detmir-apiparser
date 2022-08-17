from db_parser import db_session
from models import Products
import json

with open('js.txt', 'r') as p:
    products = p.read()
    # products = json.dumps([products])
    products = json.loads(products)
    # print(products, type(products))
    for item in products:
        print(item)
        new_item = Products(**item)
        try:
            db_session.add(new_item)
            db_session.commit()
        except:
            db_session.rollback()
