import re
from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

class ExpenseCategorizer:
    def __init__(self):
        self.categories = {
            'food': ['restaurant', 'grocery', 'food', 'cafe', 'pizza', 'burger', 'coffee', 'lunch', 'dinner'],
            'transport': ['uber', 'taxi', 'bus', 'fuel', 'gas', 'parking', 'metro', 'train'],
            'shopping': ['amazon', 'store', 'mall', 'clothing', 'shoes', 'electronics', 'online'],
            'entertainment': ['movie', 'cinema', 'game', 'music', 'netflix', 'spotify', 'concert'],
            'utilities': ['electricity', 'water', 'internet', 'phone', 'rent', 'mortgage'],
            'healthcare': ['hospital', 'doctor', 'pharmacy', 'medicine', 'clinic', 'dental'],
            'education': ['school', 'university', 'course', 'book', 'tuition', 'training'],
            'other': []
        }
        
        self.model = None
        self.vectorizer = None
        self._train_model()
    
    def _train_model(self):
        """Train the categorization model with sample data"""
        training_data = []
        training_labels = []
        
        # Generate training data from keywords
        for category, keywords in self.categories.items():
            if category != 'other':
                for keyword in keywords:
                    training_data.append(keyword)
                    training_labels.append(category)
                    # Add variations
                    training_data.append(f"{keyword} payment")
                    training_labels.append(category)
        
        # Train the model
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        X = self.vectorizer.fit_transform(training_data)
        
        self.model = MultinomialNB()
        self.model.fit(X, training_labels)
    
    def categorize(self, description: str, amount: float = None) -> Dict:
        """Categorize expense using AI"""
        description_clean = self._clean_description(description)
        
        # Use ML model for prediction
        if self.model and self.vectorizer:
            try:
                X = self.vectorizer.transform([description_clean])
                predicted_category = self.model.predict(X)[0]
                confidence = max(self.model.predict_proba(X)[0])
                
                return {
                    'category': predicted_category,
                    'confidence': float(confidence),
                    'method': 'ml_model'
                }
            except:
                pass
        
        # Fallback to keyword matching
        return self._keyword_categorize(description_clean)
    
    def _clean_description(self, description: str) -> str:
        """Clean and normalize description"""
        return re.sub(r'[^a-zA-Z\s]', '', description.lower()).strip()
    
    def _keyword_categorize(self, description: str) -> Dict:
        """Fallback keyword-based categorization"""
        description_lower = description.lower()
        
        for category, keywords in self.categories.items():
            if category != 'other':
                for keyword in keywords:
                    if keyword in description_lower:
                        return {
                            'category': category,
                            'confidence': 0.8,
                            'method': 'keyword_match'
                        }
        
        return {
            'category': 'other',
            'confidence': 0.5,
            'method': 'default'
        }
    
    def get_category_insights(self, expenses: List[Dict]) -> Dict:
        """Generate insights about spending categories"""
        category_totals = {}
        
        for expense in expenses:
            category = expense.get('category', 'other')
            amount = expense.get('amount', 0)
            
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount
        
        total_spending = sum(category_totals.values())
        
        insights = {
            'category_breakdown': category_totals,
            'total_spending': total_spending,
            'top_category': max(category_totals, key=category_totals.get) if category_totals else 'none',
            'category_percentages': {
                cat: (amount / total_spending * 100) if total_spending > 0 else 0
                for cat, amount in category_totals.items()
            }
        }
        
        return insights