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

morph_vocab = MorphVocab()
dates_extractor = DatesExtractor(morph_vocab)
def extract_date(text):
    date = list(dates_extractor(text))
    fact = date[0].__getattribute__("fact")
    return (fact.__getattribute__("day"), fact.__getattribute__("month"), fact.__getattribute__("year"))


if __name__ == "__main__":
    text = '21 апреля я провел целый день, исследуя красоту мозаик на станции майяковская.'
    print(extract_station(text))
    print(extract_date(text))
