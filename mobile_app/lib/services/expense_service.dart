import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/expense.dart';

class ExpenseService extends ChangeNotifier {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  
  List<Expense> _expenses = [];
  bool _isLoading = false;

  List<Expense> get expenses => _expenses;
  bool get isLoading => _isLoading;
  
  double get totalSpent => _expenses.fold(0.0, (sum, expense) => sum + expense.amount);
  
  Map<String, double> get categoryTotals {
    Map<String, double> totals = {};
    for (var expense in _expenses) {
      totals[expense.category] = (totals[expense.category] ?? 0) + expense.amount;
    }
    return totals;
  }

  Future<void> loadExpenses() async {
    _isLoading = true;
    notifyListeners();

    try {
      final response = await http.get(
        Uri.parse('$baseUrl/expenses'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        _expenses = data.map((json) => Expense.fromJson(json)).toList();
      } else {
        _loadSampleData();
      }
    } catch (e) {
      debugPrint('Error loading expenses: $e');
      _loadSampleData();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void _loadSampleData() {
    _expenses = [
      Expense(
        id: 1,
        description: 'Grocery Shopping',
        amount: 85.50,
        category: 'Food',
        date: DateTime.now().subtract(const Duration(days: 1)),
        aiCategory: 'Food',
        aiConfidence: 0.95,
      ),
      Expense(
        id: 2,
        description: 'Uber Ride',
        amount: 12.30,
        category: 'Transport',
        date: DateTime.now().subtract(const Duration(days: 2)),
        aiCategory: 'Transport',
        aiConfidence: 0.88,
      ),
      Expense(
        id: 3,
        description: 'Netflix Subscription',
        amount: 15.99,
        category: 'Entertainment',
        date: DateTime.now().subtract(const Duration(days: 3)),
        aiCategory: 'Entertainment',
        aiConfidence: 0.92,
      ),
      Expense(
        id: 4,
        description: 'Coffee Shop',
        amount: 4.75,
        category: 'Food',
        date: DateTime.now().subtract(const Duration(days: 4)),
        aiCategory: 'Food',
        aiConfidence: 0.85,
      ),
      Expense(
        id: 5,
        description: 'Amazon Purchase',
        amount: 67.99,
        category: 'Shopping',
        date: DateTime.now().subtract(const Duration(days: 5)),
        aiCategory: 'Shopping',
        aiConfidence: 0.78,
      ),
    ];
  }

  Future<bool> addExpense(Expense expense) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/expenses'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'description': expense.description,
          'amount': expense.amount,
          'category': expense.category,
          'payment_method': expense.paymentMethod,
          'location': expense.location,
          'notes': expense.notes,
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final newExpense = Expense.fromJson(data);
        _expenses.insert(0, newExpense);
        notifyListeners();
        return true;
      } else {
        // Fallback: add locally with mock data
        final newExpense = Expense(
          id: DateTime.now().millisecondsSinceEpoch,
          description: expense.description,
          amount: expense.amount,
          category: expense.category,
          date: DateTime.now(),
          aiCategory: expense.category,
          aiConfidence: 0.8,
          paymentMethod: expense.paymentMethod,
          location: expense.location,
          notes: expense.notes,
        );
        _expenses.insert(0, newExpense);
        notifyListeners();
        return true;
      }
    } catch (e) {
      debugPrint('Error adding expense: $e');
      return false;
    }
  }

  Future<bool> deleteExpense(int expenseId) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/expenses/$expenseId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        _expenses.removeWhere((expense) => expense.id == expenseId);
        notifyListeners();
        return true;
      }
    } catch (e) {
      debugPrint('Error deleting expense: $e');
    }
    return false;
  }

  List<Expense> getExpensesByCategory(String category) {
    return _expenses.where((expense) => expense.category == category).toList();
  }

  List<Expense> getRecentExpenses({int limit = 10}) {
    final sorted = List<Expense>.from(_expenses)
      ..sort((a, b) => b.date.compareTo(a.date));
    return sorted.take(limit).toList();
  }

  double getMonthlySpending() {
    final now = DateTime.now();
    final monthStart = DateTime(now.year, now.month, 1);
    
    return _expenses
        .where((expense) => expense.date.isAfter(monthStart))
        .fold(0.0, (sum, expense) => sum + expense.amount);
  }

  Map<String, double> getWeeklySpending() {
    final now = DateTime.now();
    final weekStart = now.subtract(Duration(days: now.weekday - 1));
    
    Map<String, double> weeklyData = {};
    
    for (int i = 0; i < 7; i++) {
      final day = weekStart.add(Duration(days: i));
      final dayName = _getDayName(day.weekday);
      
      final dayTotal = _expenses
          .where((expense) => 
              expense.date.year == day.year &&
              expense.date.month == day.month &&
              expense.date.day == day.day)
          .fold(0.0, (sum, expense) => sum + expense.amount);
      
      weeklyData[dayName] = dayTotal;
    }
    
    return weeklyData;
  }

  String _getDayName(int weekday) {
    switch (weekday) {
      case 1: return 'Mon';
      case 2: return 'Tue';
      case 3: return 'Wed';
      case 4: return 'Thu';
      case 5: return 'Fri';
      case 6: return 'Sat';
      case 7: return 'Sun';
      default: return '';
    }
  }
}