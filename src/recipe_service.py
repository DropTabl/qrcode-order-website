from flask import Flask, request, jsonify
import json
from config import conf_querry_recepie as conf_recepie
import requests
import time

app = Flask(__name__)


@app.route(conf_recepie.URL_GET, methods=['GET'])
def get_ingredients():
    """
    Get ingredients for a cocktail
    :return: JSON with ingredients
    """
    time.sleep(3)
    cocktail_name = request.args.get('cocktail')
    try:
        response = requests.get(conf_recepie.RECEPIE_PATH)
        if response.status_code == 200:
            cocktails_data = response.json()
            cocktails = cocktails_data.get('cocktails', [])

            for cocktail in cocktails:
                if cocktail['name'].lower() == cocktail_name.lower():
                    return jsonify(cocktail), 200

            return jsonify({"error": "Cocktail not found"}), 404
        else:
            return jsonify({"error": "Failed to fetch cocktails data"}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Server error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host="::", port=conf_recepie.PORT, debug=True)
