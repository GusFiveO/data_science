from sqlalchemy import Column, Time, Text, Integer, Float, BigInteger, Uuid
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Customers(Base):
    __tablename__ = "customers"

    event_time = Column(Time, primary_key=True)
    event_type = Column(Text)
    product_id = Column(Integer)
    price = Column(Float)
    user_id = Column(BigInteger)
    user_session = Column(Uuid)

    def __repr__(self):
        print(
            f"event_time: {self.event_time}\
                | event_type: {self.event_type}|\
                      product_id: {self.product_id}|\
                          price: {self.price}|\
                              user_id: {self.user_id}|\
                                  user_session: {self.user_session}\n"
        )
