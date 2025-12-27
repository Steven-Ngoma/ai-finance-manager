from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.expense import DBExpense
from ai_engine.categorizer import ExpenseCategorizer
from datetime import datetime, timedelta

router = APIRouter()
categorizer = ExpenseCategorizer()

@router.get("/insights/spending-summary")
def get_spending_insights(db: Session = Depends(get_db)):
    """Get AI-powered spending insights"""
    
    # Get last 30 days of expenses
    cutoff_date = datetime.now() - timedelta(days=30)
    expenses = db.query(DBExpense).filter(DBExpense.date >= cutoff_date).all()
    
    expense_data = [
        {
            'category': exp.category,
            'amount': exp.amount,
            'date': exp.date.isoformat()
        }
        for exp in expenses
    ]
    
    insights = categorizer.get_category_insights(expense_data)
    
    # Add AI recommendations
    recommendations = []
    
    if insights['category_breakdown']:
        top_category = insights['top_category']
        top_amount = insights['category_breakdown'][top_category]
        
        if top_amount > 500:  # If spending more than $500 in top category
            recommendations.append(f"Consider reducing {top_category} expenses - it's your highest spending category")
        
        if 'food' in insights['category_breakdown'] and insights['category_breakdown']['food'] > 300:
            recommendations.append("Food expenses are high - try meal planning to save money")
    
    return {
        "insights": insights,
        "recommendations": recommendations,
        "period": "Last 30 days",
        "total_transactions": len(expenses)
    }

@router.get("/insights/savings-opportunities")
def get_savings_opportunities(db: Session = Depends(get_db)):
    """AI-powered savings recommendations"""
    
    cutoff_date = datetime.now() - timedelta(days=60)
    expenses = db.query(DBExpense).filter(DBExpense.date >= cutoff_date).all()
    
    category_spending = {}
    for expense in expenses:
        cat = expense.category
        if cat in category_spending:
            category_spending[cat] += expense.amount
        else:
            category_spending[cat] = expense.amount
    
    opportunities = []
    
    # Analyze each category for savings
    for category, total in category_spending.items():
        monthly_avg = total / 2  # 60 days = ~2 months
        
        if category == 'food' and monthly_avg > 400:
            potential_savings = monthly_avg * 0.2  # 20% savings potential
            opportunities.append({
                'category': category,
                'current_monthly': monthly_avg,
                'potential_savings': potential_savings,
                'recommendation': 'Try meal planning and cooking at home more often'
            })
        
        elif category == 'transport' and monthly_avg > 200:
            potential_savings = monthly_avg * 0.15
            opportunities.append({
                'category': category,
                'current_monthly': monthly_avg,
                'potential_savings': potential_savings,
                'recommendation': 'Consider carpooling or public transport'
            })
        
        elif category == 'entertainment' and monthly_avg > 150:
            potential_savings = monthly_avg * 0.25
            opportunities.append({
                'category': category,
                'current_monthly': monthly_avg,
                'potential_savings': potential_savings,
                'recommendation': 'Look for free entertainment alternatives'
            })
    
    total_potential_savings = sum(opp['potential_savings'] for opp in opportunities)
    
    return {
        'opportunities': opportunities,
        'total_potential_monthly_savings': total_potential_savings,
        'analysis_period': '60 days'
    }