from unittest import TestCase
from searchengine.index.process import tokenize, normalize, remove_stop_words, statistics, get_word_list, document_statistics, inverted_index
from searchengine.parser import CacmDocument

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

    def test_statistics(self):
        self.assertEqual({"toto":3,"tata":2,"tyty":1},statistics(["toto", "tata", "tyty", "toto", "toto", "tata"]))

    def test_get_word_list(self):
        document = CacmDocument(2382,"aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        self.assertEqual(["aujourd", "toto", "tata","il", "fait", "tyty","toto","tata","tyty"],get_word_list(document))

    def test_document_statistics(self):
        document = CacmDocument(2382,"aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        common_words=["aujourd","il","fait","ca","mot","ok"]
        self.assertEqual({"toto":2,"tata":2,"tyty":2},document_statistics(document,common_words))

    def test_inverted_index(self):
        document1 = CacmDocument(1, "aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        document2 = CacmDocument(2,"plouf \n paf","tata \n toto il","tyty plouf \n paf")
        document_list = {document1.doc_id : document1, document2.doc_id : document2}
        common_words=["aujourd","il","fait","ca","mot","ok"]
        self.assertEqual({document1.doc_id : 2, document2.doc_id : 1}, inverted_index(document_list, common_words, "toto"))
