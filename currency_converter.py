import requests


def microservice_bailey_test():
    url = "http://127.0.0.1:5000/convert"
    data = {
        "budgets": {
            "USD": 100,
            "EUR": 200
        },
        "currency": "AUD"
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"error: {response.status_code}")


if __name__ == "__main__":
    microservice_bailey_test()