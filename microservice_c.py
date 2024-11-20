from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


@app.route("/compare/month", methods=["POST"])
def compare_month():
    data = request.get_json()
    month = data.get("month")
    budgets = data.get("budgets")

    if not month or not budgets:
        return jsonify({"error": "Invalid input. 'month' and 'budgets' are required."}), 400

    budget = budgets.get(month)
    if not budget:
        return jsonify({"error": f"No budget data found for month {month}."}), 404

    actual_income = budget.get("actual_income", 0)
    expected_income = budget.get("expected_income", 0)
    actual_expenses = budget.get("actual_expenses", [])
    expected_expenses = budget.get("expected_expenses", [])

    income_difference = actual_income - expected_income

    expense_comparison = []
    for expected_item in expected_expenses:
        actual_item = next((e for e in actual_expenses if e["name"] == expected_item["name"]), None)
        actual_amount = actual_item["amount"] if actual_item else 0
        difference = actual_amount - expected_item["amount"]
        expense_comparison.append({
            "category": expected_item["name"],
            "expected": expected_item["amount"],
            "actual": actual_amount,
            "difference": difference,
            "status": "overspending" if difference > 0 else "underspending" if difference < 0 else "on-budget"
        })

    return jsonify({
        "month": month,
        "income_difference": income_difference,
        "expense_comparison": expense_comparison
    })


@app.route("/compare/range", methods=["POST"])
def compare_range():
    data = request.get_json()
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    budgets = data.get("budgets")

    if not start_date or not end_date or not budgets:
        return jsonify({"error": "Invalid input. 'start_date', 'end_date', and 'budgets' are required."}), 400

    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m")
        end_date_obj = datetime.strptime(end_date, "%Y-%m")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM for 'start_date' and 'end_date'."}), 400

    aggregated_income_diff = 0
    category_trends = {}

    for month, budget in budgets.items():
        try:
            month_date = datetime.strptime(month, "%Y-%m")
        except ValueError:
            continue  # Skip invalid dates

        if start_date_obj <= month_date <= end_date_obj:
            actual_income = budget.get("actual_income", 0)
            expected_income = budget.get("expected_income", 0)
            aggregated_income_diff += (actual_income - expected_income)

            actual_expenses = budget.get("actual_expenses", [])
            expected_expenses = budget.get("expected_expenses", [])

            for expected_item in expected_expenses:
                category = expected_item["name"]
                actual_item = next((e for e in actual_expenses if e["name"] == expected_item["name"]), None)
                actual_amount = actual_item["amount"] if actual_item else 0
                difference = actual_amount - expected_item["amount"]

                if category not in category_trends:
                    category_trends[category] = {"total_overspend": 0, "total_underspend": 0}

                if difference > 0:
                    category_trends[category]["total_overspend"] += difference
                elif difference < 0:
                    category_trends[category]["total_underspend"] += abs(difference)

    return jsonify({
        "income_difference": aggregated_income_diff,
        "category_trends": category_trends
    })


if __name__ == "__main__":
    app.run(port=5002)
