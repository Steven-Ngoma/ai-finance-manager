from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.expense import DBExpense
from ai_engine.predictor import SpendingPredictor
from datetime import datetime, timedelta

router = APIRouter()
predictor = SpendingPredictor()

@router.get("/predictions/next-month")
def predict_next_month_spending(db: Session = Depends(get_db)):
    """AI prediction for next month's spending"""
    
    # Get recent expenses (last 60 days)
    cutoff_date = datetime.now() - timedelta(days=60)
    expenses = db.query(DBExpense).filter(DBExpense.date >= cutoff_date).all()
    
    # Convert to format expected by AI
    expense_data = [
        {
            'date': exp.date.isoformat(),
            'amount': exp.amount,
            'category': exp.category
        }
        for exp in expenses
    ]
    
    # Get AI prediction
    prediction = predictor.predict_next_month(expense_data)
    
    return {
        "prediction": prediction,
        "data_points": len(expense_data),
        "analysis_period": "60 days",
        "generated_at": datetime.now().isoformat()
    }

@router.get("/predictions/category/{category}")
def predict_category_spending(category: str, db: Session = Depends(get_db)):
    """AI prediction for specific category spending"""
    
    # Get category expenses (last 60 days)
    cutoff_date = datetime.now() - timedelta(days=60)
    expenses = db.query(DBExpense).filter(
        DBExpense.category == category,
        DBExpense.date >= cutoff_date
    ).all()
    
    expense_data = [
        {
            'date': exp.date.isoformat(),
            'amount': exp.amount,
            'category': exp.category
        }
        for exp in expenses
    ]
    
    prediction = predictor.predict_category_spending(expense_data, category)
    
    return {
        "category": category,
        "prediction": prediction,
        "historical_data_points": len(expense_data)
    }

@router.get("/predictions/weekly-forecast")
def get_weekly_forecast(db: Session = Depends(get_db)):
    """Get AI forecast for the next 7 days"""
    
    cutoff_date = datetime.now() - timedelta(days=30)
    expenses = db.query(DBExpense).filter(DBExpense.date >= cutoff_date).all()
    
    expense_data = [
        {
            'date': exp.date.isoformat(),
            'amount': exp.amount,
            'category': exp.category
        }
        for exp in expenses
    ]
    
    prediction = predictor.predict_next_month(expense_data)
    
    return {
        "weekly_forecast": prediction.get('daily_predictions', []),
        "total_week_prediction": sum(prediction.get('daily_predictions', [])),
        "confidence": prediction.get('confidence', 0.5),
        "trend": prediction.get('trend', 'stable')
    }

@router.get("/predictions/spending-patterns")
def analyze_spending_patterns(db: Session = Depends(get_db)):
    """Analyze spending patterns using AI"""
    
    # Get last 90 days of data
    cutoff_date = datetime.now() - timedelta(days=90)
    expenses = db.query(DBExpense).filter(DBExpense.date >= cutoff_date).all()
    
    # Group by day of week
    day_patterns = {}
    category_patterns = {}
    
    for expense in expenses:
        day_name = expense.date.strftime('%A')
        category = expense.category
        
        # Day patterns
        if day_name not in day_patterns:
            day_patterns[day_name] = []
        day_patterns[day_name].append(expense.amount)
        
        # Category patterns
        if category not in category_patterns:
            category_patterns[category] = []
        category_patterns[category].append(expense.amount)
    
    # Calculate averages
    day_averages = {
        day: sum(amounts) / len(amounts) if amounts else 0
        for day, amounts in day_patterns.items()
    }
    
    category_totals = {
        cat: sum(amounts) for cat, amounts in category_patterns.items()
    }
    
    return {
        "daily_patterns": day_averages,
        "category_breakdown": category_totals,
        "highest_spending_day": max(day_averages, key=day_averages.get) if day_averages else None,
        "top_category": max(category_totals, key=category_totals.get) if category_totals else None,
        "analysis_period": "90 days",
        "total_expenses": len(expenses)
    }