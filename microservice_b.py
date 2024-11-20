from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/monthly_summary", methods=["POST"])
def monthly_summary():
    data = request.get_json()

    month = data.get("month")
    budgets = data.get("budgets")

    budget = budgets[month]

    actual_income = budget.get("actual_income", 0)
    actual_expenses = budget.get("actual_expenses", [])
    expected_expenses = budget.get("expected_expenses", [])

    total_expenses = sum(expense["amount"] for expense in actual_expenses)
    remaining_balance = actual_income - total_expenses

    overspending_categories = []
    expected_dict = {e["name"]: e["amount"] for e in expected_expenses}

    for actual in actual_expenses:
        name, amount = actual["name"], actual["amount"]
        if name in expected_dict and amount > expected_dict[name]:
            overspending_categories.append({
                "category": name,
                "actual_spent": amount,
                "expected_budget": expected_dict[name],
                "overspend": amount - expected_dict[name],
            })

    summary = {
        "month": month,
        "total_income": actual_income,
        "total_expenses": total_expenses,
        "remaining_balance": remaining_balance,
        "overspending_categories": overspending_categories,
    }

    return jsonify(summary), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)