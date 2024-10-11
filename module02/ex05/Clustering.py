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


def elbow_method(df, iterations):
    within_square_errors = []
    for nb_clusters in range(1, iterations + 1):
        kmean = KMeans(n_clusters=nb_clusters).fit(df)
        within_square_errors.append((nb_clusters, kmean.inertia_))
    nb_clusters_list, ineratia_list = zip(*within_square_errors)

    plt.plot(nb_clusters_list, ineratia_list)
    plt.ticklabel_format(style="")
    plt.ylabel("WCSS")
    plt.xlabel("Number of clusters")
    plt.show()


def preprocess_data(df, scaler, column_list):
    data_scaled = scaler.fit_transform(df[column_list])
    return data_scaled


def plot_clusters(df, centroids, labels, colors):
    for cluster in customers_features_df["Cluster"].unique():
        clustered_data = df[df["Cluster"] == cluster]
        plt.scatter(
            clustered_data["difference"],
            clustered_data["purchase_count"],
            label=labels[cluster],
            color=colors[cluster],
        )

    plt.scatter(
        centroids[:, 0],
        centroids[:, 1],
        color="black",
        marker="x",
        s=100,
        label="Centroids",
    )
    plt.ylim(bottom=0)
    plt.title("Customer Clusters by Purchase Frequency and Total Spent")
    plt.ylabel("number of purchase")
    plt.xlabel("average day of purchases")
    plt.legend()
    plt.show()


def plot_cluster_distribution(df, labels, color):

    cluster_counts = df["Cluster"].value_counts()
    cluster_counts.index = cluster_counts.index.map(labels)

    plt.barh(
        cluster_counts.index,
        cluster_counts.values,
        color=color,
    )

    plt.title("Customers in Each Cluster")
    plt.ylabel("Cluster")
    plt.xlabel("number of customers")

    plt.ticklabel_format(style="plain", axis="x")
    formatter = EngFormatter()
    plt.gca().xaxis.set_major_formatter(formatter)

    plt.show()


engine = create_engine(url)
with Session(engine) as session:

    cte = select(
        func.max(func.date_trunc("day", Customers.event_time)).label("latest_day")
    ).cte("max_day")

    statement = (
        select(
            Customers.user_id,
            func.count(Customers.event_type).label("purchase_count"),
            func.avg(
                func.extract(
                    "day",
                    cte.c.latest_day - func.date_trunc("day", Customers.event_time),
                )
            ).label("difference"),
        )
        .where(Customers.event_type == "purchase")
        .group_by(Customers.user_id, cte.columns.latest_day)
        .order_by(Customers.user_id, "difference")
    )
    print(statement)

    response = session.execute(statement)
    customers_features = list(response)
    customers_features_df = pd.DataFrame(customers_features)

    scaler = StandardScaler()

    data_scaled = preprocess_data(
        customers_features_df, scaler, ["difference", "purchase_count"]
    )

    plt.style.use("seaborn-v0_8")
    elbow_method(data_scaled, 10)

    kmeans = KMeans(n_clusters=3, random_state=42)
    customers_features_df["Cluster"] = kmeans.fit_predict(data_scaled)
    centroids = scaler.inverse_transform(kmeans.cluster_centers_)
    colors = ["grey", "green", "cyan"]
    cluster_labels = {0: "inactive", 1: "new customers", 2: "loyal_customers"}
    plot_clusters(customers_features_df, centroids, cluster_labels, colors)

    plot_cluster_distribution(customers_features_df, cluster_labels, colors)
    cluster_counts = customers_features_df["Cluster"].value_counts()
    loyal_customers_idx = cluster_counts.idxmin()

    loyal_customers_cluster = customers_features_df[
        customers_features_df["Cluster"] == loyal_customers_idx
    ]

    data_scaled = preprocess_data(
        loyal_customers_cluster, scaler, ["difference", "purchase_count"]
    )

    elbow_method(data_scaled, 10)

    kmeans = KMeans(n_clusters=3, random_state=42)
    loyal_customers_cluster.loc[:, "Cluster"] = kmeans.fit_predict(data_scaled)
    centroids = scaler.inverse_transform(kmeans.cluster_centers_)
    colors = ["silver", "gold", "whitesmoke"]
    cluster_labels = {0: "silver", 1: "gold", 2: "platinum"}
    plot_clusters(loyal_customers_cluster, centroids, cluster_labels, colors)

    plot_cluster_distribution(loyal_customers_cluster, cluster_labels, colors)
