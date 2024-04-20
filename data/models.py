from data.db_session import databases


# main_database.sqlite
main_database = None

# train_database.sqlite
train_database = None

Line = None
Station = None
PassengerFlow = None


def load_models():
    """Loads all models from databases"""
    global main_database, train_database, Line, Station, PassengerFlow

    # main_database.sqlite
    main_database = databases["main_database"].classes

    # train_database.sqlite
    train_database = databases["train_database"].classes

    Line = train_database.line
    Station = train_database.station
    PassengerFlow = train_database.passengerflow
