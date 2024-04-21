import sqlite3
from sinewave import SinModel
import numpy as np
import tensorflow as tf


def date_to_num(date):
    nums = [int(x) for x in date.split('-')]
    return (nums[0]*365 + nums[1]*30 + nums[2])


EPOCH = 1
MAX_PASSENGER_NUM = 50000

con = sqlite3.connect('../data/databases/train_database.sqlite')
cursor = con.cursor()
xs, ys = [], []
for i in cursor.execute("SELECT id FROM station").fetchall():
    cursor.execute(f'''SELECT ymd, count FROM passengerflow WHERE
                   station_id = {i[0]} ORDER BY ymd''')
    station_data = cursor.fetchall()
    if station_data == []:
        xs += [[0]*len(xs[0])]
        ys += [[0]*len(ys[0])]
    xs += [[date_to_num(x[0]) for x in station_data]]
    ys += [[x[1] / MAX_PASSENGER_NUM for x in station_data]]
xs = np.array(xs)
ys = np.array(ys)


class Model:
    def __init__(self, num):
        self.sinmodels = []
        for _ in range(num):
            self.sinmodels += [SinModel()]

    def fit(self, x_train, y_train, epoch=1, learning_rate=0.01, make_file=False):
        if make_file:
            f = open('model_weights.txt', "w")
        for i in range(len(self.sinmodels)):
            self.sinmodels[i].fit(x_train[i], y_train[i], epoch, learning_rate)
            if make_file:
                f.write(str(self.sinmodels[i].weights.numpy()) + "\n")
        if make_file:
            f.close()

    def read_weight(self, file):
        for s in self.sinmodels:
            weights = [float(w) for w in list(file.readline()[1:-2].split())]
            weights = np.array(weights)
            s.W = tf.Variable(weights)

    def predict(self, station_id, date):
        x = date_to_num(date)
        return self.sinmodels[station_id].predict(x)

    def error_list(self, x_test, y_test):
        el = []
        for i in range(len(self.sinmodels)):
            el += [self.sinmodels[i].error(x_test[i], y_test[i])]
        return el


if __name__ == "__main__":
    model = Model(32)
    #model.fit(xs[:][:80], ys[:][:80], EPOCH, make_file=True)
    file = open("model_weights.txt", "r")
    model.read_weight(file)
    print(model.error_list(xs[:][80:], ys[:][80:]))
