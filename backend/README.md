# Personal Finance Manager

A comprehensive personal finance management application built with Flutter and FastAPI, featuring intelligent expense categorization, predictive analytics, and budget optimization.

## Features

### Core Functionality
- **Expense Tracking**: Record and categorize expenses with automatic categorization
- **Budget Management**: Set and monitor budgets across different categories
- **Financial Analytics**: Detailed spending analysis and insights
- **Predictive Modeling**: Forecast future spending patterns and trends
- **Multi-platform Support**: Available on Android, iOS, and Web

### Advanced Features
- **Smart Categorization**: Automatic expense categorization using machine learning
- **Spending Predictions**: Predict next month's expenses based on historical data
- **Budget Optimization**: Intelligent recommendations for budget allocation
- **Visual Analytics**: Interactive charts and graphs for spending visualization
- **Savings Opportunities**: Identify potential areas for cost reduction

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **SQLite**: Lightweight database for data storage
- **Python**: Core backend programming language

### Frontend
- **Flutter**: Cross-platform mobile development framework
- **Dart**: Programming language for Flutter development
- **Provider**: State management solution
- **FL Chart**: Beautiful charts and graphs
- **Google Fonts**: Typography enhancement

### Machine Learning
- **Scikit-learn**: Machine learning algorithms for predictions
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing support

## Project Structure

```
ai_finance_manager/
├── backend/                 # FastAPI backend application
│   ├── ai_engine/          # Machine learning models and algorithms
│   ├── models/             # Database models
│   ├── routes/             # API endpoints
│   ├── schemas/            # Pydantic schemas
│   └── main.py            # Application entry point
├── mobile_app/             # Flutter mobile application
│   ├── lib/
│   │   ├── models/         # Data models
│   │   ├── screens/        # UI screens
│   │   ├── services/       # API services
│   │   └── widgets/        # Reusable UI components
│   └── pubspec.yaml       # Flutter dependencies
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Flutter SDK 3.0+
- Android Studio (for Android development)
- VS Code or preferred IDE

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Mobile App Setup

1. Navigate to the mobile app directory:
```bash
cd mobile_app
```

2. Install Flutter dependencies:
```bash
flutter pub get
```

3. Run the application:
```bash
flutter run
```

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

### Key Endpoints

- `GET /api/v1/expenses` - Retrieve all expenses
- `POST /api/v1/expenses` - Create new expense
- `GET /api/v1/predictions/next-month` - Get next month spending prediction
- `GET /api/v1/insights/savings-opportunities` - Get savings recommendations
- `GET /api/v1/budgets` - Retrieve budget information

## Usage

### Adding Expenses
1. Open the mobile application
2. Tap the "Add Expense" button
3. Enter expense details (amount, description, category)
4. The system will automatically categorize similar future expenses

### Viewing Analytics
1. Navigate to the Dashboard
2. View spending overview charts
3. Check monthly budget progress
4. Review spending predictions and insights

### Budget Management
1. Go to Budget screen
2. Set monthly budgets for different categories
3. Monitor spending against budgets
4. Receive notifications when approaching limits

## Development

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Flutter tests
cd mobile_app
flutter test
```

### Code Style
- Backend: Follow PEP 8 guidelines
- Frontend: Follow Dart style guide
- Use meaningful variable names and add comments for complex logic

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Performance Optimization

- **Database**: Optimized queries with proper indexing
- **Caching**: Implemented caching for frequently accessed data
- **Mobile**: Efficient state management and lazy loading
- **API**: Asynchronous processing for better response times

## Security Features

- Input validation and sanitization
- Secure API endpoints
- Data encryption for sensitive information
- Regular security updates and patches

## Future Enhancements

- [ ] Bank account integration
- [ ] Receipt scanning with OCR
- [ ] Investment tracking
- [ ] Multi-currency support
- [ ] Advanced reporting features
- [ ] Cloud synchronization



## License

This project is licensed under the MIT License - see the LICENSE file for details.

**Steven Ngoma**  
Email: stevenngoma697@gmail.com  
Phone: +260 776 987 839

---

*Built with passion for financial technology and user experience.*