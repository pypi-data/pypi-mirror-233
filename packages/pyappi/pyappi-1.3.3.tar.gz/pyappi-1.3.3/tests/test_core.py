import unittest
from pyappi.document import VolatileDocument, Document
from pyappi.document.exceptions import DocumentNotLocked


test_documents = [(VolatileDocument,"vdtest"), (Document,"dtest")]


class TestAppiCore(unittest.TestCase):
    def setUp(self):
        [doc(name).delete() for (doc,name) in test_documents]

    def _test_transaction_base(self,_doc_type, _doc_name):
        with _doc_type(_doc_name) as doc:

            doc.types = {}
            doc.types.int = 1
            doc.types.string = "string"
            doc.types.float = 63.437

            self.assertEqual(1,doc.types.int)
            self.assertEqual("string",doc.types.string)
            self.assertEqual(63.437,doc.types.float)


            doc.types.subobj = {}
            doc.types.subobj["test~pre"] = "after"
            doc.types.subobj["test~pre"] = "before-"

            self.assertEqual("before-after",doc.types.subobj["test~pre"])

        self.assertRaises(DocumentNotLocked, lambda: doc.types)
        self.assertRaises(DocumentNotLocked, lambda: setattr(doc.types,"int",2))
            

    def test_transaction(self):
        [self._test_transaction_base(doc,name) for (doc,name) in test_documents]



if __name__ == "__main__":
    unittest.main()
