# Persona-Driven Document Intelligence

A sophisticated document analysis system that extracts and prioritizes content from PDF collections based on user personas and specific job requirements.

## Features

- **Multi-Document Processing**: Handles 3-5 PDF documents simultaneously
- **Persona-Based Analysis**: Tailors content extraction to specific user roles
- **Intelligent Ranking**: Prioritizes sections based on relevance to persona and task
- **Structured Output**: Generates standardized JSON with metadata and analysis
- **CPU Optimized**: Runs efficiently without GPU requirements
- **Fast Processing**: Completes analysis within 60 seconds

## Installation

### Using Docker (Recommended)

```bash
docker build -t challenge1b .
docker run -v "${PWD}:/app" challenge1b python /app/src/main.py "/app/Challenge_1b/Collection 1"
```

### Manual Installation

```bash
pip install -r requirements.txt
python src\main.py "Challenge_1b\Collection 1"
```

## Usage

### Input Structure
Place your collections in the following structure:
```
Collection X/
├── PDFs/
│   ├── document1.pdf
│   ├── document2.pdf
│   └── document3.pdf
├── challenge1b_input.json
└── challenge1b_output.json (generated)
```

### Running the System

```bash
# Process a specific collection
python src\main.py "Challenge_1b\Collection 1"

# With Docker
docker run -v "${PWD}:/app" challenge1b python /app/src/main.py "/app/Challenge_1b/Collection 1"
```

### Input Configuration

The `challenge1b_input.json` file should contain:

```json
{
    "challenge_info": {
        "challenge_id": "round_1b_XXX",
        "test_case_name": "specific_test_case"
    },
    "documents": [
        {
            "filename": "document.pdf",
            "title": "Document Title"
        }
    ],
    "persona": {
        "role": "Travel Planner"
    },
    "job_to_be_done": {
        "task": "Plan a 4-day trip for 10 college friends"
    }
}
```

## Supported Personas

- **Travel Planner**: Focuses on destinations, activities, accommodations
- **HR Professional**: Emphasizes forms, processes, compliance
- **Food Contractor**: Prioritizes recipes, ingredients, menu planning
- **Researcher**: Targets methodology, analysis, academic content
- **Student**: Focuses on learning materials and educational content

## Output Format

The system generates a `challenge1b_output.json` file with:

```json
{
    "metadata": {
        "input_documents": ["list of processed files"],
        "persona": "User Persona",
        "job_to_be_done": "Task description",
        "processing_timestamp": "ISO timestamp"
    },
    "extracted_sections": [
        {
            "document": "source.pdf",
            "section_title": "Section Title",
            "importance_rank": 1,
            "page_number": 1
        }
    ],
    "subsection_analysis": [
        {
            "document": "source.pdf",
            "refined_text": "Extracted content...",
            "page_number": 1
        }
    ]
}
```

## Performance

- **Processing Time**: ≤60 seconds for 3-5 documents
- **Memory Usage**: Optimized for CPU-only execution
- **Model Size**: ≤1GB total footprint
- **Compatibility**: Works on standard CPU hardware

## Architecture

The system consists of four main components:

1. **Document Processor**: PDF text extraction and structuring
2. **Persona Analyzer**: Relevance scoring and section ranking
3. **Section Extractor**: Content refinement and formatting
4. **Main Controller**: Orchestration and output generation

## Requirements

- Python 3.9+
- CPU-only processing
- No internet access during execution
- Standard memory constraints

## License

This project is developed for the Adobe India Hackathon 2025.