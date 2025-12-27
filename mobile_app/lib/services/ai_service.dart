import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AIService extends ChangeNotifier {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  
  double _nextMonthPrediction = 0.0;
  double _savingsOpportunity = 0.0;
  String _topSpendingCategory = 'Loading...';
  List<Map<String, dynamic>> _weeklyForecast = [];
  Map<String, dynamic> _spendingPatterns = {};
  bool _isLoading = false;

  // Getters
  double get nextMonthPrediction => _nextMonthPrediction;
  double get savingsOpportunity => _savingsOpportunity;
  String get topSpendingCategory => _topSpendingCategory;
  List<Map<String, dynamic>> get weeklyForecast => _weeklyForecast;
  Map<String, dynamic> get spendingPatterns => _spendingPatterns;
  bool get isLoading => _isLoading;

  Future<void> loadPredictions() async {
    _isLoading = true;
    notifyListeners();

    try {
      // Load next month prediction
      await _loadNextMonthPrediction();
      
      // Load savings opportunities
      await _loadSavingsOpportunities();
      
      // Load spending patterns
      await _loadSpendingPatterns();
      
      // Load weekly forecast
      await _loadWeeklyForecast();
      
    } catch (e) {
      debugPrint('Error loading AI predictions: $e');
      _setDefaultValues();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> _loadNextMonthPrediction() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/predictions/next-month'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _nextMonthPrediction = data['prediction']['predicted_total']?.toDouble() ?? 0.0;
      } else {
        _nextMonthPrediction = 1200.0; // Default prediction
      }
    } catch (e) {
      _nextMonthPrediction = 1200.0;
    }
  }

  Future<void> _loadSavingsOpportunities() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/insights/savings-opportunities'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _savingsOpportunity = data['total_potential_monthly_savings']?.toDouble() ?? 0.0;
      } else {
        _savingsOpportunity = 150.0; // Default savings opportunity
      }
    } catch (e) {
      _savingsOpportunity = 150.0;
    }
  }

  Future<void> _loadSpendingPatterns() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/predictions/spending-patterns'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _spendingPatterns = data;
        _topSpendingCategory = data['top_category'] ?? 'Food';
      } else {
        _setDefaultPatterns();
      }
    } catch (e) {
      _setDefaultPatterns();
    }
  }

  Future<void> _loadWeeklyForecast() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/predictions/weekly-forecast'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _weeklyForecast = List<Map<String, dynamic>>.from(
          data['weekly_forecast']?.map((item) => {
            'day': DateTime.now().add(Duration(days: _weeklyForecast.length)).weekday,
            'amount': item?.toDouble() ?? 0.0,
          }) ?? []
        );
      } else {
        _setDefaultForecast();
      }
    } catch (e) {
      _setDefaultForecast();
    }
  }

  void _setDefaultValues() {
    _nextMonthPrediction = 1200.0;
    _savingsOpportunity = 150.0;
    _topSpendingCategory = 'Food';
    _setDefaultPatterns();
    _setDefaultForecast();
  }

  void _setDefaultPatterns() {
    _spendingPatterns = {
      'daily_patterns': {
        'Monday': 45.0,
        'Tuesday': 38.0,
        'Wednesday': 42.0,
        'Thursday': 55.0,
        'Friday': 68.0,
        'Saturday': 85.0,
        'Sunday': 52.0,
      },
      'category_breakdown': {
        'Food': 450.0,
        'Transport': 200.0,
        'Shopping': 300.0,
        'Entertainment': 150.0,
        'Utilities': 180.0,
      },
      'top_category': 'Food',
    };
    _topSpendingCategory = 'Food';
  }

  void _setDefaultForecast() {
    _weeklyForecast = [
      {'day': 1, 'amount': 45.0},
      {'day': 2, 'amount': 38.0},
      {'day': 3, 'amount': 42.0},
      {'day': 4, 'amount': 55.0},
      {'day': 5, 'amount': 68.0},
      {'day': 6, 'amount': 85.0},
      {'day': 7, 'amount': 52.0},
    ];
  }

  Future<Map<String, dynamic>> getCategoryPrediction(String category) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/predictions/category/$category'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      debugPrint('Error getting category prediction: $e');
    }

    return {
      'category': category,
      'prediction': {
        'predicted_amount': 200.0,
        'confidence': 0.7,
        'trend': 'stable'
      }
    };
  }

  Future<Map<String, dynamic>> getSpendingInsights() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/insights/spending-summary'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      debugPrint('Error getting spending insights: $e');
    }

    return {
      'insights': {
        'category_breakdown': _spendingPatterns['category_breakdown'] ?? {},
        'total_spending': 1285.0,
        'top_category': _topSpendingCategory,
      },
      'recommendations': [
        'Consider reducing food expenses - it\'s your highest spending category',
        'Great job staying within your entertainment budget!',
      ],
    };
  }

  String getSpendingTrend() {
    if (_nextMonthPrediction > 1300) return 'increasing';
    if (_nextMonthPrediction < 1000) return 'decreasing';
    return 'stable';
  }

  Color getTrendColor() {
    switch (getSpendingTrend()) {
      case 'increasing': return const Color(0xFFFF5722);
      case 'decreasing': return const Color(0xFF4CAF50);
      default: return const Color(0xFF2196F3);
    }
  }

  String getTrendIcon() {
    switch (getSpendingTrend()) {
      case 'increasing': return '📈';
      case 'decreasing': return '📉';
      default: return '📊';
    }
  }
}