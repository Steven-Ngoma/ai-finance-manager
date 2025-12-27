from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.expense import DBExpense
from schemas.expense import ExpenseCreate, ExpenseResponse
from ai_engine.categorizer import ExpenseCategorizer

router = APIRouter()
categorizer = ExpenseCategorizer()

@router.post("/expenses", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """Create new expense with AI categorization"""
    
    # Use AI to categorize the expense
    ai_result = categorizer.categorize(expense.description, expense.amount)
    
    # Create expense with AI insights
    db_expense = DBExpense(
        description=expense.description,
        amount=expense.amount,
        category=expense.category or ai_result['category'],
        ai_category=ai_result['category'],
        ai_confidence=ai_result['confidence'],
        payment_method=expense.payment_method,
        location=expense.location,
        notes=expense.notes
    )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    return ExpenseResponse(
        id=db_expense.id,
        description=db_expense.description,
        amount=db_expense.amount,
        category=db_expense.category,
        date=db_expense.date,
        ai_category=db_expense.ai_category,
        ai_confidence=db_expense.ai_confidence,
        payment_method=db_expense.payment_method,
        location=db_expense.location,
        notes=db_expense.notes
    )

@router.get("/expenses", response_model=List[ExpenseResponse])
def get_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all expenses"""
    expenses = db.query(DBExpense).offset(skip).limit(limit).all()
    return expenses

@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """Get specific expense"""
    expense = db.query(DBExpense).filter(DBExpense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/expenses/{expense_id}/recategorize")
def recategorize_expense(expense_id: int, db: Session = Depends(get_db)):
    """Re-run AI categorization on an expense"""
    expense = db.query(DBExpense).filter(DBExpense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # Re-categorize with AI
    ai_result = categorizer.categorize(expense.description, expense.amount)
    
    expense.ai_category = ai_result['category']
    expense.ai_confidence = ai_result['confidence']
    
    db.commit()
    
    return {
        "message": "Expense recategorized",
        "new_category": ai_result['category'],
        "confidence": ai_result['confidence']
    }

@router.get("/expenses/category/{category}")
def get_expenses_by_category(category: str, db: Session = Depends(get_db)):
    """Get expenses by category"""
    expenses = db.query(DBExpense).filter(DBExpense.category == category).all()
    return expenses

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Delete an expense"""
    expense = db.query(DBExpense).filter(DBExpense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    
    return {"message": "Expense deleted successfully"}