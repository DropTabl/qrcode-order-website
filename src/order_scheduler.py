from flask import Flask, request, jsonify
import queue
import requests
from config import conf_order_sched as conf_order
from config import conf_callback_sched as conf_callback
from config import conf_order_store

from config import BASE_URL

app = Flask(__name__)

order_queue = queue.Queue()
counter_order_id = 0
def get_callback_url():
    """
    Fetches the callback URL from the callback service (if available)
    :return: The callback URL or None if not available
    """
    try:
        callback_get_url = f"{BASE_URL}{conf_callback.PORT}{conf_callback.URL_GET}"
        response = requests.get(callback_get_url)
        if response.status_code == 200:
            callback_data = response.json()
            if 'callback_url' in callback_data:
                return callback_data['callback_url']
            else:
                return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching callback URL: {e}")
        return None

@app.route(conf_order.URL_SET, methods=['POST'])
def set_order():
    """
    Adds a new order to the queue or sends it to the callback URL if available
    :return: A response message and status code
    """
    global counter_order_id
    order_data = request.json
    if not order_data:
        return jsonify({"error": "No order data provided"}), 400

    #Checks the order:
    required_fields = ["drink", "size", "name"]
    if not all(field in order_data for field in required_fields):
        return jsonify({"error": "Missing order details"}), 400

    counter_order_id += 1
    order_data["order_id"] = counter_order_id
    order_data["status"] = "Recieved"
    order_data["recipe_id"] = -1
    order_data["orderbot_id"] = -1
    data = {
        "id": counter_order_id,
        "orderbot_id": "-1",
        "status": "Order Initiated"
    }

    print(f"Add new data to conf_order_store.URL_UPDATE {data}")
    response = requests.put(f"{BASE_URL}{conf_order_store.PORT}{conf_order_store.URL_UPDATE}", json=data)

    callback_url = get_callback_url()
    if callback_url:
        # If a callback URL is available, send a POST request to the callback URL with the order data
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.put(callback_url, json=order_data, headers=headers)
            return jsonify({"message": "Order sent to callback URL","order_id":counter_order_id}), response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error sending POST request: {e}")
            return jsonify({"error": str(e)}), 500
    else:
        order_queue.put(order_data)
        return jsonify({"message": "Order added to the que","order_id":counter_order_id}), 200

@app.route(conf_order.URL_GET, methods=['GET'])
def get_order():
    """
    Fetches the next order from the queue and removes it
    :return: The next order in the queue or a message if the queue is empty
    """
    try:
        order = order_queue.get_nowait()
        return jsonify(order), 200
    except queue.Empty:
        return jsonify({"message": "No orders in the queue"}), 204

@app.route(conf_order.URL_DEBUG, methods=['GET'])
def get_all_orders():
    """
    Fetches all orders from the queue (for debugging purposes)
    :return: A list of all orders in the queue
    """
    with order_queue.mutex:
        all_orders = list(order_queue.queue)
    return jsonify({"all_orders": all_orders}), 200

if __name__ == "__main__":
    app.run(host="::", port=conf_order.PORT,debug=True, threaded=True)