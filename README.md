A. The program should send an HTTP post request to request that the microservice sort the categories.


Example call:

url = "http://127.0.0.1:5000/sort-budget"
data = {
    "categories": [
        {"name": "Rent", "amount": 1500},
        {"name": "Groceries", "amount": 500},
        {"name": "Entertainment", "amount": 200}
    ]
}
response = requests.post(url, json=data)


B. The server responds with JSON file containing the sorted categories.


Example call:

response = requests.post(url, json=data)
if response.status_code == 200:
    sorted_categories = response.json().get('sorted_categories', [])
    for category in sorted_categories:
        print(f"{category['name']}: ${category['amount']}")


C. UML Sequence Diagram

+-------------------+        +--------------------+        +-------------------+
| Main Program      |        | Microservice       |        | Server Logic      |
+-------------------+        +--------------------+        +-------------------+
       |                           |                               |
       | POST request for sorted   |                               |
       |    budget                 |                               |
       |-------------------------->|                               |
       |                           |                               |
       |                           | processRequest()              |
       |                           |------------------------------>|
       |                           |                               |
       |                           | Sort data (descending)        |
       |                           |<------------------------------|
       |                           |                               |
       | Return sorted JSON        |                               |
       |<--------------------------|                               |
       |                           |                               |
       | Parse and display data    |                               |
       |---------------------------------------------------------->|

