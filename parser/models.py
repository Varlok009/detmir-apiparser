from sqlalchemy import JSON, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db_parser import Base, engine


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    name = Column(String())
    price = Column(Float)
    cities = Column(JSON)
    promo_price = Column(Float)
    link = Column(String())

    def __repr__(self) -> str:
        return f'product {self.id}, {self.name}'


# class City(Base):
#     __tablename__ = "cities"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String())
#     products = relationship("Product", lazy='subquery')
#
#     def __repr__(self) -> str:
#         return f'city {self.id}, {self.name}'

#
# class ProductCity(Base):
#     __tablename__ = "products_cities"
#
#     id = Column(Integer, primary_key=True)
#     product_id = Column(Integer, ForeignKey('products.id'))
#     city_id = Column(Integer, ForeignKey('cities.id'))
#
#     def __repr__(self) -> str:
#         return f'product {self.id}, {self.name}, city {self.id}, {self.name}'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)