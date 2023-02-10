class Document:
    def __init__(self,doc_id, position1, position2):
        self.doc_id=doc_id
        self.position1=position1
        self.position2=position2

    def __eq__(self, other):
        assert self.doc_id == other.doc_id
        assert self.position1== other.position1
        assert self.position2 == other.position2

