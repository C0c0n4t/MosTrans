from tensorflow import keras
from tensorflow.keras import layers
import sqlite3
import numpy as np

INPUT_SIZE = 7
OUTPUT_SIZE = 1
MAX_NUM = 50000
TEST_SIZE = 10


con = sqlite3.connect('../data/databases/train_database.sqlite')
cursor = con.cursor()
train_images = []
train_labels = []
test_images = []
test_labels = []
for i in range(322):
    cursor.execute(f'''SELECT ymd, count FROM passengerflow WHERE
                   station_id = {i} ORDER BY ymd''')
    station_data = [x[1] for x in cursor.fetchall()]
    if station_data == []:
        continue
    for i in range(len(station_data) - INPUT_SIZE - TEST_SIZE):
        train_images += [station_data[i:i + INPUT_SIZE]]
        train_labels += [station_data[i + INPUT_SIZE]]

    for i in range(len(station_data) - INPUT_SIZE - TEST_SIZE, len(station_data) - INPUT_SIZE):
        test_images += [station_data[i:i + INPUT_SIZE]]
        test_labels += [station_data[i + INPUT_SIZE]]

train_images = np.array(train_images)
train_labels = np.array(train_labels)
train_images = train_images.astype('float32') / MAX_NUM
train_labels = train_labels.astype('float32') / MAX_NUM

test_images = np.array(test_images)
test_labels = np.array(test_labels)
test_images = test_images.astype('float32') / MAX_NUM
test_labels = test_labels.astype('float32') / MAX_NUM

model = keras.Sequential([
    layers.Dense(INPUT_SIZE, activation="relu"),
    layers.Dense(10*INPUT_SIZE, activation="softmax"),
    layers.Dense(OUTPUT_SIZE, activation="sigmoid")
    ])

model.compile(optimizer="rmsprop",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.fit(train_images, train_labels, epochs=5, batch_size=16)

test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"test_acc: {test_acc}")

prediction = model.predict(test_images[:10])
print(prediction)
print(test_labels[:10])





