import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from models import Customers
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, func

user = "alorain"
password = "mysecretpassword"
host = "127.0.0.1"
port = "5432"
database = "piscineds"

url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(url)
with Session(engine) as session:
    statement = (
        select(
            func.date_trunc("day", Customers.event_time), func.count(Customers.user_id)
        )
        .where(Customers.event_type == "purchase")
        .group_by(func.date_trunc("day", Customers.event_time))
    )
    response = session.execute(statement)
    user_purchase_by_time = list(response)
    days, nb_users = zip(*user_purchase_by_time)
    fig, ax = plt.subplots()
    plt.style.use("seaborn-v0_8")
    ax.plot(days, nb_users)
    ax.set_ylabel("Number of customers")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    plt.show()

    statement = (
        select(
            func.date_trunc("month", Customers.event_time), func.sum(Customers.price)
        )
        .where(Customers.event_type == "purchase")
        .group_by(func.date_trunc("month", Customers.event_time))
    )
    response = session.execute(statement)
    sales_per_month = list(response)
    months, sales = zip(*sales_per_month)
    months = [month.strftime("%b") for month in months]
    fig, ax = plt.subplots()
    ticks_y = ticker.FuncFormatter(lambda x, _: x / 1000000)
    ax.yaxis.set_major_formatter(ticks_y)

    ax.set_ylabel("Total sales in million of ₳")
    ax.bar(months, sales)
    plt.show()

    sales_per_user_cte = (
        select(
            func.date_trunc("day", Customers.event_time).label("day"),
            func.sum(Customers.price).label("sales"),
            Customers.user_id,
        )
        .where(Customers.event_type == "purchase")
        .group_by("day", Customers.user_id, Customers.user_session)
        .order_by("day")
    )
    sales_per_user_cte = sales_per_user_cte.cte("sales_per_user")
    statement = select(
        sales_per_user_cte.columns.day, func.avg(sales_per_user_cte.columns.sales)
    ).group_by(sales_per_user_cte.columns.day)

    response = session.execute(statement)
    average_spend_per_customers = list(response)

    days, avg_sales = zip(*average_spend_per_customers)
    fig, ax = plt.subplots()

    ax.fill_between(days, avg_sales)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_ylabel("average spend/customers in ₳")
    plt.show()
