from typing import *

# database
db_files = [r"data\databases\main_database.sqlite", r"data\databases\train_database.sqlite"]


def db_init():
    """Initializes all databases"""
    from data import db_session
    db_session.global_init(db_files)

    from data.models import load_models
    load_models()


def parse_xlsx():
    """Parses xlsx file into `train_database`"""
    import pandas as pd

    from data.db_session import sessions
    from data.models import Line, Station, PassengerFlow

    dataframe = pd.read_excel(r"..\data\databases\dataset.xlsx")

    lines = set()
    counter = 0
    for data in dataframe.values:
        station_name, line_id, line_name = data[0], data[1], data[2].lower()

        if (line_id, line_name) not in lines:
            lines.add((line_id, line_name))
            line = Line(id=line_id, name=line_name)
            sessions["train_database"].add(line)

        station = Station(id=counter, name=station_name, line_id=line_id)
        counter += 1
        sessions["train_database"].add(station)
        for date, count in zip(list(dataframe.keys())[3:], data[3:]):
            passenger_flow = PassengerFlow(station_id=station.id, ymd=str(date)[:10], count=count)
            sessions["train_database"].add(passenger_flow)
    sessions["train_database"].commit()
