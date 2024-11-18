from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/sort-budget', methods=['POST'])
def sort_budget():
    data = request.get_json()

    categories = data['categories']

    sorted_categories = sorted(categories, key=lambda x: x['amount'], reverse=True)
    return jsonify({"sorted_categories": sorted_categories})


if __name__ == '__main__':
    app.run(debug=True)
