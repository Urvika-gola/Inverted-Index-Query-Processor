## About
The InvertedIndex Python class constructs an inverted index from a text file and supports Boolean queries with AND and OR operations. This project was developed for CSC 583 under Instructor Mihai Surdeanu. This project demonstrates efficient text search capabilities on a document corpus.

## Functionalities
Inverted Index Creation: Parses documents to create an inverted index for fast text search. Boolean Query Processing: Supports complex Boolean queries with AND and OR operations, along with handling operator precedence. Error Handling: Recognizes and informs users of invalid or empty queries/documents.

## Testing
q5_1(query: str) -> list: Executes a simple AND query.
q5_2(query: str) -> list: Executes a simple OR query.
q5_3(query: str) -> list: Executes a complex query with both AND and OR, where AND takes precedence.
