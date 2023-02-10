from unittest import TestCase
from csc583.invertedindex import InvertedIndex
from csc583.document import Document

class Test_hw2_q7(TestCase):
    input_path= "Docs.txt"

    def test_q7_1_1(self):
        query = "schizophrenia /2 drug"
        gold_q711=[Document("Doc1",3,1),Document("Doc2",1,2)]
        ans_q711=InvertedIndex(self.input_path).q7_1_1(query)

        assert type(ans_q711) is not None
        assert type(ans_q711) is list
        assert len(ans_q711) > 0
        assert len(ans_q711) == 2

        for gold,ans in zip(gold_q711,ans_q711):
            gold.__eq__(ans)


    def test_q7_1_2(self):
        query = "schizophrenia /4 drug"
        gold_q712 = [Document("Doc1", 3, 1), Document("Doc2", 1, 2), Document("Doc3", 5, 1)]
        ans_q712 = InvertedIndex(self.input_path).q7_1_2(query)
        assert ans_q712 is not None
        assert type(ans_q712) is list
        assert len(ans_q712) > 0
        assert len(ans_q712) == 3

        for gold, ans in zip(gold_q712, ans_q712):
            gold.__eq__(ans)


    def test_q7_2_directional(self):
        query = "schizophrenia /2 drug"
        gold_q72 = [Document("Doc2", 1, 2)]
        ans_q72 = InvertedIndex(self.input_path).q7_2(query)

        assert ans_q72 is not None
        assert type(ans_q72) is list
        assert len(ans_q72) > 0
        assert len(ans_q72) == 1

        for gold, ans in zip(gold_q72, ans_q72):
            gold.__eq__(ans)


