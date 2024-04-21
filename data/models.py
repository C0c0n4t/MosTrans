from data.db_session import databases

# train_database.sqlite
train_database = None

Line = None
Station = None
PassengerFlow = None


def load_models():
    """Loads all models from databases"""
    global train_database, Line, Station, PassengerFlow

    # train_database.sqlite
    train_database = databases["train_database"].classes

    Line = train_database.line
    Station = train_database.station
    PassengerFlow = train_database.passengerflow
