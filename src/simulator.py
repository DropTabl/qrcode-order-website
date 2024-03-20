from flask import Flask, request, jsonify
from config import conf_process_ingredients as conf_porc_ing
import json
import time

app = Flask(__name__)


# Toy function to simulate consuming an ingredient
def consume(item, amount):
    """
    Simulate consuming an ingredient
    :param item: The ingredient to consume
    :param amount: The amount of the ingredient to consume
    :return: None
    """
    print(f"Consuming {amount} grams of {item}")
    time.sleep(3)


def mix(technique, strength, duration):
    """
    Simulate mixing a drink
    :param technique: The technique to mix the drink
    :param strength: The strength of the mix
    :param duration: The duration of the mix
    :return: None
    """
    print(f"{technique}ing drink with strength {strength} for {duration} seconds")
    time.sleep(duration)

def serve(drink):
    """
    Simulate serving a drink
    :param drink: The drink to serve
    :return: None
    """
    print(f"Serving drink: {drink}")
    time.sleep(5)

@app.route(conf_porc_ing.URL_PUMP, methods=['POST'])
def pump_liquid():
    """
    Process the ingredients for a cocktail, consuming the liquor and non-alcohol ingredients
    :return: A JSON response with a message indicating the ingredients were processed successfully
    """
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        form = request.form
        data = {"liquor": json.loads(form["liquor"]), "non_alcohol": json.loads(form["non_alcohol"])}


    else:
        data = request.json
    if not data or 'liquor' not in data or 'non_alcohol' not in data:
        return jsonify({"error": "Invalid request, missing 'Liquor' or 'Non_alcohol'"}), 400

    # Process Liquor ingredients
    for liquor in data['liquor']:

        item = liquor['name']
        amount = liquor['amount_grams']
        consume(item, amount)

    # Process Non_alcohol ingredients
    for non_alcohol in data['non_alcohol']:
        item = non_alcohol['name']
        amount = non_alcohol['amount_grams']
        consume(item, amount)


    return jsonify({"message": "Ingredients processed successfully"}), 200

@app.route(conf_porc_ing.URL_PROCESS, methods=['POST'])
def process_ingredient():
    """
    Process the other ingredients for a cocktail, consuming the other ingredients
    :return: A JSON response with a message indicating the other ingredients were processed successfully
    """
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        form = request.form
        data = {"other": json.loads(form["other"])}

    else:
        data = request.json
    if not data or 'other' not in data:
        return jsonify({"error": "Invalid request, missing 'Other'"}), 400

    # Process Other ingredients
    for other in data['other']:
        item = other['name']
        amount = other['amount_grams']
        consume(item, amount)

    return jsonify({"message": "Other ingredients processed successfully"}), 200


@app.route(conf_porc_ing.URL_MIX, methods=['POST'])
def mix_ingredients():
    """
    Mix the ingredients for a cocktail
    :return: A JSON response with a message indicating the cocktail was mixed successfully
    """
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        form = request.form

        print(form)
        data = json.loads(form["mix_technique"])
        print(f"DATA{data}")
    else:
        data = request.json
    if not data or ('duration' not in data and 'strength' not in data and 'technique' not in data):
        return jsonify({"error": "Invalid request, missing 'Other'"}), 400

    mix(data["technique"],data["strength"],data["duration"])

    return jsonify({"message": "Mixed cocktail successfully"}), 200


@app.route(conf_porc_ing.URL_SERVE, methods=['POST'])
def serve_cocktail():
    """
    Serve the cocktail
    :return: A JSON response with a message indicating the cocktail was served successfully
    """
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        drink = request.form["drink"]


        serve(drink)

        return jsonify({"message": f"Served Cocktail {drink} successfully"}), 200
    return jsonify({"message": "Something went wrong while mixing"}), 400

@app.route(conf_porc_ing.URL_COMPLETE, methods=['POST'])
def complete_order():
    """
    Complete the order
    :return: A JSON response with a message indicating the order was completed successfully
    """
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        order_id = request.form["order_id"]

        return jsonify({"message": f"Completed order {order_id} successfully"}), 200
    return jsonify({"message": "Something went wrong while completing"}), 400




if __name__ == '__main__':
    app.run(host="::",port=conf_porc_ing.PORT,debug=True, threaded=True)