from flask import Flask, request, jsonify
import threading
from config import conf_order_store
import json


app = Flask(__name__)

lock = threading.Lock()

orders = {}

@app.route(conf_order_store.URL_GET, methods=['GET'])
def get_order_status(id):
    """
    Get the status of an order
    :param id: The order id
    :return: The status of the order
    """
    with lock:
        order = orders.get(id)
    if order:
        return jsonify(order), 200
    else:
        return jsonify({"error": "Order not found"}), 404

@app.route(conf_order_store.URL_UPDATE, methods=['PUT'])
def update_order():
    """
    Update the status of an order, given the order id, orderbot_id and the new status (in the request body)
    :return: A message indicating the status of the update
    """
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        form = request.form
        orderbot_id = form['orderbot_id']
        order_id = form['order_id']
        status = form['status']
        order = {
            'orderbot_id': orderbot_id,
            'status': status
        }
        with lock:
            orders[int(order_id)] = order



    else:
        data = request.json
        if not data or 'id' not in data or 'status' not in data:
            return jsonify({"error": "Missing data"}), 400

        id = data['id']
        old_status = data['status']

        #Since the last action was not ACK with OK there is a Problem with this Order
        #if old_status != "OK" and data['status']!= "OK":
        #    return jsonify({"message": "Order has an issue"}), 400


        order = {
            'status': data['status'],
            'orderbot_id':data["orderbot_id"]
        }

        with lock:
            orders[id] = order
    return jsonify({"message": "Order updated"}), 200

@app.route(conf_order_store.URL_GET_ALL, methods=['GET'])
def get_all():
    """
    Get all the orders (for debugging purposes)
    :return: A list of all the orders
    """
    with lock:
        res = orders
        return jsonify(res), 200
    return jsonify({"message": "Lock not aquired"}), 200


@app.route(conf_order_store.URL_GET_CURRENT, methods=['GET'])
def get_current_order():
    """
    Get the current orders that are not served yet
    :return: A list of the current orders
    """
    with lock:
        incomplete_orders = []
        for id in orders:
            if orders[id]["status"] != "Order Served" and orders[id]["status"] != "Order Initiated":
                current_order = {
                    "id": id,
                    "orderbot_id": orders[id]["orderbot_id"],
                    "status": orders[id]["status"]
                }
                incomplete_orders.append(current_order)


        return jsonify({"incomplete_orders": incomplete_orders}), 200


@app.route(conf_order_store.URL_GET_COMPLETED, methods=['GET'])
def get_completed_orders():
    """
    Get the orders that have been served
    :return: A list of the completed orders
    """
    completed_orders = []
    with lock:
        for id in orders:
            if orders[id]["status"]== "Order Served":
               completed_orders.append(id)

    return jsonify({"completed_orders": completed_orders}), 200

@app.route(conf_order_store.URL_GET_NEW, methods=['GET'])
def get_new_orders():
    """
    Get the orders that have been initiated but not served and not yet started
    :return: A list of the new orders
    """
    new_orders = []
    with lock:
        for id in orders:
            if orders[id]["status"]== "Order Initiated":
               new_orders.append(id)

    return jsonify({"new_orders": new_orders}), 200


if __name__ == '__main__':
    app.run(debug=True,host="::",port=conf_order_store.PORT,threaded=True)