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
    data = request.json
    budgets = data.get("budgets", {})
    target_currency = data.get("currency")
    source_currency = data.get("source_currency", "USD")

    conversion_rate = conversion_rates[source_currency][target_currency]
    converted_budgets = {}

    for date, budget in budgets.items():
        converted_budget = {}

        for budget_type in ["actual", "expected"]:
            income = budget.get(f"{budget_type}_income", 0)
            expenses = budget.get(f"{budget_type}_expenses", [])

            converted_income = round(income * conversion_rate, 2)

            converted_expenses = [
                {"name": expense["name"], "amount": round(expense["amount"] * conversion_rate, 2)}
                for expense in expenses
            ]

            converted_budget[f"{budget_type}_income"] = converted_income
            converted_budget[f"{budget_type}_expenses"] = converted_expenses

        converted_budgets[date] = converted_budget

    return jsonify(converted_budgets)


if __name__ == "__main__":
    app.run(port=5000)
