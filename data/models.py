from data.db_session import databases


# main_database.sqlite
main_database = databases["main_database"].classes

# train_database.sqlite
train_database = databases["train_database"].classes

Line = train_database.line
Station = train_database.station
PassengerFlow = train_database.passengerflow
