# Adobe Guys - Connecting the Dots Challenge

Welcome to our submission for the **“Connecting the Dots” Hackathon Challenge** organized by Adobe.  
We are **Team Adobe Guys** and this repository includes complete solutions for **Round 1A** and **Round 1B**.

---

## 🧑‍🤝‍🧑 Team Members

- **Vigneshwar SI**
- **Mohana Krishnan G**
- **Iniya Vasanthan VM**

---

## 🚀 Challenge Overview

### 🌟 Theme: Connecting the Dots Through Docs

Our mission was to rethink how PDFs are read and understood — transforming static documents into intelligent, context-aware reading companions.

---

## ✅ Round 1A - Understand Your Document

### 🔧 Objective

Build an offline solution that takes in a PDF and outputs a structured outline containing:

- **Title**
- **Headings**: H1, H2, H3
- **Output Format**: JSON

### 📁 Output Format
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

### 📦 Features

- Built using Python and PyMuPDF
- Compatible with AMD64 Docker architecture
- Fully offline, no external API calls
- Handles different font sizes, positions, and heuristics
- Optimized for PDFs up to 50 pages within 10s



## 🔍 Round 1B - Persona-Driven Document Intelligence

### 🎯 Objective

Build a persona-aware analyzer that ranks sections and subsections relevant to the given **persona** and **job-to-be-done**, from a collection of documents.

### 📋 Features

- Extracted key sections and ranked their importance
- Subsection analysis based on refined text summaries
- Outputs structured JSON for relevance insights
- Handles domain diversity (research, education, finance)
- Fully modular pipeline

### 💾 Output Includes

- Input Metadata
- Relevant Sections (Document, Page, Title, Rank)
- Sub-section Analysis (Page, Refined Text)

### ⚙️ Constraints Met

- CPU-only (amd64)
- Execution ≤ 60 seconds (for 3-5 documents)
- Offline-ready
- Model size ≤ 1 GB

---


## 🤝 Acknowledgements

Thanks to Adobe for this amazing opportunity. This challenge helped us apply document intelligence in real-world problem-solving.

---

## 🔒 Note

Please keep this repository **private** until the official announcement to make it public.

---
