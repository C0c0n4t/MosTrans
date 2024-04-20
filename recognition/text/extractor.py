from Levenshtein import distance
from natasha import DatesExtractor, MorphVocab
import sqlite3
# from deep_translator import GoogleTranslator

connection = sqlite3.connect('data/databases/train_database.sqlite')
cursor = connection.cursor()
stations = [''.join(x).split(' (')[0].lower() for x in cursor.execute('SELECT NAME FROM STATION').fetchall()]
def extract_keyword(keywords, text):
    text = ''.join(text.split()).lower()
    min_distance = float("inf")
    min_distance_keyword = None
    for keyword in keywords:
        tmp = ''.join(keyword.split())
        for i in range(len(text) - len(tmp) + 1):
            w = ''.join(text[i:i + len(tmp)])
            cur_distance = distance(w, tmp)
            if cur_distance < min_distance:
                min_distance = cur_distance
                min_distance_keyword = keyword
        
    return min_distance_keyword

morph_vocab = MorphVocab()
dates_extractor = DatesExtractor(morph_vocab)
def extract_date(text):
    date = list(dates_extractor(text))
    if date == []:
        return (None, None, None)
    fact = date[0].__getattribute__("fact")
    return (fact.__getattribute__("day"), fact.__getattribute__("month"), fact.__getattribute__("year"))


if __name__ == "__main__":
    text = '21 апреля Площадь революции'
    print(extract_keyword(stations, text))
    print(extract_date(text))
    # print(stations)
