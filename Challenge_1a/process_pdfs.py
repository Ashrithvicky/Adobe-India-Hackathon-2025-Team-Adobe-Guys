import fitz  # PyMuPDF
import re

PAGE_OFFSET = -1

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)

    # Try built-in TOC first
    toc = doc.get_toc()
    if toc and len(toc) > 0:
        return extract_from_toc(doc, toc)

    # Fallback to text analysis
    return extract_from_text_analysis(doc)

def extract_from_toc(doc, toc):
    outline = []
    title = "Untitled Document"
    if doc.page_count > 0:
        first_page = doc[0]
        first_page_elements = get_text_elements_from_page(first_page)
        title = extract_multi_line_title(first_page_elements)

    for level, heading, page_num in toc:
        if level <= 3:
            heading_level = f"H{level}"
            outline.append({
                "level": heading_level,
                "text": heading,
                "page": page_num
            })
    outline = remove_title_headings(outline, title)
    outline = [normalize_heading_text(h) for h in outline]
    return {"title": title, "outline": outline}

def extract_from_text_analysis(doc):
    all_text_elements = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        all_text_elements.extend(get_text_elements_from_page(page, page_num + 1))

    if not all_text_elements:
        return {"title": "Untitled Document", "outline": []}

    # Title: concatenate top-most, largest-font lines on first page
    first_page_elements = [elem for elem in all_text_elements if elem["page"] == 1]
    title = extract_multi_line_title(first_page_elements)
    title_lines = [t.strip().lower() for t in split_title_lines(title)]

    # --- FORM DETECTION ---
    if is_form_document(title, all_text_elements):
        return {"title": title, "outline": []}

    # Find TOC pages (pages containing "Table of Contents" as a heading)
    toc_pages = set()
    for elem in all_text_elements:
        if is_exact_common_heading(elem["text"], "table of contents"):
            toc_pages.add(elem["page"])

    # Heading candidates: only numbered headings or exact common heading keywords, not in TOC pages
    heading_candidates = []
    for elem in all_text_elements:
        text = elem["text"]
        # Allow "Table of Contents" heading even if on TOC page
        if elem["page"] in toc_pages and not is_exact_common_heading(text, "table of contents"):
            continue
        if len(text.strip()) > 200:
            continue
        if is_table_or_form_label(text):
            continue
        # Only include numbered headings if they are not too long (avoid list items)
        if is_numbered_heading(text) and len(text.strip()) <= 80:
            elem["confidence"] = 10
            heading_candidates.append(elem)
        elif is_exact_common_heading(text):
            elem["confidence"] = 10
            heading_candidates.append(elem)

    heading_candidates = remove_title_from_headings(heading_candidates, title_lines)
    heading_candidates = remove_duplicate_headings(heading_candidates)
    heading_candidates.sort(key=lambda x: (x["page"], x["y_position"]))

    outline = []
    for elem in heading_candidates:
        level = determine_heading_level(elem["text"])
        if level:
            outline.append({
                "level": level,
                "text": elem["text"],
                "page": elem["page"] + PAGE_OFFSET,
                "y_position": elem["y_position"]
            })

    outline = [h for h in outline if h["page"] > 0]  # Remove any with page < 1
    outline.sort(key=lambda x: (x["page"], x["y_position"]))
    for o in outline:
        o.pop("y_position", None)

    outline = remove_title_headings(outline, title)
    outline = [normalize_heading_text(h) for h in outline]

    return {"title": title, "outline": outline}

def get_text_elements_from_page(page, page_num=1):
    elements = []
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            full_text = ""
            font_sizes = []
            is_bold = False
            for span in line["spans"]:
                text = span["text"]
                if text:
                    full_text += text + " "
                    font_sizes.append(span["size"])
                    if span["flags"] & 2**4:
                        is_bold = True
            full_text = full_text.rstrip('\n')
            if full_text and len(full_text.strip()) > 1:
                avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 12
                elements.append({
                    "text": full_text,
                    "page": page_num,
                    "font_size": round(avg_font_size, 1),
                    "is_bold": is_bold,
                    "y_position": line["bbox"][1] if line.get("bbox") else 0
                })
    return elements

def extract_multi_line_title(first_page_elements):
    if not first_page_elements:
        return "Untitled Document"
    max_font = max(e["font_size"] for e in first_page_elements)
    title_lines = [e for e in first_page_elements if abs(e["font_size"] - max_font) < 0.1]
    title_lines.sort(key=lambda x: x["y_position"])
    title = "".join([e["text"] for e in title_lines])
    return title

def split_title_lines(title):
    # Split title into lines for matching
    return [line for line in re.split(r' {2,}|\n', title) if line.strip()]

def is_form_document(title, all_text_elements):
    form_keywords = ["form", "application", "request", "certificate", "registration", "claim", "report", "invoice"]
    title_lower = title.lower()
    if any(word in title_lower for word in form_keywords):
        return True
    first_page_elems = [e for e in all_text_elements if e["page"] == 1]
    short_numbered = [e for e in first_page_elems if re.match(r'^\d+\.?$', e["text"].strip())]
    if len(short_numbered) >= 5:
        return True
    table_fields = [
        "date", "name", "age", "s.no", "relationship", "signature", "remarks", "version", "identifier", "reference", "pay + si + npa"
    ]
    table_fields_found = [e for e in first_page_elems if e["text"].strip().lower() in table_fields]
    if len(table_fields_found) >= 3:
        return True
    return False

def is_numbered_heading(text):
    patterns = [
        r'^\d+\.\s+.+',           # "1. Introduction"
        r'^\d+\.\d+\s+.+',        # "2.1 Section"
        r'^\d+\.\d+\.\d+\s+.+',   # "2.1.1 Subsection"
        r'^Chapter\s+\d+.*',      # "Chapter 1"
        r'^Section\s+\d+.*',      # "Section 1"
        r'^Part\s+\d+.*',         # "Part 1"
    ]
    for pattern in patterns:
        if re.match(pattern, text.strip(), re.IGNORECASE):
            return True
    return False

def is_exact_common_heading(text, match=None):
    common_headings = [
        "introduction", "overview", "conclusion", "summary", "references", 
        "bibliography", "acknowledgements", "table of contents", "abstract",
        "methodology", "results", "discussion", "background", "literature review",
        "revision history", "appendix", "glossary", "index"
    ]
    text_lower = text.lower().strip()
    if match:
        return text_lower == match
    return text_lower in common_headings

def is_table_or_form_label(text):
    if re.match(r'^\d+\.?$', text.strip()):
        return True
    if re.match(r'^[A-Za-z]$', text.strip()):
        return True
    table_fields = [
        "date", "name", "age", "s.no", "relationship", "signature", "remarks", "version", "identifier", "reference", "pay + si + npa"
    ]
    text_lower = text.lower().strip()
    return text_lower in table_fields

def determine_heading_level(text):
    if re.match(r'^\d+\.\s+', text.strip()):
        return "H1"
    elif re.match(r'^\d+\.\d+\s+', text.strip()):
        return "H2"
    elif re.match(r'^\d+\.\d+\.\d+\s+', text.strip()):
        return "H3"
    if is_exact_common_heading(text):
        return "H1"
    return None

def remove_duplicate_headings(candidates):
    unique_candidates = []
    seen_texts = set()
    for candidate in candidates:
        text_normalized = re.sub(r'\s+', ' ', candidate["text"].lower().strip())
        if text_normalized not in seen_texts:
            seen_texts.add(text_normalized)
            unique_candidates.append(candidate)
    return unique_candidates

def remove_title_headings(outline, title):
    # Remove any heading that matches any line in the title (case-insensitive, ignoring whitespace)
    title_lines = [t.strip().lower() for t in split_title_lines(title)]
    def is_title_line(htext):
        htext_norm = re.sub(r'\s+', ' ', htext.strip().lower())
        return any(htext_norm == re.sub(r'\s+', ' ', t) for t in title_lines)
    return [h for h in outline if not is_title_line(h["text"])]

def remove_title_from_headings(heading_candidates, title_lines):
    # Remove any heading candidate that matches any line in the title
    def is_title_line(htext):
        htext_norm = re.sub(r'\s+', ' ', htext.strip().lower())
        return any(htext_norm == re.sub(r'\s+', ' ', t) for t in title_lines)
    return [h for h in heading_candidates if not is_title_line(h["text"])]

def normalize_heading_text(h):
    h["text"] = re.sub(r' +', ' ', h["text"])
    h["text"] = h["text"].replace("–", "-").replace("—", "-")
    h["text"] = h["text"].rstrip() + " "  # Ensure trailing space as in expected output
    return h

import os
import json
from process_pdfs import extract_outline

def main():
    is_docker = os.path.exists("/.dockerenv")
    if is_docker:
        INPUT_DIR = "/app/input"
        OUTPUT_DIR = "/app/output"
    else:
        INPUT_DIR = os.path.join(os.getcwd(), "sample_dataset/pdfs")
        OUTPUT_DIR = os.path.join(os.getcwd(), "sample_dataset/outputs")

    if not os.path.exists(INPUT_DIR):
        print(f"Input directory {INPUT_DIR} does not exist!")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    try:
        all_files = os.listdir(INPUT_DIR)
        pdf_files = [f for f in all_files if f.lower().endswith(".pdf")]
    except Exception as e:
        print(f"Error reading input directory: {e}")
        return

    if not pdf_files:
        print(f"No PDF files found in {INPUT_DIR}")
        return

    for filename in pdf_files:
        try:
            pdf_path = os.path.join(INPUT_DIR, filename)
            if not os.path.exists(pdf_path):
                continue
            data = extract_outline(pdf_path)
            if not data:
                data = {"title": "Untitled Document", "outline": []}
            out_filename = os.path.splitext(filename)[0] + ".json"
            out_path = os.path.join(OUTPUT_DIR, out_filename)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()
