import unittest
from unittest import TestCase
from searchengine.parser.cacm_document import _read_document_id, _get_next_cacm_document
from searchengine.parser import load_from_cacm_file, load_from_cacm
from io import StringIO


class TestProcess(TestCase):

    def test_read_doc_id(self):
        text = StringIO(".I 42\n.T\ntata\n")
        self.assertEqual(42, _read_document_id(text))

    def test_read_doc(self):
        text = StringIO(".I 25\n.W\ntiti\n.T\ntata\n.K\ntoto\n.B\nsome date\n")
        doc = None
        _, doc = _get_next_cacm_document(text)
        self.assertEqual(25, doc.doc_id)
        self.assertEqual("tata\n", doc.title)
        self.assertEqual("toto\n", doc.keywords)
        self.assertEqual("titi\n", doc.abstract)

    def test_read_several_docs(self):
        text = StringIO(".I 25\n.T\ntata\n.K\ntoto\n.B some date here\n.I 28\n.T\nyoyo\n")
        docs = list(load_from_cacm(text))
        self.assertEqual(2, len(docs))
        self.assertEqual("yoyo\n", docs[1].title)

    @unittest.skip("Skipping this test until the resource file is distributed")
    def test_load_from_file(self):
        docs = load_from_cacm_file("./resources/cacm.all")
        self.assertEqual(3204, (len(list(docs))))

    def test_get_full_text(self):
        text = StringIO(".I 22\n.T\ntoto\n.K\ntata\n.W\nhi\n")
        doc = list(load_from_cacm(text))[0]
        self.assertEqual(doc.get_full_text(), "toto\n\nhi\n\ntata\n\n")
