# Round 1A: Understand Your Document

## Challenge Theme
**Connecting the Dots Through Docs**

## Objective
Develop a PDF outline extractor that parses PDF files and outputs a structured JSON containing:
- Document title
- Headings: H1, H2, H3 with their corresponding page numbers

---

## Input and Output Format

### Input
PDF files placed in the `/app/input` directory.

### Output
For each input PDF, a corresponding `.json` file is created in the `/app/output` directory, structured as:

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

---

## How to Build and Run

### Build the Docker Image
```bash
docker build --platform linux/amd64 -t challenge1a:solution .
```

### Run the Docker Container
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none challenge1a:solution
```

---

## Approach

1. **PDF Parsing**:
   - Uses `PyMuPDF` (`fitz`) to extract text blocks, font sizes, and positioning.

2. **Title Extraction**:
   - Extracts the largest font-sized, topmost multi-line text from the first page.

3. **TOC and Heuristics**:
   - If internal Table of Contents (TOC) exists, headings are extracted directly.
   - If not, uses rule-based and heuristic logic to determine headings from text patterns and positions.

4. **Heading Detection**:
   - Matches numbered headings (e.g., `1.`, `2.1`, `3.1.2`) and common section names (`Introduction`, `Summary`, etc.).
   - Filters out irrelevant elements like table labels and form components.

5. **Heading Level Classification**:
   - Based on regex patterns:
     - `1.` → H1
     - `1.1` → H2
     - `1.1.1` → H3

6. **Post-Processing**:
   - Removes duplicate headings.
   - Filters out headings that match title lines.
   - Normalizes heading text for consistency.

---

## Folder Structure

```
Challenge_1a/
├── sample_dataset/
│   ├── outputs/         # JSON files provided as outputs.
│   ├── pdfs/            # Input PDF files
│   └── schema/          # Output schema definition
│       └── output_schema.json
├── Dockerfile           # Docker container configuration
├── process_pdfs.py      # Sample processing script
└── README.md           # This file
```

---

## Constraints

| Constraint       | Requirement                   |
|------------------|-------------------------------|
| Execution Time   | ≤ 10 seconds for 50-page PDF |
| Internet Access  | Not allowed                   |
| Model Size       | ≤ 200MB (if ML model used)    |
| Architecture     | Compatible with amd64 (x86_64)|
| GPU Usage        | Not allowed (CPU only)        |

---

## Dependencies

- Python 3.x
- `PyMuPDF` (fitz)
- `re`, `os`, `json` (standard libraries)

---

