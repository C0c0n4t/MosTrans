import unittest

from recognition.text import extractor


class TestTextRecognition(unittest.TestCase):

    def setUp(self):
        import io
        self.stations = [station.strip() for station in io.open("tests/assets/stations.txt", mode="r", encoding="utf-8").readlines()]
        self.data = [elem.strip() for elem in io.open("tests/assets/text_testdata.txt", mode="r", encoding="utf-8").readlines()]
        self.answer = [elem.strip().split(", ")[0] for elem in io.open("tests/assets/text_answerdata.txt", mode="r", encoding="utf-8").readlines()]

    def test1(self):
        self.assertEqual(extractor.extract_keyword(self.stations, self.data[0]), self.answer[0])

    def test2(self):
        self.assertEqual(extractor.extract_keyword(self.stations, self.data[1]), self.answer[1])

    def test3(self):
        self.assertEqual(extractor.extract_keyword(self.stations, self.data[2]), self.answer[2])

    def test4(self):
        self.assertEqual(extractor.extract_keyword(self.stations, self.data[3]), self.answer[3])

    def test5(self):
        self.assertEqual(extractor.extract_keyword(self.stations, self.data[4]), self.answer[4])

    def test6(self):
        self.assertEqual(extractor.extract_keyword(self.stations, self.data[5]), self.answer[5])

    def test7(self):
        self.assertEqual(extractor.extract_keyword(self.stations, self.data[6]), self.answer[6])

    def test8(self):
        self.assertEqual(extractor.extract_keyword(self.stations, self.data[7]), self.answer[7])

    def test9(self):
        self.assertEqual(extractor.extract_keyword(self.stations, self.data[8]), self.answer[8])

    def test10(self):
        self.assertEqual(extractor.extract_keyword(self.stations, self.data[9]), self.answer[9])


class TestDateRecognition(unittest.TestCase):

    def setUp(self):
        import io
        self.data = [elem.strip() for elem in
                     io.open("tests/assets/text_testdata.txt", mode="r", encoding="utf-8").readlines()]
        self.answer = [elem.strip().split(", ")[1] for elem in
                       io.open("tests/assets/text_answerdata.txt", mode="r", encoding="utf-8").readlines()]

    def test1(self):
        self.assertEqual(extractor.extract_date(self.data[0]), self.answer[0])

    def test2(self):
        self.assertEqual(extractor.extract_date(self.data[1]), self.answer[1])

    def test3(self):
        self.assertEqual(extractor.extract_date(self.data[2]), self.answer[2])

    def test4(self):
        self.assertEqual(extractor.extract_date(self.data[3]), self.answer[3])

    def test5(self):
        self.assertEqual(extractor.extract_date(self.data[4]), self.answer[4])

    def test6(self):
        self.assertEqual(extractor.extract_date(self.data[5]), self.answer[5])

    def test7(self):
        self.assertEqual(extractor.extract_date(self.data[6]), self.answer[6])

    def test8(self):
        self.assertEqual(extractor.extract_date(self.data[7]), self.answer[7])

    def test9(self):
        self.assertEqual(extractor.extract_date(self.data[8]), self.answer[8])

    def test10(self):
        self.assertEqual(extractor.extract_date(self.data[9]), self.answer[9])
