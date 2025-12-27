class Expense {
  final int id;
  final String description;
  final double amount;
  final String category;
  final DateTime date;
  final String? aiCategory;
  final double? aiConfidence;
  final String? paymentMethod;
  final String? location;
  final String? notes;

  Expense({
    required this.id,
    required this.description,
    required this.amount,
    required this.category,
    required this.date,
    this.aiCategory,
    this.aiConfidence,
    this.paymentMethod,
    this.location,
    this.notes,
  });

  factory Expense.fromJson(Map<String, dynamic> json) {
    return Expense(
      id: json['id'],
      description: json['description'],
      amount: json['amount'].toDouble(),
      category: json['category'],
      date: DateTime.parse(json['date']),
      aiCategory: json['ai_category'],
      aiConfidence: json['ai_confidence']?.toDouble(),
      paymentMethod: json['payment_method'],
      location: json['location'],
      notes: json['notes'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'description': description,
      'amount': amount,
      'category': category,
      'date': date.toIso8601String(),
      'ai_category': aiCategory,
      'ai_confidence': aiConfidence,
      'payment_method': paymentMethod,
      'location': location,
      'notes': notes,
    };
  }

  bool get isAICategorized => aiCategory != null && aiConfidence != null;
  
  bool get isHighConfidence => (aiConfidence ?? 0) > 0.8;
  
  String get formattedAmount => '\$${amount.toStringAsFixed(2)}';
  
  String get formattedDate {
    final now = DateTime.now();
    final difference = now.difference(date).inDays;
    
    if (difference == 0) return 'Today';
    if (difference == 1) return 'Yesterday';
    if (difference < 7) return '${difference} days ago';
    
    return '${date.day}/${date.month}/${date.year}';
  }
}