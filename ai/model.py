from Levenshtein import distance
from natasha import DatesExtractor, MorphVocab
import sqlite3

connection = sqlite3.connect('../data/databases/train_database.sqlite')
cursor = connection.cursor()
stations = [''.join(x).split('(')[0].lower() for x in cursor.execute('SELECT NAME FROM STATION').fetchall()]
def extract_station(text):
    text = text.lower().split()
    min_distance = float("inf")
    min_distance_station = None
    for station in stations:
        tmp = ''.join(station.split())
        for i in range(len(text) - len(station.split()) + 1):
            w = ''.join(text[i:i + len(station.split())])
            cur_distance = distance(w, tmp)
            if cur_distance < min_distance:
                min_distance = cur_distance
                min_distance_station = station
        
    return min_distance_station

if __name__ == "__main__":
    text = 'Вчера я провел целый день, исследуя красоту мозаик на станции майяковская.'
    print(extract_station(text))
