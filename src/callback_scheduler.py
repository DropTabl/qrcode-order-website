from flask import Flask, request, jsonify
from flask import make_response
import queue
import requests
from config import conf_order_sched as conf_order
from config import conf_callback_sched as conf_callback
from config import BASE_URL

app = Flask(__name__)

callback_queue = queue.Queue()

def get_order():
    """
    Fetches an order from the Order Service (if available)
    :return: Order data if available, None otherwise
    """
    try:
        order_get_url = f"{BASE_URL}{conf_order.PORT}{conf_order.URL_GET}"
        response = requests.get(order_get_url)
        if response.status_code == 200:
            order_data = response.json()
            # Check if we received an order or a message indicating no orders are available
            if 'order_id' in order_data:
                return order_data
            else:
                return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Order URL: {e}")
        return None


@app.route(conf_callback.URL_SET, methods=['GET'])
def set_callback():
    """
    Adds a callback to the queue if there are no orders available, otherwise it returns the order data
    :return: Order data if available, message indicating the callback was added to the queue otherwise
    """
    callback_url = request.headers.get('Cpee-Callback')
    if not callback_url:
        return jsonify({"error": "No Cpee-Callback header found"}), 400

    try:
        # Check if there is an order available before adding the callback
        order_data = get_order()
        if order_data:
            return jsonify(order_data), 200

        else:
            # No orders available, add the callback to the queue
            callback_queue.put(callback_url)
            response = make_response(jsonify({"message": "Callback URL added to the queue"}), 200)
            response.headers['CPEE-CALLBACK'] = 'true'
            return response

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route(conf_callback.URL_GET, methods=['GET'])
def get_callback():
    """
    Returns a callback URL from the queue if available and removes it from the queue
    :return: Callback URL if available, message indicating no callbacks available otherwise
    """
    try:
        callback_url = callback_queue.get_nowait()
        return jsonify({"callback_url": callback_url}), 200
    except queue.Empty:
        return jsonify({"message": "There are currently no callbacks available"}), 204

@app.route(conf_callback.URL_DEBUG, methods=['GET'])
def get_all_callbacks():
    """
    Returns all the callbacks currently in the queue (for debugging purposes)
    :return: All the callbacks currently in the queue
    """
    with callback_queue.mutex:  # Thread-safe access to the underlying list
        all_callbacks = list(callback_queue.queue)
    return jsonify({"all_callbacks": all_callbacks}), 200

if __name__ == "__main__":
    app.run(host="::", port=conf_callback.PORT,debug=True, threaded=True)