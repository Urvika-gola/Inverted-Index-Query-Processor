# Positional Inverted Index

## Overview
This project implements a **Positional Inverted Index** in Python, enabling efficient document retrieval based on term proximity. The `InvertedIndex` class indexes a document corpus and provides search functionality for queries with two terms separated by a specified distance (`k`). The index supports **bidirectional** and **unidirectional** positional proximity search algorithms.

Developed for **CSC 583** under **Instructor Mihai Surdeanu**.

## Features

- **Positional Indexing**: Stores term positions for efficient proximity-based retrieval.
- **Bidirectional and Unidirectional Search**:
  - **Bidirectional Search**: Finds terms within a distance `k` of each other in either direction.
  - **Unidirectional Search**: Finds terms within a distance `k` with the first term preceding the second.
- **Configurable Proximity Queries**: Handles queries in the format `term1 /k term2` to specify the maximum distance between terms.

## Public Methods
read_txt_file(input_file: str) -> list: Reads the document file line by line, returning non-empty lines.
- q7_1_1(query: str) -> list: Executes a bidirectional proximity query.
- q7_1_2(query: str) -> list: Executes a second bidirectional proximity query.
- q7_2(query: str) -> list: Executes a unidirectional proximity query.
