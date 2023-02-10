from csc583.document import Document

class InvertedIndex:

    def __init__(self,input_file):
        # add your code here
        pass

    def read_txt_file(self,input_file):
        #add your code here
        docs=None
        return docs

    def q7_1_1(self, query):
        # add your code here
        #return multiple outputs that have the same docid if and
        # when there are multiple matches per doc.
        ans=[]
        ans1 = Document("Doc1",3,1)
        ans2 = Document("Doc2",1,2)
        ans.append(ans1)
        ans.append(ans2)
        return ans

    def q7_1_2(self, query):
        # add your code here
        ans = []
        ans1 = Document("Doc1", 3, 1)
        ans2 = Document("Doc2", 1, 2)
        ans3 = Document("Doc3", 5, 1)
        ans.append(ans1)
        ans.append(ans2)
        ans.append(ans3)
        return ans


    def q7_2(self, query):
        # add your code here
        ans = []
        ans1 = Document("Doc2", 1, 2)
        ans.append(ans1)
        return ans

def main():
    # adding a main just in case you want to run not from pytest
    query="schizophrenia /2 drug"
    ans=InvertedIndex().q7_1_1(query)


if __name__ == "__main__":
    main()