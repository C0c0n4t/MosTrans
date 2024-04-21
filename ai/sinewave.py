import numpy as np
import tensorflow as tf


class SinModel:
    def __init__(self):
        self.W = tf.Variable(tf.random.uniform((4,),))

    def predict(self, x):
        return (self.W[0] * np.sin(self.W[1] * x + self.W[2]) + self.W[3])

    def __call__(self, x_set):
        return [self.predict(x) for x in x_set]

    def fit(self, x_train, y_train, epoch=1, learning_rate=0.01):
        assert len(x_train) == len(y_train)
        for _ in range(epoch):
            for x, y in zip(x_train, y_train):
                with tf.GradientTape() as tape:
                    y_c = self.predict(x)
                    loss = abs(y - y_c)
                grad = tape.gradient(loss, self.W)
                self.W.assign_sub(learning_rate * grad)

    def error(self, x_test, y_test):
        assert len(x_test) == len(y_test)
        loss = 0
        for x, y in zip(x_test, y_test):
            loss += abs(y - self.predict(x)) / y
        return (loss / len(x_test)).numpy() / len(y_test)

    @property
    def weights(self):
        return self.W
