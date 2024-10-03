import matplotlib.pyplot as plt
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
    statement = select(Customers.event_type, func.count(Customers.event_type)).group_by(
        Customers.event_type
    )
    response = session.execute(statement)
    event_type_list = list(response)
    event_types, count = zip(*event_type_list)
    fig, ax = plt.subplots()
    ax.pie(count, labels=event_types, autopct="%1.1f%%")
    plt.show()
