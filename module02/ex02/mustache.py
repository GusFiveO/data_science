from sqlalchemy import create_engine, select, func
import matplotlib.pyplot as plt
from models import Customers
from sqlalchemy.orm import Session
import pandas as pd

user = "alorain"
password = "mysecretpassword"
host = "127.0.0.1"
port = "5432"
database = "piscineds"

url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(url)
with Session(engine) as session:
    statement = (
        select(Customers.price)
        .where(Customers.event_type == "purchase")
        .order_by(Customers.price)
    )

    response = session.execute(statement)
    purchased_product_price_list = list(response)
    price_df = pd.DataFrame(purchased_product_price_list)
    print(price_df.describe().apply(lambda s: s.apply("{0:.5f}".format)))
    plt.style.use("seaborn-v0_8")
    plt.boxplot(price_df, sym="gD", widths=0.75, vert=False)
    plt.show()
    plt.boxplot(price_df, sym="", widths=0.75, vert=False)
    plt.show()

    statement = (
        select(func.sum(Customers.price))
        .where(Customers.event_type == "purchase")
        .group_by(Customers.user_id)
    )

    response = session.execute(statement)
    average_basket_price_per_user = list(response)
    average_basket_df = pd.DataFrame(average_basket_price_per_user)
    # print(average_basket_df.describe().apply(lambda s: s.apply("{0:.5f}".format)))
    plt.boxplot(average_basket_df, sym="gD", widths=0.75, vert=False)
    plt.show()
