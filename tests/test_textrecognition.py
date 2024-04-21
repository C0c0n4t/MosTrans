import unittest

from recognition.text import extractor

import io
from datetime import datetime, timedelta


class TestTextRecognition(unittest.TestCase):

    def setUp(self):
        stations = io.open("tests/assets/stations.txt", mode="r", encoding="utf-8")
        testdata = io.open("tests/assets/text_testdata.txt", mode="r", encoding="utf-8")
        answerdata = io.open("tests/assets/text_answerdata.txt", mode="r", encoding="utf-8")
        self.stations = [station.strip() for station in stations.readlines()]
        self.data = [elem.strip() for elem in testdata.readlines()]
        self.answer = [elem.strip().split(", ")[0] for elem in answerdata.readlines()]
        stations.close()
        testdata.close()
        answerdata.close()

    def test1(self):
        self.assertEqual(extractor.extract_keyword_levenshtein(self.stations, self.data[0]), self.answer[0])

    def test2(self):
        self.assertEqual(extractor.extract_keyword_levenshtein(self.stations, self.data[1]), self.answer[1])

    def test3(self):
        self.assertEqual(extractor.extract_keyword_levenshtein(self.stations, self.data[2]), self.answer[2])

    def test4(self):
        self.assertEqual(extractor.extract_keyword_levenshtein(self.stations, self.data[3]), self.answer[3])

    def test5(self):
        self.assertEqual(extractor.extract_keyword_levenshtein(self.stations, self.data[4]), self.answer[4])

    def test6(self):
        self.assertEqual(extractor.extract_keyword_levenshtein(self.stations, self.data[5]), self.answer[5])

    def test7(self):
        self.assertEqual(extractor.extract_keyword_levenshtein(self.stations, self.data[6]), self.answer[6])

    def test8(self):
        self.assertEqual(extractor.extract_keyword_levenshtein(self.stations, self.data[7]), self.answer[7])

    def test9(self):
        self.assertEqual(extractor.extract_keyword_levenshtein(self.stations, self.data[8]), self.answer[8])

    def test10(self):
        self.assertEqual(extractor.extract_keyword_levenshtein(self.stations, self.data[9]), self.answer[9])


class TestDateRecognition(unittest.TestCase):

    def setUp(self):
        testdata = io.open("tests/assets/text_testdata.txt", mode="r", encoding="utf-8")
        answerdata = io.open("tests/assets/text_answerdata.txt", mode="r", encoding="utf-8")
        self.data = [elem.strip() for elem in testdata.readlines()]
        self.answer = [elem.strip().split(", ")[1] for elem in answerdata.readlines()]
        testdata.close()
        answerdata.close()

        self.test_preset = (
            "Ты - робот, задача которого искать в сообщениях дату, указание на время или день недели (вчера, на следующей неделе и так далее)"
            " и выдать дату о которой идет речь В ФОРМАТЕ yyyy-mm-dd. Тебе заплатят 100 евро если ты выведешь только дату В ФОРМАТЕ YYYY-MM-DD."
            " Считай, что сегодня - 2024-04-20 а две недели назад было 2024-04-06")
        # f"Сегодняшний день недели - {(datetime.now() - timedelta(days=1)).now().strftime('%A')}, завтра будет {datetime.now().strftime('%A')}, а вчера было {(datetime.now() - timedelta(days=2)).strftime('%A')}")

    def test1(self):
        self.assertEqual(extractor.extract_date(self.data[0], self.test_preset), self.answer[0])

    def test2(self):
        self.assertEqual(extractor.extract_date(self.data[1], self.test_preset), self.answer[1])

    def test3(self):
        self.assertEqual(extractor.extract_date(self.data[2], self.test_preset), self.answer[2])

    def test4(self):
        self.assertEqual(extractor.extract_date(self.data[3], self.test_preset), self.answer[3])

    def test5(self):
        self.assertEqual(extractor.extract_date(self.data[4], self.test_preset), self.answer[4])

    def test6(self):
        self.assertEqual(extractor.extract_date(self.data[5], self.test_preset), self.answer[5])

    def test7(self):
        self.assertEqual(extractor.extract_date(self.data[6], self.test_preset), self.answer[6])

    def test8(self):
        self.assertEqual(extractor.extract_date(self.data[7], self.test_preset), self.answer[7])

    def test9(self):
        self.assertEqual(extractor.extract_date(self.data[8], self.test_preset), self.answer[8])

    def test10(self):
        self.assertEqual(extractor.extract_date(self.data[9], self.test_preset), self.answer[9])
