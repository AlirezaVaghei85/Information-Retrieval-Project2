# 🔍 Information Retrieval System - Project #2
> Advanced Inverted Index Optimization, Text Preprocessing Pipelines & Memory Analysis on Reuters-21578 Corpus

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NLTK](https://img.shields.io/badge/NLTK-3.8%2B-green.svg?style=for-the-badge&logo=nltk)](https://www.nltk.org/)
[![Memory Profiling](https://img.shields.io/badge/Profiling-Pympler-orange.svg?style=for-the-badge)](https://pypi.org/project/Pympler/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg?style=for-the-badge)](LICENSE)

---

## 📑 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Index Architecture](#-index-architecture)
- [Preprocessing Pipelines Compared](#-preprocessing-pipelines-compared)
- [Performance & Optimization Insights](#-performance--optimization-insights)
- [Getting Started](#-getting-started)
- [Interactive Menu Usage](#-interactive-menu-usage)
- [Repository Structure](#-repository-structure)
- [Author & Acknowledgments](#-author--acknowledgments)

---

## 📌 Overview

This project is an advanced **Information Retrieval (IR)** engine implemented in Python. It builds a Binary Search Tree (BST) based **Inverted Index** over the **Reuters-21578** benchmark dataset ($10,788$ documents).

The core focus of this second project is **Preprocessing Pipeline Evaluation**, **Dictionary Compression / Lossy Pruning**, and **Exact Memory Profiling** comparing various text normalization strategies on index size and query retrieval.

---

## ✨ Key Features

- **🌲 BST Inverted Index Structure:** Efficient tree-based storage for terms, mapping each term to its sorted Posting List (`DocIDs`).
- **🔤 Comprehensive Preprocessing Pipelines:**
  1. **No Preprocessing:** Raw tokenized text indexing.
  2. **Case Folding:** Uniform lowercasing.
  3. **Stopword Removal:** Top-20 and Top-50 stopword filtering.
  4. **Stemming:** Porter Stemmer algorithm.
  5. **Lemmatization:** WordNet Lemmatizer.
- **✂️ Lossy Pruning & Index Compression:**
  - **Single-Frequency Pruning:** Removes noise terms appearing in fewer than 2 documents.
  - **Top-20K Vocabulary Truncation:** Keeps top 20,000 high-frequency terms and reconstructs a **Balanced Binary Search Tree** using a mid-point split algorithm.
- **📊 Precise Memory Measurement:** Uses `pympler.asizeof` to independently profile:
  - Total Index Size
  - Vocabulary Size
  - Postings List Size
- **🔎 Boolean Search Engine:**
  - Single-term retrieval.
  - Two-term conjunctive (`AND`) boolean retrieval using linear pointer merge on sorted posting lists.
- **💾 Persistence:** Fast serialization and deserialization of binary trees using Python's `pickle`.

---

## 🧠 Index Architecture & Data Structures

```text
                 [ Node: "market" ]
                /                  \
   [ Node: "bank" ]              [ Node: "oil" ]
      DocIDs: [1, 5, 12]            DocIDs: [3, 5, 9, 22]

```

Each tree node contains:

* `term`: Unique string identifier.
* `DocID`: Sorted list of document IDs where the term occurs.
* `left` & `right`: Pointers to BST child nodes.

---

## ⚡ Preprocessing Pipelines Compared

| Strategy | Description | Target Compression Impact |
| --- | --- | --- |
| **No Preprocess** | Baseline raw tokens from Reuters dataset. | 0% (Baseline) |
| **LowerCase** | Converts all tokens to lower-case. | Vocabulary reduction |
| **Stopword Removal 20** | Filters out top 20 frequent English words. | Postings list reduction |
| **Stopword Removal 50** | Filters out top 50 frequent English words. | Significant postings reduction |
| **Porter Stemming** | Reduces words to their morphological roots. | Vocabulary & Postings consolidation |
| **Lemmatization** | Contextual dictionary-based word reduction. | High precision vocabulary reduction |
| **Lossy Pruning** | Drops all terms with `doc_freq < 2`. | Removes long-tail noise terms |
| **Keep 20k Terms** | Filters top 20k terms & builds balanced BST. | Strict vocabulary ceiling & speedup |

---

## 📈 Performance & Optimization Insights

* **Recall vs. Precision Trade-off:** Applying `Stemming` and `Lemmatization` groups morphological variations of words (e.g., *market, markets, marketing* $\rightarrow$ *market*). This significantly increases the number of retrieved documents (**Recall**) but may introduce some noise, slightly lowering exact-match **Precision**.
* **Memory Footprint Reduction:** Stopword removal (especially Top-50) and `Lossy Pruning` drastically shrink the total footprint of the Posting Lists by eliminating low-value, high-frequency connectors and ultra-rare typos.
* **Search Complexity:** By extracting the Top-20K terms and rebuilding the index via a `build_balanced()` function, the index avoids BST worst-case skewed tree scenarios ($O(N)$), guaranteeing $O(\log N)$ average query time.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.10+ installed along with the required packages:

```bash
pip install nltk pympler psutil

```

### Dataset Preparation

The system uses the NLTK `reuters` dataset. You can initialize and serialize the raw data by running the setup script (or uncommenting the initialization block):

```python
import nltk
nltk.download('reuters')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

```

### Running the Engine

Execute the main script to load the serialized indexes and enter the interactive search mode:

```bash
python main.py

```

---

## 💻 Interactive Menu Usage

Upon execution, the terminal displays the current index memory usage statistics and prompts for search operations across all preprocessed models:

```text
======================================
Index Memory Profiling
======================================
Size Of Index: 14.52 MB
Size Of Vocabs: 2.18 MB
Size Of Posting: 12.34 MB

1. Search for one query
2. Search for two queries with AND
3. See 30 most frequent terms
Choose an option: 

```

### Example Output (Option 2: Boolean AND Search)

```text
Enter your query: oil AND market

No Preprocess:
Query: oil AND market
Documents retrieved: 412
Doc IDs: ['10005', '10011', '10022', ...]

With Lower Case:
Query: oil AND market
Documents retrieved: 450
Doc IDs: ['10005', '10011', '10015', ...]

With Stemming:
Query: oil AND market
Documents retrieved: 512
Doc IDs: ['10001', '10005', ...]

```

### Boolean AND Algorithm (`Intersect`)

Conjunctive query processing uses a linear two-pointer algorithm on sorted posting lists, bounded by $O(N + M)$ time complexity:

```text
List 1 (oil):    [ 3 -> 5 -> 9  -> 22 ]
                       ^
List 2 (market): [ 1 -> 5 -> 12 -> 22 ]
                       ^
Result:          [ 5, 22 ]

```

---

## 📁 Repository Structure

```text
.
├── main.py                   # Main project script (Tree, Preprocessing, Query Engine)
├── data.pkl                  # Serialized Reuters corpus tokens
├── No_PreProcess.pkl         # Serialized raw BST index
├── LowerCase.pkl             # Serialized lowercased index
├── stopword_removal_20.pkl   # Serialized top-20 stopword-removed index
├── stopword_removal_50.pkl   # Serialized top-50 stopword-removed index
├── Stemming.pkl              # Serialized stemmed index
├── Lemmatizing.pkl           # Serialized lemmatized index
├── Lossy_pruning.pkl         # Serialized pruned index (doc_freq >= 2)
├── Keep_20k_terms.pkl        # Serialized balanced 20k-term index
└── README.md                 # Project documentation

```

---

## 👤 Author & Acknowledgments

* **Author:** Alireza Vaghei
* Developed as part of the **Information Retrieval** coursework at **Birjand University**.
* Special thanks to NLTK maintainers for providing the Reuters dataset.

```

```
