from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.budget import DBBudget
from models.expense import DBExpense
from datetime import datetime

router = APIRouter()

@router.post("/budgets")
def create_budget(category: str, monthly_limit: float, db: Session = Depends(get_db)):
    """Create a new budget for a category"""
    
    current_month = datetime.now().strftime('%Y-%m')
    
    # Check if budget already exists for this month/category
    existing = db.query(DBBudget).filter(
        DBBudget.category == category,
        DBBudget.month == current_month
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Budget already exists for this category this month")
    
    # Calculate current spending for this category this month
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_spent = db.query(DBExpense).filter(
        DBExpense.category == category,
        DBExpense.date >= month_start
    ).with_entities(DBExpense.amount).all()
    
    total_spent = sum(amount[0] for amount in current_spent)
    
    budget = DBBudget(
        category=category,
        monthly_limit=monthly_limit,
        current_spent=total_spent,
        month=current_month
    )
    
    db.add(budget)
    db.commit()
    db.refresh(budget)
    
    return budget

@router.get("/budgets")
def get_budgets(db: Session = Depends(get_db)):
    """Get all active budgets"""
    current_month = datetime.now().strftime('%Y-%m')
    budgets = db.query(DBBudget).filter(
        DBBudget.month == current_month,
        DBBudget.is_active == True
    ).all()
    
    return budgets

@router.get("/budgets/status")
def get_budget_status(db: Session = Depends(get_db)):
    """Get budget status with AI insights"""
    current_month = datetime.now().strftime('%Y-%m')
    budgets = db.query(DBBudget).filter(
        DBBudget.month == current_month,
        DBBudget.is_active == True
    ).all()
    
    status_report = []
    
    for budget in budgets:
        percentage_used = (budget.current_spent / budget.monthly_limit) * 100 if budget.monthly_limit > 0 else 0
        remaining = budget.monthly_limit - budget.current_spent
        
        # AI status assessment
        if percentage_used >= 90:
            status = "critical"
            ai_advice = "Budget almost exceeded! Consider reducing spending in this category."
        elif percentage_used >= 75:
            status = "warning"
            ai_advice = "Approaching budget limit. Monitor spending carefully."
        elif percentage_used >= 50:
            status = "on_track"
            ai_advice = "Good progress. Stay mindful of remaining budget."
        else:
            status = "safe"
            ai_advice = "Well within budget. Good financial discipline!"
        
        status_report.append({
            'category': budget.category,
            'monthly_limit': budget.monthly_limit,
            'current_spent': budget.current_spent,
            'remaining': remaining,
            'percentage_used': percentage_used,
            'status': status,
            'ai_advice': ai_advice
        })
    
    return {
        'budgets': status_report,
        'month': current_month,
        'total_budgets': len(budgets)
    }