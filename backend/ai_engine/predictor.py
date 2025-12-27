import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd

class SpendingPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.poly_features = PolynomialFeatures(degree=2)
        self.is_trained = False
    
    def predict_next_month(self, expenses: List[Dict]) -> Dict:
        """Predict next month's spending using AI"""
        if not expenses:
            return self._default_prediction()
        
        # Prepare data for prediction
        df = self._prepare_data(expenses)
        
        if len(df) < 7:  # Need at least a week of data
            return self._simple_prediction(expenses)
        
        # Train model and predict
        try:
            prediction = self._ml_prediction(df)
            return prediction
        except Exception as e:
            return self._simple_prediction(expenses)
    
    def _prepare_data(self, expenses: List[Dict]) -> pd.DataFrame:
        """Prepare expense data for ML model"""
        data = []
        
        for expense in expenses:
            data.append({
                'date': expense.get('date', datetime.now().isoformat()),
                'amount': expense.get('amount', 0),
                'category': expense.get('category', 'other')
            })
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Group by day
        daily_spending = df.groupby(df['date'].dt.date)['amount'].sum().reset_index()
        daily_spending['day_number'] = range(len(daily_spending))
        
        return daily_spending
    
    def _ml_prediction(self, df: pd.DataFrame) -> Dict:
        """Use machine learning for prediction"""
        X = df[['day_number']].values
        y = df['amount'].values
        
        # Apply polynomial features for better fitting
        X_poly = self.poly_features.fit_transform(X)
        
        # Train the model
        self.model.fit(X_poly, y)
        self.is_trained = True
        
        # Predict next 30 days
        future_days = np.array([[len(df) + i] for i in range(30)])
        future_days_poly = self.poly_features.transform(future_days)
        predictions = self.model.predict(future_days_poly)
        
        # Ensure predictions are positive
        predictions = np.maximum(predictions, 0)
        
        total_predicted = float(np.sum(predictions))
        daily_average = float(np.mean(predictions))
        
        # Calculate trend
        recent_avg = float(df.tail(7)['amount'].mean())
        trend = "increasing" if daily_average > recent_avg else "decreasing"
        
        return {
            'predicted_total': total_predicted,
            'daily_average': daily_average,
            'trend': trend,
            'confidence': self._calculate_confidence(df, predictions),
            'method': 'ml_prediction',
            'daily_predictions': predictions.tolist()[:7]  # First week
        }
    
    def _simple_prediction(self, expenses: List[Dict]) -> Dict:
        """Simple average-based prediction"""
        total_amount = sum(exp.get('amount', 0) for exp in expenses)
        days_of_data = len(set(exp.get('date', '')[:10] for exp in expenses))
        
        if days_of_data == 0:
            return self._default_prediction()
        
        daily_average = total_amount / days_of_data
        predicted_total = daily_average * 30
        
        return {
            'predicted_total': predicted_total,
            'daily_average': daily_average,
            'trend': 'stable',
            'confidence': 0.6,
            'method': 'simple_average',
            'daily_predictions': [daily_average] * 7
        }
    
    def _default_prediction(self) -> Dict:
        """Default prediction when no data available"""
        return {
            'predicted_total': 1000.0,
            'daily_average': 33.33,
            'trend': 'unknown',
            'confidence': 0.3,
            'method': 'default',
            'daily_predictions': [33.33] * 7
        }
    
    def _calculate_confidence(self, df: pd.DataFrame, predictions: np.ndarray) -> float:
        """Calculate prediction confidence based on data quality"""
        data_points = len(df)
        variance = float(df['amount'].var())
        
        # More data points = higher confidence
        data_confidence = min(data_points / 30, 1.0)
        
        # Lower variance = higher confidence
        variance_confidence = 1.0 / (1.0 + variance / 1000)
        
        return float((data_confidence + variance_confidence) / 2)
    
    def predict_category_spending(self, expenses: List[Dict], category: str) -> Dict:
        """Predict spending for a specific category"""
        category_expenses = [exp for exp in expenses if exp.get('category') == category]
        
        if not category_expenses:
            return {
                'predicted_amount': 0.0,
                'confidence': 0.0,
                'trend': 'no_data'
            }
        
        total = sum(exp.get('amount', 0) for exp in category_expenses)
        days = len(set(exp.get('date', '')[:10] for exp in category_expenses))
        
        if days == 0:
            return {'predicted_amount': 0.0, 'confidence': 0.0, 'trend': 'no_data'}
        
        daily_avg = total / days
        predicted_monthly = daily_avg * 30
        
        return {
            'predicted_amount': predicted_monthly,
            'confidence': min(days / 30, 1.0),
            'trend': 'stable'
        }