from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import expenses, predictions, insights, budgets
from models.expense import DBExpense
from models.budget import DBBudget

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Finance Manager API",
    description="AI-Powered Personal Finance Management System",
    version="1.0.0"
)

# CORS middleware for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(expenses.router, prefix="/api/v1", tags=["expenses"])
app.include_router(predictions.router, prefix="/api/v1", tags=["ai-predictions"])
app.include_router(insights.router, prefix="/api/v1", tags=["ai-insights"])
app.include_router(budgets.router, prefix="/api/v1", tags=["budgets"])

@app.get("/")
def read_root():
    return {
        "message": "AI Finance Manager API",
        "features": [
            "Smart expense categorization",
            "AI spending predictions",
            "Budget optimization",
            "Financial insights"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "ai_engine": "active"}