import unittest

from recognition.text import model


class TestTextRecognition(unittest.TestCase):

    def setUp(self):
        import io
        self.data = io.open("tests/assets/text_testdata.txt", mode="r", encoding="utf-8").readlines()
        self.answer = io.open("tests/assets/text_answerdata.txt", mode="r", encoding="utf-8").readlines()
        print(self.data, self.answer)

    def test1(self):
        self.assertEqual(model.extract_station(self.data[0].strip()), self.answer[0].strip().split(", ")[0])

    def test2(self):
        self.assertEqual(model.extract_station(self.data[1].strip()), self.answer[1].strip().split(", ")[0])

    def test3(self):
        self.assertEqual(model.extract_station(self.data[2].strip()), self.answer[2].strip().split(", ")[0])

    def test4(self):
        self.assertEqual(model.extract_station(self.data[3].strip()), self.answer[3].strip().split(", ")[0])

    def test5(self):
        self.assertEqual(model.extract_station(self.data[4].strip()), self.answer[4].strip().split(", ")[0])

    def test6(self):
        self.assertEqual(model.extract_station(self.data[5].strip()), self.answer[5].strip().split(", ")[0])

    def test7(self):
        self.assertEqual(model.extract_station(self.data[6].strip()), self.answer[6].strip().split(", ")[0])

    def test8(self):
        self.assertEqual(model.extract_station(self.data[7].strip()), self.answer[7].strip().split(", ")[0])