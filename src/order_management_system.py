from flask import Flask, request
import requests

from config import BASE_URL
from config import conf_order_sched as conf_order
from config import conf_callback_sched as conf_callback
from config import conf_static_oms as conf_oms

app = Flask(__name__)

@app.route(conf_oms.URL_SET, methods=['GET'])
def oms():
    """
    This function is used to send a drink to the order scheduler by scanning a qr code first and then sending the drink to the order scheduler
    :return: A message that the drink is being prepared and the order number
    """
    drink = request.args.get('drink', default=None, type=str)
    headers = {'Content-Type': 'application/json'}
    url_order_set = f"{BASE_URL}{conf_order.PORT}{conf_order.URL_SET}"
    drink_json = {
        "drink": drink,
        "size": "Large",
        "name": "Static"
    }

    if drink:
        response = requests.post(url_order_set, json=drink_json, headers=headers)
        if response.status_code == 200:
            data = response.json()
            order_number = data.get('order_id')

            return f'Preparing {drink} \n <br> Ordernumber {order_number}', 200
        else:
            return "Failed to get a successful response", 400

    else:
        return 'Please specify a drink.', 400

if __name__ == '__main__':
    app.run(host='::', port=conf_oms.PORT, debug=True,threaded=True)
