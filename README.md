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
