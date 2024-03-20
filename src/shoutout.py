from flask import Flask, request, jsonify
from config import conf_shoutout as conf_shout
import json
import time

app = Flask(__name__)

@app.route(conf_shout.URL_SET, methods=['POST'])
def complete_order():
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        order_id = request.form["order_id"]
        order_name = request.form["name"]
        drink_name = request.form["drink"]

        #TODO ESP32 SOUND
        print(f"HELLO {order_name}, your {drink_name} with order number {order_id} is ready for you to pick up")
        time.sleep(4)


        return jsonify({"message": f"Completed shoutout {order_id} successfully"}), 200
    return jsonify({"message": "Something went wrong while shouting out"}), 400


if __name__ == '__main__':
    app.run(host="::",port=conf_shout.PORT,debug=True, threaded=True)