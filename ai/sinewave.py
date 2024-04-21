import numpy as np
import sqlite3
import tensorflow as tf


def date_to_num(date):
    nums = [int(x) for x in date.split('-')]
    return (nums[0]*365 + nums[1]*30 + nums[2])


def grad(a, omega, x, phi, b):
    '''Gradient of function y = a*sin(omega*x + phi) + b'''
    return (np.sin(omega*x + phi), a*x*np.cos(omega*x + phi),
            a*np.cos(omega*x + phi), 1)


con = sqlite3.connect('../data/databases/train_database.sqlite')
cursor = con.cursor()
xs, ys = [], []
for i in range(322):
    cursor.execute(f'''SELECT ymd, count FROM passengerflow WHERE
                   station_id = {i} ORDER BY ymd''')
    station_data = cursor.fetchall()
    xs += [[date_to_num(x[0]) for x in station_data]]
    ys += [[x[1] / 50000 for x in station_data]]


class SinModel:
    def __init__(self):
        self.W = tf.Variable(tf.random.uniform((4,),))

    def calc(self, x):
        return (self.W[0] * np.sin(self.W[1] * x + self.W[2]) + self.W[3])

    def __call__(self, x_set):
        return [self.calc(x) for x in x_set]

    def fit(self, x_train, y_train, epoch=1, learning_rate=0.01):
        assert len(x_train) == len(y_train)
        for _ in range(epoch):
            for x, y in zip(x_train, y_train):
                with tf.GradientTape() as tape:
                    y_c = self.calc(x)
                    loss = abs(y - y_c)
                grad = tape.gradient(loss, self.W)
                self.W.assign_sub(learning_rate * grad)

    def score(self, x_test, y_test):
        assert len(x_test) == len(y_test)
        loss = 0
        for x, y in zip(x_test, y_test):
            loss += abs(y - self.calc(x))
        return loss / len(x_test)

    @property
    def weights(self):
        return self.W


model0 = SinModel()
model0.fit(xs[0], ys[0], epoch=30)
print(model0.score(xs[0][80:], ys[0][80:]))
print()
print(model0(xs[0][90:]))
print(ys[0][90:])
print(model0.weights)
