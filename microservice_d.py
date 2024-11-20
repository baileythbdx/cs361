from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

GOALS_FILE = "savings_goals.json"


def initialize_goals_file():
    if not os.path.exists(GOALS_FILE):
        print("Savings goals file not found. Initializing a new file...")
        save_goals({})
    else:
        try:
            with open(GOALS_FILE, "r") as file:
                json.load(file)
        except json.JSONDecodeError:
            print("Savings goals file is corrupted. Reinitializing the file...")
            save_goals({})


def save_goals(goals):
    with open(GOALS_FILE, "w") as file:
        json.dump(goals, file, indent=4)


def load_goals():
    with open(GOALS_FILE, "r") as file:
        return json.load(file)


initialize_goals_file()
savings_goals = load_goals()


@app.route("/goal/create", methods=["POST"])
def create_goal():
    data = request.get_json()

    goal_name = data.get("goal_name")
    target_amount = data.get("target_amount")
    deadline = data.get("deadline")

    target_amount = float(target_amount)
    deadline = datetime.strptime(deadline, "%Y-%m-%d")

    if goal_name in savings_goals:
        return jsonify({"error": "A goal with this name already exists"})

    savings_goals[goal_name] = {
        "target_amount": target_amount,
        "deadline": deadline.strftime("%Y-%m-%d"),
        "saved_amount": 0.0,
    }
    save_goals(savings_goals)

    return jsonify({"message": f"Savings goal '{goal_name}' created successfully!"})


@app.route("/goal/progress", methods=["GET"])
def view_progress():
    goal_name = request.args.get("goal_name")

    goal = savings_goals.get(goal_name)

    target_amount = goal["target_amount"]
    saved_amount = goal["saved_amount"]
    deadline = datetime.strptime(goal["deadline"], "%Y-%m-%d")
    today = datetime.today()

    remaining_amount = target_amount - saved_amount
    progress_percentage = (saved_amount / target_amount) * 100 if target_amount > 0 else 0

    months_remaining = (deadline.year - today.year) * 12 + (deadline.month - today.month)
    if months_remaining > 0:
        required_monthly_savings = remaining_amount / months_remaining
    else:
        required_monthly_savings = remaining_amount

    return jsonify({
        "goal_name": goal_name,
        "target_amount": target_amount,
        "saved_amount": saved_amount,
        "remaining_amount": max(remaining_amount, 0),
        "progress_percentage": round(progress_percentage, 2),
        "required_monthly_savings": round(required_monthly_savings, 2) if remaining_amount > 0 else 0,
        "deadline": goal["deadline"]
    })


@app.route("/goal/update", methods=["POST"])
def update_goal():
    data = request.get_json()

    goal_name = data.get("goal_name")
    saved_amount = data.get("saved_amount")

    saved_amount = float(saved_amount)

    goal = savings_goals.get(goal_name)

    goal["saved_amount"] += saved_amount
    save_goals(savings_goals)

    return jsonify({"message": f"Saved amount updated for goal '{goal_name}'"})


@app.route("/goal/list", methods=["GET"])
def list_goals():
    return jsonify(savings_goals)


if __name__ == "__main__":
    app.run(port=5003)
