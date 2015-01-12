from unittest import TestCase
from searchengine.evaluation.evaluation import *
from searchengine.search.vectorial_search import vectorial_search
from searchengine.parser import CacmDocument
from searchengine.index.process import Weighting

class TestEvaluation(TestCase):

    def test_number_of_relevant_documents(self):
        request = Request(1, "tata", [1,2])
        document1 = CacmDocument(1, "aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        document2 = CacmDocument(2,"plouf \n paf","tata \n toto il tata","tyty plouf \n tata paf")
        document_list = [document1, document2]
        common_words=["aujourd","il","fait","ca","mot","ok"]
        search_result = vectorial_search(request.text, document_list, common_words, 2,Weighting.TermFrequency)
        self.assertEqual(2,number_of_relevant_documents(request, search_result))

    def test_precision(self):
        request = Request(1,"tata",[1,2])
        document1 = CacmDocument(1, "aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        document2 = CacmDocument(2,"plouf \n paf","tata \n toto il tata","tyty plouf \n tata paf")
        document_list = [document1, document2]
        common_words=["aujourd","il","fait","ca","mot","ok"]
        search_results = vectorial_search(request.text, document_list, common_words, 2,Weighting.TermFrequency)
        self.assertEqual(1,precision(request, search_results))
        
    def test_rappel(self):
        request = Request(1,"tata",[1,2])
        document1 = CacmDocument(1, "aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        document2 = CacmDocument(2,"plouf \n paf","tata \n toto il tata","tyty plouf \n tata paf")
        document_list = [document1, document2]
        common_words=["aujourd","il","fait","ca","mot","ok"]
        search_results = vectorial_search(request.text, document_list, common_words, 2,Weighting.TermFrequency)
        self.assertEqual(1,rappel(request, search_results))
        
    @unittest.skip("Skipping until Travis CI is properly configured (this test blocks otherwise)")
    def test_plot_precision_rappel(self):
        request = Request(1,"tata",[1,2])
        document1 = CacmDocument(1, "aujourd \n toto \n tata","il fait \n tyty","toto \n tata tyty")
        document2 = CacmDocument(2,"plouf \n paf","tata \n toto il tata","tyty plouf \n tata paf")
        document_list = [document1, document2]
        common_words=["aujourd","il","fait","ca","mot","ok"]
        search_results = vectorial_search(request.text, document_list, common_words, 2,Weighting.TermFrequency)
        plot_precision_rappel(request, search_results)