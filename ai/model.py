from autocorrect import Speller
from Levenshtein import distance
from natasha import DatesExtractor, MorphVocab


stations = ['маяковская', 'каширская', 'нагатинский затон']

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
    text = 'Вчера я провел целый день, исследуя красоту мозаик на станции майяковская.'
    print(extract(text))
