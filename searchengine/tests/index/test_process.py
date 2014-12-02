from unittest import TestCase
from searchengine.index.process import tokenize, normalize, remove_stop_words


class TestProcess(TestCase):

    def test_tokenize(self):
        self.assertEqual(["aujourd", "hui", "lundi", "il", "fait", "beau", "enfin", "presque"], tokenize("aujourd'hui (lundi) il fait beau - enfin, presque."))
        self.assertEqual([], tokenize(""))

    def test_normalize(self):
        self.assertEqual("abcdef", normalize("AbCdEf"))
        self.assertEqual("abcdef", normalize("abcdef"))

    def test_remove_stop_words(self):
        self.assertEqual(["toto", "tata", "tyty"], remove_stop_words(["toto",
            "tata", "titi", "tutu", "tyty"], ["titi", "tutu"]))
