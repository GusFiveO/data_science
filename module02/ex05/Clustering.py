import datetime
from matplotlib.ticker import EngFormatter
import numpy as np
from sqlalchemy import case, create_engine, select, func
import matplotlib.pyplot as plt
from models import Customers
from sqlalchemy.orm import Session
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd

user = "alorain"
password = "mysecretpassword"
host = "127.0.0.1"
port = "5432"
database = "piscineds"

url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(url)
with Session(engine) as session:
    statement = select(
        func.count(case((Customers.event_type == "purchase", 1))).label(
            "purchase_frequency"
        ),
        func.sum(
            case(
                (Customers.event_type == "purchase", Customers.price),
                else_=0,
            )
        ).label("total_spent"),
    ).group_by(Customers.user_id)
    response = session.execute(statement)
    customers_features = list(response)
    customers_features_df = pd.DataFrame(customers_features)

    print(customers_features_df)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(customers_features_df)
    print(data_scaled)
    wcss = []
    # for i in range(1, 11):
    #     kmeans = KMeans(
    #         n_clusters=i, init="k-means++", max_iter=300, n_init=10, random_state=0
    #     )
    #     kmeans.fit(data_scaled)
    #     wcss.append(kmeans.inertia_)

    kmeans = KMeans(
        n_clusters=4, init="k-means++", max_iter=300, n_init=10, random_state=0
    )
    customers_features_df["Cluster"] = kmeans.fit_predict(data_scaled)

    for cluster in customers_features_df["Cluster"].unique():
        clustered_data = customers_features_df[
            customers_features_df["Cluster"] == cluster
        ]
        plt.scatter(
            clustered_data["purchase_frequency"],
            clustered_data["total_spent"],
            label=f"Cluster {cluster}",
        )

    # Plot cluster centers
    centers = scaler.inverse_transform(kmeans.cluster_centers_)
    plt.scatter(
        centers[:, 0],
        centers[:, 1],
        color="black",
        marker="x",
        s=100,
        label="Centroids",
    )

    plt.style.use("seaborn-v0_8")

    plt.title("Customer Clusters by Purchase Frequency and Total Spent")
    plt.xlabel("Purchase Frequency")
    plt.ylabel("Total Spent")
    plt.legend()
    plt.show()

    cluster_counts = customers_features_df["Cluster"].value_counts()
    total_spent_per_cluster = customers_features_df.groupby("Cluster")[
        "total_spent"
    ].sum()

    # Plot the bar chart
    plt.figure(figsize=(8, 5))
    total_spent_per_cluster.plot(kind="bar", color=["blue", "green", "orange", "red"])

    plt.title("Total sales in Each Cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Total sales")

    plt.ticklabel_format(style="plain", axis="y")
    formatter = EngFormatter()
    plt.gca().yaxis.set_major_formatter(formatter)

    plt.show()
