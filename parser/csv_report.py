import csv
from db_parser import db_session
from models import Product


def create_csv_report(city: str) -> None:
    with open(f'city_{city}.csv', 'a', encoding='utf-8', newline='') as target_file:
        fields = ['id', 'name', 'price', 'city', 'promo_price', 'link']
        writer = csv.DictWriter(target_file, fields, delimiter=';')
        writer.writeheader()
        products = db_session.query(Product).filter(Product.cities.contains('RU-MOW')).all()
        for product in products:
            try:
                writer.writerow({'id': product.product_id,
                                 'name': product.name,
                                 'price': product.price,
                                 'city': city,
                                 'promo_price': product.promo_price,
                                 'link': product.link,
                                 })
            except ValueError:
                print(f'error: {product}')
                continue


if __name__ == '__main__':
    for city in ['RU-MOW', 'RU-SPE']:
        create_csv_report(city)
