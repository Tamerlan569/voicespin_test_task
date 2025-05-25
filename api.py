from flask import Flask, request, jsonify
from threading import Lock

app = Flask(__name__)

# In-memory storage for numbers
numbers = []
lock = Lock()


@app.route('/numbers', methods=['POST'])
def add_number():
    data = request.get_json()
    number = data.get('number')

    if isinstance(number, int):
        with lock:
            numbers.append(number)
        return jsonify({"message": "Number added"}), 201
    else:
        return jsonify({"error": "Invalid input"}), 400


@app.route('/average', methods=['GET'])
def get_average():
    with lock:
        if not numbers:
            return jsonify({"average": 0.0}), 200
        average = sum(numbers) / len(numbers)
    return jsonify({"average": average}), 200


if __name__ == '__main__':
    app.run(debug=True)
