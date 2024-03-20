from flask import Flask, render_template,request,jsonify
import requests
import qrcode
from io import BytesIO
import base64
import json

from config import BASE_URL
from config import conf_link_creation as conf_link_create
from config import conf_static_website as cond_static_web
from urllib.parse import urlparse, parse_qs
import pyttsx3

app = Flask(__name__,template_folder='/home/students/ge56qon/Project/Project/HTML')
shoutout_messages = []

links = {}
def get_drink_data():
    """
    This function is used to get the links for the drinks
    :return: The links for the drinks
    """
    url_avail_urls = f"{BASE_URL}{conf_link_create.PORT}{conf_link_create.URL_GET}"
    response = requests.get(url_avail_urls)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def speak(text):
    """
    This function is used to speak a given text
    :param text: The text to speak
    :return: None
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.route("/shoutout", methods=['PUT'])
def shoutout():
    """
    This function is used to set the shoutout message
    :return: A message that the shoutout message has been set
    """
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        form = request.form
        drink = form['drink']
        name = form['name']
        order_id = form['order_id']
        shoutout_message = f"{drink} with ID: {order_id} is ready, please pick it up"
        #speak(shoutout_message)
        shoutout_messages.append(shoutout_message)
        return jsonify({"message": "Text spoken successfully"}), 200

    data = request.data.decode("utf-8")
    speak(data)
    return jsonify({"message": "Text spoken successfully"}), 200

@app.route("/shoutout_get", methods=['GET'])
def shoutout_get():
    """
    This function is used to get the shoutout message
    :return: The shoutout message
    """
    if len(shoutout_messages)>0:
        shoutout_message = shoutout_messages.pop()
        return jsonify({"message": shoutout_message}), 200
    else:
        return jsonify({"message": ""}), 200





@app.route("/links", methods=['PUT'])
def set_drink_data():
    """
    This function is used to set the links for the drinks
    :return: A message that the links have been set
    """
    global links
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        form = request.form["URLs"]
        links = json.loads(form)
        print(links)
        return jsonify({"message": "URLS added successfully"}), 200


def generate_qr_code(link):
    """
    This function is used to generate a qr code from a given link
    :param link: The link to generate the qr code from
    :return: The qr code as a base64 encoded string
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


@app.route('/')
def index():
    """
    This function is used to render the index.html file and generate qr codes for the drinks
    :return: The index.html file with the qr codes
    """
    global links
    drinks = links
    for drink in drinks:
        drink['qr_code'] = generate_qr_code(drink['link'])


    return render_template('index.html', drinks=drinks)



#[{'drink': 'Gin Tonic', 'link': 'https://lehre.bpm.in.tum.de/ports/8122/OMS/?drink=Gin%20Tonic', 'qr_code': '/9j

if __name__ == '__main__':
    app.run(host="::",port=cond_static_web.PORT,debug=True)
