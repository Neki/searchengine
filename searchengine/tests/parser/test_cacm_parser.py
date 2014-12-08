from unittest import TestCase
from searchengine.parser.document import _read_document_id, _build_cacm_documents, _build_cacm_document, ReachedEndOfFile
from io import StringIO


class TestProcess(TestCase):

    def test_read_doc_id(self):
        text = StringIO(".I 42\n.T\ntata\n")
        self.assertEqual(42, _read_document_id(text))

    def test_read_doc(self):
        text = StringIO(".I 25\n.T\ntata\n.K\ntoto\n")
        doc = None
        try:
            doc = _build_cacm_document(text)
        except ReachedEndOfFile:
            pass
        self.assertEqual(25, doc.doc_id)
        self.assertEqual("tata\n", doc.title)
        self.assertEqual("toto\n", doc.keywords)

    def test_read_several_docs(self):
        text = StringIO(".I 25\n.T\ntata\n.K\ntoto\n.I 28\n.T\nyoyo\n")
        docs = _build_cacm_documents(text)
        self.assertEqual(2, len(docs))
        self.assertEqual("yoyo\n", docs[1].title)
