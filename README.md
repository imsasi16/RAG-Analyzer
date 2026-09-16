# RAG Analyzer

A practical Retrieval-Augmented Generation (RAG) project for document-based question answering.

The project compares different retrieval approaches and shows how retrieved document context can be provided to an LLM to generate grounded answers with source page references.

## Project Overview

RAG (Retrieval-Augmented Generation) combines document retrieval with an LLM.

Instead of asking an LLM to answer only from its trained knowledge, this project:

1. Loads a PDF document.
2. Splits the document into smaller chunks.
3. Creates embeddings for the chunks.
4. Stores the embeddings in ChromaDB.
5. Retrieves relevant information using different retrieval methods.
6. Sends the retrieved context to an LLM.
7. Generates an answer based on the retrieved document.
8. Shows the source document and page numbers.
9. Evaluates the retrieval methods using multiple questions.

## Architecture

```text
                    PDF Document
                         |
                         v
                  Document Loader
                         |
                         v
                      Chunking
                         |
                         v
                     Embeddings
                         |
                         v
                    ChromaDB
                         |
              +----------+----------+
              |                     |
              v                     v
       Retrieval Methods       SQLite Database
              |
    +---------+---------+----------------+
    |         |         |        |       |
    v         v         v        v       v
   DB      Keyword   Metadata  Vector  Hybrid
    |         |         |        |       |
    +---------+---------+--------+-------+
                         |
                         v
                 Retrieved Context
                         |
                         v
                        LLM
                         |
                         v
                  Generated Answer
                         |
                         v
                 Source / Page
                    References
```

## Retrieval Methods

### 1. DB Baseline

A simple database-based baseline that retrieves stored document chunks.

### 2. Keyword Retrieval

Uses keyword matching to find chunks containing terms related to the question.

### 3. Metadata Retrieval

Uses document metadata such as filename and page information to retrieve content.

### 4. Vector Retrieval

Uses embeddings and semantic similarity to find content related to the meaning of the question.

### 5. Hybrid Retrieval

Combines keyword retrieval and vector retrieval to use both exact-term matching and semantic similarity.

## Technologies Used

* Python
* SQLite
* ChromaDB
* Sentence Transformers
* Groq API
* Large Language Model (LLM)
* PyPDF
* JSON
* Git & GitHub

## Project Structure

```text
RAG-Analyzer/
│
├── data/
│   └── raw/
│       └── NIST_CSF_2.0.pdf
│
├── database/
│   └── sqlite_db.py
│
├── evaluation/
│   ├── eval_dataset.json
│   ├── evaluate.py
│   ├── results.json
│   └── RESULTS
```
