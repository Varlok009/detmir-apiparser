from sqlalchemy import JSON, Column, Integer, String
from db_parser import Base, engine


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String())

    def __repr__(self) -> str:
        return f'product {self.id}, {self.name}'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)