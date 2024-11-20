from flask import Flask, request, jsonify

app = Flask(__name__)

conversion_rates = {
    "USD": {"USD": 1.0, "EUR": 0.85, "AUD": 1.35, "CAD": 1.25},
    "EUR": {"EUR": 1.0, "USD": 1.18, "AUD": 1.59, "CAD": 1.47},
    "AUD": {"AUD": 1.0, "USD": 0.74, "EUR": 0.63, "CAD": 0.93},
    "CAD": {"CAD": 1.0, "USD": 0.80, "EUR": 0.68, "AUD": 1.08}
}


@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.json
        budgets = data.get("budgets")
        target_currency = data.get("currency")
        source_currency = data.get("source_currency", "USD")
        conversion_rate = conversion_rates[source_currency][target_currency]
        converted_budgets = {}

        for date, budget in budgets.items():
            converted_budget = {}
            for budget_type in ['actual', 'expected']:
                income_key = f"{budget_type}_income"
                expenses_key = f"{budget_type}_expenses"

                income = budget.get(income_key, 0)
                expenses = budget.get(expenses_key, [])

                converted_income = round(income * conversion_rate, 2)

                converted_expenses = []
                for expense in expenses:
                    converted_amount = round(expense["amount"] * conversion_rate, 2)
                    converted_expenses.append({"name": expense["name"], "amount": converted_amount})

                converted_budget[income_key] = converted_income
                converted_budget[expenses_key] = converted_expenses

            converted_budgets[date] = converted_budget

        return jsonify(converted_budgets)

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)