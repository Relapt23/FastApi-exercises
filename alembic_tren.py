from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from pydantic import BaseModel


engine = create_engine("sqlite:///database.db", echo=True)

class Base(DeclarativeBase): pass
Session = sessionmaker(autoflush=False, bind=engine)
class Product(Base):
    __tablename__ = "products2"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    title = Column(String)
    price = Column(Integer)
    count = Column(Integer)
    description = Column(String)
    color = Column(String)

Base.metadata.create_all(bind=engine,checkfirst=True)

class Products(BaseModel):
    title: str
    price: int
    count: int
    description: str
    color: str


app = FastAPI()

@app.post("/add")
def add_product(product_data: Products):
    with Session(autoflush=False, bind=engine) as session:
        product = Product(title = product_data.title, price =product_data.price, count =product_data.count, description = product_data.description)
        session.add(product)
        session.commit()
        session.refresh(product)
        products = session.query(Product).all()
    for p in products:
        if p.title == product_data.title:
            return {f"{p.id}.{p.title} ({p.price})"}
        pass


