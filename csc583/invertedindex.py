from csc583.document import Document

class InvertedIndex:
    """
    Class InvertedIndex takes in a text file containing the DocID and words as input to create an positional index
    It contains methods to calculate the query containing 2 terms and distance k between them.
    Public Methods: read_txt_file, q7_1_1, q7_1_2, q7_2
    Private Methods: _parse_query, _create_positional_index, _get_doc_id_from_line, _positional_intersect_bidirectional,
    _positional_intersect_unidirectional.
    Author: Urvika Gola
    Course: CSC 583, Instructor - Mihai Surdeanu, TA - Shreya Nupur Shakya
    """

    def __init__(self, input_file):
        """
        The constructor for InvertedIndex class
        :param doc: the document file containing documents
        """
        self.doc = input_file

    def read_txt_file(self, input_file: str) -> list:
        """
        Read the text file line by line; and stores every line in a string array
        :param input_file: Docs.txt
        :return: a string array of non-empty lines
        """
        with open(input_file) as f:
            lines = [line.strip() for line in f.readlines() if len(line.strip()) != 0]
        if len(lines) == 0:
            assert False, "The document is empty, returning False."
        return lines

    def _parse_query(self, query: str, is_bidirectional: bool) -> list[Document]:
        """
        This method does 3 things in order to parse the query
        1. Reads the text file
        2. Creates a positional index based on the reading it performed in Step 1.
        3. Breaks down the query into terms and value of K and sends to the bidirectional or unidirectional positional
        intersect algorithm
        :param query: the input query in the form "schizophrenia /2 drug"
        :param is_bidirectional: if set to True, it will use bidirectional algorithm otherwise unidirectional algorithm.
        :return: the result in the format expected in the assignment
        """
        lines = self.read_txt_file(self.doc)  # read the text file and create an array of lines
        inverted_index = self._create_positional_index(lines)  # create a positional index that looks like
        # {'breakthrough': [[1, [0]]], 'drug': [[1, [1]], [2, [2]], [3, [1]]], 'for': [[1, [2]], [3, [2]], [4, [2]]],
        #  'schizophrenia': [[1, [3]], [2, [1]], [3, [5]], [4, [3]]], 'new': [[2, [0]], [3, [0]], [4, [0]]],
        #  'treatment': [[3, [3]]], 'of': [[3, [4]]], 'hopes': [[4, [1]]], 'patients': [[4, [4]]]}
        split_query = query.split()
        position_list_of_term_one = inverted_index[split_query[0]]  # fetch the first term of the query
        position_list_of_term_two = inverted_index[split_query[2]]  # fetch the second term of the query
        k = int(split_query[1].replace("/", ""))  # fetch the value of k
        if is_bidirectional:
            answer = self._positional_intersect_bidirectional(position_list_of_term_one, position_list_of_term_two, k)
        else:
            answer = self._positional_intersect_unidirectional(position_list_of_term_one, position_list_of_term_two, k)
        return self._parse_answer(answer)

    def _create_positional_index(self, lines: list) -> dict:
        """
        Create the positional index that stores the DocIDs and corresponding positional values of the terms
        :param lines: the lines of the Docs.txt as a String Array
        :return: a dictionary containing the positional index with key as the word and value as [DocID, [pos1, pos2..]]
        """
        doc_id_with_line = {}  # creates a dict as shown below
        # {1: 'Doc1    breakthrough drug for schizophrenia', 2: 'Doc2    new approach for treatment of schizophrenia',
        # 3: 'Doc3    new hopes for schizophrenia patients', 4: 'Doc4    new schizophrenia drug'}
        positional_index = {}

        for line in lines:
            doc_id = self._get_doc_id_from_line(line)  # the key is the Doc ID
            if doc_id:
                # ignore the lines from which we were unable to parse DocID e.g. "Doc    breakthrough for schizophrenia"
                doc_id_with_line[doc_id] = line

        for doc_id, line in doc_id_with_line.items():
            words = line.split()[1:]  # skip the first word as it must be the Doc identifier like 'Doc1'
            idx = 0
            for word in words:
                if word not in positional_index:
                    positional_index[word] = [[doc_id, [idx]]]
                    idx += 1
                elif word in positional_index:
                    # If the word (term) is already present in the dictionary, add the DocID if it's not present
                    # if the DocID is present too, we will skip it as we don't want duplicates.
                    get_doc_ids = []  # stores the DocIDs in a separate list for checking the above logic.
                    values = positional_index[word]
                    for doc_id_and_positions in values:
                        get_doc_ids.append(doc_id_and_positions[0])

                    if doc_id not in get_doc_ids:
                        positional_index[word].append([doc_id, [idx]])  # add the docID and the index to the term's value
                    else:
                        # if docID is already present, update the existing positional list corresponding to that docID
                        # by appending this position to it.
                        existing_value = positional_index[word]
                        for doc_id_and_positions in existing_value:
                            if doc_id_and_positions[0] == doc_id:
                                existing_position_list = doc_id_and_positions[1]
                                existing_position_list.append(idx)
                    idx += 1
        # sort the dict based on DocIDs using the below sorted method and a lambda function
        # note that the positional list is already sorted as we iterate over words using indices in ascending order.
        for key in positional_index:
            some_list = positional_index[key]
            sorted_list = sorted(some_list, key=lambda x: x[0])
            positional_index[key] = sorted_list
        return positional_index

    def _get_doc_id_from_line(self, line: str) -> int:
        """
        Get the number and index of this last digit so that after that the content of the line starts
        :param line: the line containing the docID and words e.g. "Doc40    new schizophrenia drug"
        :return: the integer part of the DocID eg, returns int 40 for "Doc40    new schizophrenia drug"
        """
        num = []  # stores separate digits of the number
        for char in line:
            if char.isdigit():
                # as long as we encounter digit, append it. This is mostly to handle more than just single digit DocIDs
                num.append(char)
            elif char == " ":
                # if we encounter a space, that means the number is terminated, join the digits and return it
                return int(''.join(num)) if (len(num) > 0) else False
        return int(''.join(num)) if (len(num) > 0) else False  # return false if no numeric digit was found in the line

    def _positional_intersect_bidirectional(self, p1: list, p2: list, k: int) -> list:
        """
        An algorithm for proximity intersection of positing list p1 and p2
        The algorithm finds places where the two terms within k words of each other, in either direction.
        :param p1: positional list p1 in the form [[1, [0]], [2, [0, 1]] i.e. [DocID, [pos1, pos2, ..]]
        :param p2: positional list p2 in the form [[1, [0]], [2, [0, 1]] i.e. [DocID, [pos1, pos2, ..]]
        :param k: the distance k
        :return: list of triples giving docID and the term position in p1 and p2
        """
        result = []
        i, j = 0, 0  # to access indices i and j of list1 and list2 respectively
        while i < len(p1) and j < len(p2):
            if p1[i][0] == p2[j][0]:  # if the docIDs match
                l = []  # l stores the candidate solutions
                pos1, pos2 = 0, 0
                while pos1 < len(p1[i][1]):  # for every position in p1, we will look at position in p2
                    while pos2 < len(p2[j][1]):
                        if abs(p2[j][1][pos2] - p1[i][1][pos1]) <= k:   # if the distance between them is k
                            l.append(p2[j][1][pos2])                    # then add it to candidate list
                        elif p2[j][1][pos2] > p1[i][1][pos1]:           # if the position in p2 is greater, then
                            break                                       # stop looking forward in p2
                        pos2 += 1                                       # otherwise, keep looking forward in p2
                    while len(l) != 0 and abs(l[0] - p1[i][1][pos1]) > k:
                        l.pop(0)                                        # cleaning the candidate list
                    for ps in l:
                        result.append([p1[i][0], p1[i][1][pos1], ps])
                    pos1 += 1
                i += 1
                j += 1
            elif p1[i][0] < p2[j][0]:  # if docIDs don't match and docID of p1 is smaller
                i += 1                 # increment pointer from list with smaller docID i.e. p1
            else:
                j += 1  # otherwise, increment pointer from larger docID i.e. p2
        return result

    def _parse_answer(self, answer: list):
        """
        Parses the list from the algorithm and returns in the form as expected in the assignment.
        1. It basically appends "Doc" in front of all the numeric Doc IDs
        2. Sorts the String with Doc + number in lexicographical order
        :param answer: list of triples giving docID and the term position in p1 and p2 e.g. [3, 2, 3]
        :return: list of Document("Doc2", 1, 2) ....
        """
        ans = []
        for _answer in answer:
            final_ans = Document("Doc" + str(_answer[0]), _answer[1], _answer[2])
            ans.append(final_ans)
        # sort the final list of documents in lexicographical order as asked in the assignment.
        return sorted(ans, key=lambda k: k.doc_id)

    def _positional_intersect_unidirectional(self, p1: list, p2: list, k: int) -> list:
        """
        An algorithm for proximity intersection of positing list p1 and p2
        The algorithm finds places where the two terms within k words of each other, in forward direction
        i.e. the word1 appears before word2
        :param p1: positional list p1 in the form [[1, [0]], [2, [0, 1]] i.e. [DocID, [pos1, pos2, ..]]
        :param p2: positional list p2 in the form [[1, [0]], [2, [0, 1]] i.e. [DocID, [pos1, pos2, ..]]
        :param k: the distance k
        :return: list of triples giving docID and the term position in p1 and p2 e.g. [3,2,3]
        """
        result = []
        i, j = 0, 0  # to access indices i and j of list1 and list2 respectively
        while i < len(p1) and j < len(p2):
            if p1[i][0] == p2[j][0]:  # if the docIDs match
                pos1 = 0
                pos2 = 0
                while pos1 < len(p1[i][1]):
                    while pos2 < len(p2[j][1]) and p2[j][1][pos2] < p1[i][1][pos1]:
                        # ensuring to not consider positions of p2 which are less than p1
                        pos2 += 1
                    while pos2 < len(p2[j][1]) and p2[j][1][pos2] - p1[i][1][pos1] <= k:
                        result.append([p1[i][0], p1[i][1][pos1], p2[j][1][pos2]])
                        pos2 += 1
                    pos1 += 1
                i += 1
                j += 1
            elif p1[i][0] < p2[j][0]:  # if docIDs don't match and docID of p1 is smaller
                i += 1                 # increment pointer from list with smaller docID i.e. p1
            else:
                j += 1
        return result

    def q7_1_1(self, query: str) -> list[Document]:
        """
        Method for Q8 Part 1.1
        Note: The positions begin from index 0 in my code.
        :param query: e.g. drug /2 schizophrenia
        :return: list of triples giving docID and the term position p1 and p2 of the two terms
        """
        return self._parse_query(query, True)

    def q7_1_2(self, query: str) -> list[Document]:
        """
        Method for Q8 Part 1.2
        Note: The positions begin from index 0 in my code.
        :param query: e.g. drug /2 schizophrenia
        :return: list of triples giving docID and the term position p1 and p2 of the two terms
        """
        return self._parse_query(query, True)

    def q7_2(self, query):
        """
        Method for Q8 Part 2
        Note: The positions begin from index 0 in my code.
        :param query: e.g. drug /2 schizophrenia
        :return: list of triples giving docID and the term position p1 and p2 of the two terms
        """
        return self._parse_query(query, False)

def main():
    # adding a main just in case you want to run not from pytest
    query="schizophrenia /2 drug"
    ans=InvertedIndex().q7_1_1(query)

if __name__ == "__main__":
    main()
