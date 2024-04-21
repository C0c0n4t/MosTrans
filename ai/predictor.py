import sqlite3
from ai.sinewave import SinModel
import numpy as np
import tensorflow as tf


def date_to_num(date):
    nums = [int(x) for x in date.split('-')]
    return (nums[0]*365 + nums[1]*30 + nums[2])


EPOCH = 1
MAX_PASSENGER_NUM = 50000


con = sqlite3.connect('data/databases/train_database.sqlite')
cursor = con.cursor()
xs, ys = [], []
count = 0
indexes = [x[0] for x in cursor.execute("SELECT id FROM station").fetchall()]
STATION_NUM = len(indexes)
for i in indexes:
    cursor.execute(f'''SELECT ymd, count FROM passengerflow WHERE
                   station_id = {i} ORDER BY ymd''')
    station_data = cursor.fetchall()
    if station_data == []:
        xs += [[0]*len(xs[0])]
        ys += [[0]*len(ys[0])]
    xs += [[date_to_num(x[0]) for x in station_data]]
    ys += [[x[1] / MAX_PASSENGER_NUM for x in station_data]]
xs = dict(zip(indexes, xs))
ys = dict(zip(indexes, ys))
con.close()


class Model:
    def __init__(self, indexes):
        self.sinmodels = dict()
        for i in indexes:
            self.sinmodels[i] = SinModel()

    def fit(self, x_train, y_train, epoch=1, learning_rate=0.01, make_file=False):
        if make_file:
            f = open('model_weights.txt', "w")
        for i in self.sinmodels.keys():
            self.sinmodels[i].fit(x_train[i], y_train[i], epoch, learning_rate)
            if make_file:
                f.write(str(self.sinmodels[i].weights.numpy()) + "\n")
        if make_file:
            f.close()

    def read_weight(self, file):
        for s in self.sinmodels.values():
            weights = [float(w) for w in list(file.readline()[1:-2].split())]
            weights = np.array(weights)
            s.W = tf.Variable(weights)
        return self

    def predict(self, station_id, date):
        x = date_to_num(date)
        return int(self.sinmodels[station_id].predict(x) * MAX_PASSENGER_NUM)

    def error_list(self, x_test, y_test):
        el = []
        for i in self.sinmodels.keys():
            el += [self.sinmodels[i].error(x_test[i], y_test[i])]
        return el


if __name__ == "__main__":
    model = Model(indexes)
    model.fit(xs, ys, EPOCH, make_file=True)
#    file = open("model_weights.txt", "r")
#    model.read_weight(file)
    print(model.error_list(xs, ys))
