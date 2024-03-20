from flask import Flask, request,jsonify
import json
from config import conf_analyse_logs as conf_analyse
from config import conf_order_store
from config import BASE_URL
import requests

app = Flask(__name__)


@app.route(conf_analyse.URL_SET, methods=["POST"])
def log_to_orderstore():
    """
    This function logs the order to the order store, if a data element is changed
    :return: JSON response
    """
    form_data_dict = request.form.to_dict()
    if form_data_dict.get("topic") =="dataelements" and form_data_dict.get("event")=="change":
        event = form_data_dict.get("event")
        notification = json.loads(form_data_dict.get("notification"))
        content = notification["content"]
        changed = content["changed"]

        if "order1" in changed:
            index = changed.index("order1")
            order = content["values"][changed[index]]
            id_order = order["order_id"]
            status_order = order["status"]

            data = {
                "id": id_order,
                "status": status_order
            }
            response = requests.post(f"{BASE_URL}{conf_order_store.PORT}{conf_order_store.URL_UPDATE}", json=data)

            # Check if the request was successful
            if response.status_code == 200:
                return jsonify({"message": "Order logged and processed"}), response.status_code
            else:
                return jsonify({"message": "Failed to update order"}), response.status_code


    return jsonify({"message": "Nothing to log"}), 200


if __name__ == "__main__":
    app.run(host="::", port=conf_analyse.PORT, debug=True,threaded=True)


