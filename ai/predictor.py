import sqlite3
from sinewave import SinModel


def date_to_num(date):
    nums = [int(x) for x in date.split('-')]
    return (nums[0]*365 + nums[1]*30 + nums[2])


EPOCH = 10
MAX_PASSENGER_NUM = 50000

con = sqlite3.connect('../data/databases/train_database.sqlite')
cursor = con.cursor()
xs, ys = [], []
for i in range(322):
    cursor.execute(f'''SELECT ymd, count FROM passengerflow WHERE
                   station_id = {i} ORDER BY ymd''')
    station_data = cursor.fetchall()
    xs += [[date_to_num(x[0]) for x in station_data]]
    ys += [[x[1] / MAX_PASSENGER_NUM for x in station_data]]


class Model:
    def __init__(self, num):
        self.sinmodels = []
        for _ in range(num):
            self.sinmodels += [SinModel()]

    def fit(self, x_train, y_train, epoch=1, learning_rate=0.01):
        for i in range(len(self.sinmodels)):
            self.sinmodels[i].fit(x_train[i], y_train[i], epoch, learning_rate)

    def predict(self, station_id, date):
        x = date_to_num(date)
        return self.sinmodels[station_id].predict(x)
