from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


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
    monthly_details = {}

    for month, budget in budgets.items():
        try:
            month_date = datetime.strptime(month, "%Y-%m")
        except ValueError:
            continue

        if start_date_obj <= month_date <= end_date_obj:
            actual_income = budget.get("actual_income", 0)
            expected_income = budget.get("expected_income", 0)
            monthly_income_diff = actual_income - expected_income
            aggregated_income_diff += monthly_income_diff

            actual_expenses = budget.get("actual_expenses", [])
            expected_expenses = budget.get("expected_expenses", [])

            monthly_category_diff = {}

            for expected_item in expected_expenses:
                category = expected_item["name"]
                actual_item = next((e for e in actual_expenses if e["name"] == expected_item["name"]), None)
                actual_amount = actual_item["amount"] if actual_item else 0
                difference = actual_amount - expected_item["amount"]

                # Track trends for the category
                if category not in category_trends:
                    category_trends[category] = {"total_overspend": 0, "total_underspend": 0, "overspend_months": 0,
                                                 "underspend_months": 0}

                if difference > 0:
                    category_trends[category]["total_overspend"] += difference
                    category_trends[category]["overspend_months"] += 1
                elif difference < 0:
                    category_trends[category]["total_underspend"] += abs(difference)
                    category_trends[category]["underspend_months"] += 1

                monthly_category_diff[category] = {
                    "expected": expected_item["amount"],
                    "actual": actual_amount,
                    "difference": difference,
                    "status": "overspending" if difference > 0 else "underspending" if difference < 0 else "on-budget"
                }

            monthly_details[month] = {
                "income_difference": monthly_income_diff,
                "category_details": monthly_category_diff
            }

    if aggregated_income_diff > 0:
        income_message = f"(You earned ${aggregated_income_diff:.2f} more than expected in total.)"
    elif aggregated_income_diff < 0:
        income_message = f"(You earned ${abs(aggregated_income_diff):.2f} less than expected in total.)"
    else:
        income_message = "(Your earnings matched your expectations.)"

    category_messages = []
    for category, trends in category_trends.items():
        net_difference = trends["total_overspend"] - trends["total_underspend"]
        if net_difference > 0:
            category_messages.append(
                f"{category}: Overspent ${net_difference:.2f} overall ({trends['overspend_months']} months)."
            )
        elif net_difference < 0:
            category_messages.append(
                f"{category}: Underspent ${abs(net_difference):.2f} overall ({trends['underspend_months']} months)."
            )
        else:
            category_messages.append(f"{category}: Stayed on budget overall.")

    return jsonify({
        "income_difference": aggregated_income_diff,
        "income_message": income_message,
        "category_trends": category_trends,
        "category_messages": category_messages,
        "monthly_details": monthly_details
    })


if __name__ == "__main__":
    app.run(port=5002)
