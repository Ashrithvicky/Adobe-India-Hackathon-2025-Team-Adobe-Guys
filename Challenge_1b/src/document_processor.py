import PyPDF2
import re
import os
from typing import Dict, List, Tuple

class DocumentProcessor:
    def __init__(self):
        self.documents = {}
        
    def extract_text_from_pdf(self, pdf_path: str) -> Dict[int, str]:
        page_texts = {}
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        text = page.extract_text()
                        if text.strip():
                            page_texts[page_num] = text
                    except Exception as e:
                        continue
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
        return page_texts
    
    def clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\-.,;:!?()]', '', text)
        return text.strip()
    
    def extract_sections(self, text: str) -> List[Dict]:
        sections = []
        paragraphs = text.split('\n\n')
        
        for i, paragraph in enumerate(paragraphs):
            paragraph = self.clean_text(paragraph)
            if len(paragraph) > 50:
                if re.match(r'^[A-Z][A-Za-z\s\-:]+$', paragraph.split('\n')[0]):
                    title = paragraph.split('\n')[0][:100]
                else:
                    words = paragraph.split()[:10]
                    title = ' '.join(words) + "..."
                
                sections.append({
                    'title': title,
                    'content': paragraph,
                    'word_count': len(paragraph.split()),
                    'section_index': i
                })
        
        return sections
    
    def process_documents(self, document_paths: List[str]) -> Dict:
        processed_docs = {}
        
        for doc_path in document_paths:
            if not os.path.exists(doc_path):
                continue
                
            filename = os.path.basename(doc_path)
            page_texts = self.extract_text_from_pdf(doc_path)
            
            doc_sections = {}
            for page_num, text in page_texts.items():
                sections = self.extract_sections(text)
                doc_sections[page_num] = sections
            
            processed_docs[filename] = {
                'page_texts': page_texts,
                'sections': doc_sections,
                'total_pages': len(page_texts)
            }
        
        return processed_docs