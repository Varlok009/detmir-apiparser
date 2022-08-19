from db_parser import db_session
from models import Product


def add_product_to_db(new_item: Product) -> None:
    db_session.add(new_item)
    db_session.commit()
    try:
        db_session.add(new_item)
        db_session.commit()
    except:
        print(f'error {new_item.product_id} - {new_item.name}')
        db_session.rollback()
