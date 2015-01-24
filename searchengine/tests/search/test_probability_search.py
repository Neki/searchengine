from unittest import TestCase
from searchengine.search.probability_search import binary_independance_retrieval
from searchengine.parser.cacm_document import CacmDocument
from searchengine.index.index import Index


class TestProbabilitySearch(TestCase):

    def test_binary_independance_retrieval(self):
        request = "tata"
        document1 = CacmDocument(1, "aujourd \n toto \n" ,"il fait \n tyty", "toto \n tyty")
        document2 = CacmDocument(2, "plouf \n paf", "tata \n toto il tata", "tyty plouf \n tata paf")
        document_list = [document1, document2]
        common_words = ["aujourd", "il", "fait", "ca", "mot", "ok"]
        index = Index(common_words, document_list)
        search_result = binary_independance_retrieval(request, index,  2)
        self.assertEqual(2, search_result[0][0])

