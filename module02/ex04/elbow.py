import numpy as np
from sqlalchemy import create_engine, select, func
import matplotlib.pyplot as plt
from models import Customers
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans
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
        select(func.sum(Customers.price))
        .where(Customers.event_type == "purchase")
        .group_by(Customers.user_id)
    )

    response = session.scalars(statement)
    sales_per_customers = list(response)
    sales_per_customers = np.array(sales_per_customers).reshape(-1, 1)
    plt.style.use("seaborn-v0_8")
    within_square_errors = []
    for nb_clusters in range(1, 11):
        kmean = KMeans(n_clusters=nb_clusters).fit(sales_per_customers)
        within_square_errors.append((nb_clusters, kmean.inertia_))
    nb_clusters_list, ineratia_list = zip(*within_square_errors)
    plt.plot(nb_clusters_list, ineratia_list)
    plt.ticklabel_format(style="")
    plt.show()

    statement = (
        select(func.count())
        .where(Customers.event_type == "purchase")
        .group_by(Customers.user_id)
    )

    response = session.scalars(statement)
    purchase_per_customers = list(response)
    purchase_per_customers = np.array(purchase_per_customers).reshape(-1, 1)
    within_square_errors = []
    for nb_clusters in range(1, 11):
        kmean = KMeans(n_clusters=nb_clusters).fit(purchase_per_customers)
        within_square_errors.append((nb_clusters, kmean.inertia_))
    nb_clusters_list, ineratia_list = zip(*within_square_errors)
    plt.plot(nb_clusters_list, ineratia_list)
    plt.ticklabel_format(style="plain")
    plt.show()
