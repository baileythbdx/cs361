from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# File to store savings goals
GOALS_FILE = "savings_goals.json"

# Function to initialize the savings goals file
def initialize_goals_file():
    if not os.path.exists(GOALS_FILE):  # Check if the file exists
        print("Savings goals file not found. Initializing a new file...")
        save_goals({})  # Create an empty file with default content
    else:
        try:
            with open(GOALS_FILE, "r") as file:
                json.load(file)  # Try to load the file
        except json.JSONDecodeError:
            print("Savings goals file is corrupted. Reinitializing the file...")
            save_goals({})  # Reset the file if it's corrupted

# Save function to write the goals data to the file
def save_goals(goals):
    with open(GOALS_FILE, "w") as file:
        json.dump(goals, file, indent=4)

# Load function to retrieve goals data from the file
def load_goals():
    with open(GOALS_FILE, "r") as file:
        return json.load(file)

# Initialize the file at the start of the microservice
initialize_goals_file()
savings_goals = load_goals()

# Route to create a new savings goal
@app.route("/goal/create", methods=["POST"])
def create_goal():
    data = request.get_json()

    goal_name = data.get("goal_name")
    target_amount = data.get("target_amount")
    deadline = data.get("deadline")

    if not goal_name or not target_amount or not deadline:
        return jsonify({"error": "Goal name, target amount, and deadline are required"}), 400

    try:
        target_amount = float(target_amount)
        deadline = datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid target amount or deadline format"}), 400

    if goal_name in savings_goals:
        return jsonify({"error": "A goal with this name already exists"}), 400

    savings_goals[goal_name] = {
        "target_amount": target_amount,
        "deadline": deadline.strftime("%Y-%m-%d"),
        "saved_amount": 0.0,
    }
    save_goals(savings_goals)

    return jsonify({"message": f"Savings goal '{goal_name}' created successfully!"}), 201

# Route to view progress on a specific savings goal
@app.route("/goal/progress", methods=["GET"])
def view_progress():
    goal_name = request.args.get("goal_name")

    if not goal_name:
        return jsonify({"error": "Goal name is required"}), 400

    goal = savings_goals.get(goal_name)
    if not goal:
        return jsonify({"error": f"No savings goal found with the name '{goal_name}'"}), 404

    target_amount = goal["target_amount"]
    saved_amount = goal["saved_amount"]
    deadline = datetime.strptime(goal["deadline"], "%Y-%m-%d")
    today = datetime.today()

    remaining_amount = target_amount - saved_amount
    progress_percentage = (saved_amount / target_amount) * 100 if target_amount > 0 else 0

    # Calculate required monthly savings
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
    }), 200

# Route to update the saved amount for a goal
@app.route("/goal/update", methods=["POST"])
def update_goal():
    data = request.get_json()

    goal_name = data.get("goal_name")
    saved_amount = data.get("saved_amount")

    if not goal_name or saved_amount is None:
        return jsonify({"error": "Goal name and saved amount are required"}), 400

    try:
        saved_amount = float(saved_amount)
    except ValueError:
        return jsonify({"error": "Invalid saved amount"}), 400

    goal = savings_goals.get(goal_name)
    if not goal:
        return jsonify({"error": f"No savings goal found with the name '{goal_name}'"}), 404

    goal["saved_amount"] += saved_amount
    save_goals(savings_goals)

    return jsonify({"message": f"Saved amount updated for goal '{goal_name}'"}), 200

# Route to list all savings goals
@app.route("/goal/list", methods=["GET"])
def list_goals():
    return jsonify(savings_goals), 200

if __name__ == "__main__":
    app.run(port=5004)