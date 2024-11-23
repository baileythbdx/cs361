from flask import Flask, request, jsonify

app = Flask(__name__)

conversion_rates = {
    "USD": {"USD": 1.0, "EUR": 0.85, "AUD": 1.35, "CAD": 1.25},
    "EUR": {"EUR": 1.0, "USD": 1.18, "AUD": 1.59, "CAD": 1.47},
    "AUD": {"AUD": 1.0, "USD": 0.74, "EUR": 0.63, "CAD": 0.93},
    "CAD": {"CAD": 1.0, "USD": 0.80, "EUR": 0.68, "AUD": 1.08}
}


def calculate_converted_amount(amount, conversion_rate):
    return round(amount * conversion_rate, 2)


def convert_budget(budget, conversion_rate):
    return {
        "actual_income": calculate_converted_amount(budget.get("actual_income", 0), conversion_rate),
        "actual_expenses": [
            {"name": expense["name"], "amount": calculate_converted_amount(expense["amount"], conversion_rate)}
            for expense in budget.get("actual_expenses", [])
        ],
        "expected_income": calculate_converted_amount(budget.get("expected_income", 0), conversion_rate),
        "expected_expenses": [
            {"name": expense["name"], "amount": calculate_converted_amount(expense["amount"], conversion_rate)}
            for expense in budget.get("expected_expenses", [])
        ]
    }


@app.route("/convert", methods=["POST"])
def convert():
    data = request.json
    budgets = data.get("budgets", {})
    target_currency = data.get("currency")
    source_currency = data.get("source_currency", "USD")

    conversion_rate = conversion_rates[source_currency][target_currency]
    converted_budgets = {date: convert_budget(budget, conversion_rate) for date, budget in budgets.items()}

    return jsonify(converted_budgets)


if __name__ == "__main__":
    app.run(port=5000)