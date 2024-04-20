from Levenshtein import distance
from natasha import DatesExtractor, MorphVocab
import sqlite3

connection = sqlite3.connect('../data/databases/train_database.sqlite')
cursor = connection.cursor()
stations = [''.join(x).split()[0].split('-')[0].lower() for x in cursor.execute('SELECT NAME FROM STATION').fetchall()]
def extract(text):
    text = text.lower()
    min_distance = float("inf")
    min_distance_station = None
    for station in stations:
        cur_distance = distance(text, station)
        if cur_distance < min_distance:
            min_distance = cur_distance
            min_distance_station = station
    return min_distance_station

if __name__ == "__main__":
    text = 'В прошлую пятницу я был поражен количеством людей, которые едут на работу через станцию библиотека имени ленина.'
    print(extract(text))
