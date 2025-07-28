import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import Dict, List, Tuple

class PersonaAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.persona_keywords = {}
        self.job_keywords = {}
        
    def extract_persona_keywords(self, persona: str) -> List[str]:
        persona_mapping = {
            'travel planner': ['travel', 'trip', 'journey', 'vacation', 'tourism', 'destination', 'itinerary', 'visit', 'explore', 'adventure', 'accommodation', 'hotel', 'activities', 'attractions', 'guide', 'planning'],
            'researcher': ['research', 'study', 'analysis', 'methodology', 'data', 'findings', 'literature', 'academic', 'investigation', 'experiment', 'theory', 'hypothesis', 'evidence'],
            'student': ['learn', 'study', 'education', 'course', 'exam', 'assignment', 'knowledge', 'understanding', 'concept', 'theory', 'practice', 'skill', 'development'],
            'hr professional': ['employee', 'hiring', 'recruitment', 'onboarding', 'training', 'policy', 'compliance', 'form', 'documentation', 'process', 'management', 'workflow'],
            'food contractor': ['food', 'recipe', 'cooking', 'menu', 'ingredient', 'preparation', 'cuisine', 'meal', 'dish', 'catering', 'buffet', 'vegetarian', 'nutrition']
        }
        
        persona_lower = persona.lower()
        keywords = []
        
        for key, values in persona_mapping.items():
            if key in persona_lower:
                keywords.extend(values)
        
        return keywords
    
    def extract_job_keywords(self, job_description: str) -> List[str]:
        job_lower = job_description.lower()
        keywords = []
        
        if 'trip' in job_lower or 'travel' in job_lower:
            keywords.extend(['itinerary', 'destination', 'activities', 'accommodation', 'transportation', 'budget', 'group', 'friends'])
        
        if 'menu' in job_lower or 'food' in job_lower:
            keywords.extend(['recipe', 'ingredient', 'cooking', 'preparation', 'serving', 'dietary', 'nutrition', 'buffet'])
        
        if 'form' in job_lower or 'document' in job_lower:
            keywords.extend(['template', 'fillable', 'process', 'workflow', 'compliance', 'management'])
        
        if 'research' in job_lower or 'literature' in job_lower:
            keywords.extend(['methodology', 'analysis', 'findings', 'sources', 'references', 'study'])
        
        numbers = re.findall(r'\d+', job_description)
        if numbers:
            keywords.extend(['planning', 'organization', 'logistics'])
        
        return keywords
    
    def calculate_relevance_score(self, section_content: str, persona: str, job_description: str) -> float:
        persona_keywords = self.extract_persona_keywords(persona)
        job_keywords = self.extract_job_keywords(job_description)
        
        all_keywords = list(set(persona_keywords + job_keywords))
        
        content_lower = section_content.lower()
        keyword_matches = 0
        total_keywords = len(all_keywords)
        
        for keyword in all_keywords:
            if keyword in content_lower:
                keyword_matches += 1
        
        keyword_score = keyword_matches / max(total_keywords, 1)
        
        length_score = min(len(section_content.split()) / 100, 1.0)
        
        structure_score = 0.0
        if any(marker in content_lower for marker in [':', '-', '•', '1.', '2.', '3.']):
            structure_score = 0.3
        
        final_score = (keyword_score * 0.6) + (length_score * 0.2) + (structure_score * 0.2)
        
        return min(final_score, 1.0)
    
    def rank_sections(self, sections_data: Dict, persona: str, job_description: str) -> List[Dict]:
        all_sections = []
        
        for document, doc_data in sections_data.items():
            for page_num, sections in doc_data['sections'].items():
                for section in sections:
                    relevance_score = self.calculate_relevance_score(
                        section['content'], persona, job_description
                    )
                    
                    all_sections.append({
                        'document': document,
                        'section_title': section['title'],
                        'content': section['content'],
                        'page_number': page_num,
                        'relevance_score': relevance_score,
                        'word_count': section['word_count']
                    })
        
        all_sections.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        for i, section in enumerate(all_sections, 1):
            section['importance_rank'] = i
        
        return all_sections[:10]