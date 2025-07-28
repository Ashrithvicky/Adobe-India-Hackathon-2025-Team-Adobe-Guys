import json
import os
import sys
from datetime import datetime
from typing import Dict, List

from document_processor import DocumentProcessor
from persona_analyzer import PersonaAnalyzer
from section_extractor import SectionExtractor

class PersonaDocumentIntelligence:
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.persona_analyzer = PersonaAnalyzer()
        self.section_extractor = SectionExtractor()
    
    def load_input_config(self, input_path: str) -> Dict:
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading input config: {e}")
            return {}
    
    def process_documents(self, config: Dict, pdf_directory: str) -> Dict:
        document_paths = []
        input_documents = []
        
        for doc in config.get('documents', []):
            filename = doc['filename']
            pdf_path = os.path.join(pdf_directory, filename)
            if os.path.exists(pdf_path):
                document_paths.append(pdf_path)
                input_documents.append(filename)
        
        processed_docs = self.doc_processor.process_documents(document_paths)
        
        persona = config.get('persona', {}).get('role', 'General User')
        job_description = config.get('job_to_be_done', {}).get('task', 'General analysis')
        
        ranked_sections = self.persona_analyzer.rank_sections(
            processed_docs, persona, job_description
        )
        
        extracted_sections = self.section_extractor.format_extracted_sections(ranked_sections)
        subsection_analysis = self.section_extractor.generate_subsection_analysis(ranked_sections)
        
        output = {
            "metadata": {
                "input_documents": input_documents,
                "persona": persona,
                "job_to_be_done": job_description,
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": extracted_sections,
            "subsection_analysis": subsection_analysis
        }
        
        return output
    
    def save_output(self, output: Dict, output_path: str):
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
            print(f"Output saved to: {output_path}")
        except Exception as e:
            print(f"Error saving output: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <collection_path>")
        print("Example: python main.py Collection\ 1")
        sys.exit(1)
    
    collection_path = sys.argv[1]
    
    if not os.path.exists(collection_path):
        print(f"Collection path does not exist: {collection_path}")
        sys.exit(1)
    
    input_file = os.path.join(collection_path, "challenge1b_input.json")
    output_file = os.path.join(collection_path, "challenge1b_output.json")
    pdf_directory = os.path.join(collection_path, "PDFs")
    
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        sys.exit(1)
    
    if not os.path.exists(pdf_directory):
        print(f"PDF directory not found: {pdf_directory}")
        sys.exit(1)
    
    pdi = PersonaDocumentIntelligence()
    
    print("Loading input configuration...")
    config = pdi.load_input_config(input_file)
    
    if not config:
        print("Failed to load input configuration")
        sys.exit(1)
    
    print("Processing documents...")
    output = pdi.process_documents(config, pdf_directory)
    
    print("Saving output...")
    pdi.save_output(output, output_file)
    
    print("Processing completed successfully!")

if __name__ == "__main__":
    main()