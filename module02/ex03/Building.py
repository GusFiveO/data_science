import numpy as np
from sqlalchemy import create_engine, distinct, select, func
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
        # select(func.count(distinct(Customers.user_session)))
        select(func.count())
        .where(Customers.event_type == "purchase")
        .group_by(Customers.user_id)
    )

    response = session.scalars(statement)
    order_frequency = list(response)
    # max = max(order_frequency)
    bins = np.arange(0, 50, 10)
    plt.style.use("seaborn-v0_8")
    plt.hist(order_frequency, bins=bins)
    plt.xticks(bins)
    plt.ylabel("customers")
    plt.xlabel("frequency")
    plt.title("Cutomers purchase frequency")
    plt.show()

    statement = (
        select(func.sum(Customers.price))
        .where(Customers.event_type == "purchase")
        .group_by(Customers.user_id)
    )

    response = session.scalars(statement)
    alt_spent_per_customer = list(response)
    bins = np.arange(0, 201, 50)
    plt.hist(alt_spent_per_customer, bins=bins)
    plt.xticks(bins)
    plt.ylabel("customers")
    plt.xlabel("monetary value in ₳")
    plt.title("Monetary distribution")
    plt.show()
