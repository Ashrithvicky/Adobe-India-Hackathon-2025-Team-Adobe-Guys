import re
from typing import Dict, List

class SectionExtractor:
    def __init__(self):
        pass
    
    def extract_subsections(self, content: str, max_length: int = 800) -> str:
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        refined_content = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if current_length + len(sentence) <= max_length:
                refined_content.append(sentence)
                current_length += len(sentence) + 1
            else:
                break
        
        result = ' '.join(refined_content)
        
        if not result.endswith('.'):
            if result.endswith(',') or result.endswith(';'):
                result = result[:-1] + '.'
            else:
                result += '.'
        
        return result
    
    def clean_and_format_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        text = text.strip()
        
        if not text.endswith('.'):
            text += '.'
        
        return text
    
    def generate_subsection_analysis(self, ranked_sections: List[Dict]) -> List[Dict]:
        subsection_analysis = []
        
        for section in ranked_sections[:5]:
            refined_text = self.extract_subsections(section['content'])
            refined_text = self.clean_and_format_text(refined_text)
            
            if len(refined_text.split()) >= 20:
                subsection_analysis.append({
                    'document': section['document'],
                    'refined_text': refined_text,
                    'page_number': section['page_number']
                })
        
        return subsection_analysis
    
    def format_extracted_sections(self, ranked_sections: List[Dict]) -> List[Dict]:
        extracted_sections = []
        
        for section in ranked_sections[:5]:
            extracted_sections.append({
                'document': section['document'],
                'section_title': section['section_title'],
                'importance_rank': section['importance_rank'],
                'page_number': section['page_number']
            })
        
        return extracted_sections