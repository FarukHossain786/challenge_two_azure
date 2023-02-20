from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from challenge_two_azure import Totalvideos, Details


application = Flask(__name__)
app=application

@app.route('/')
@cross_origin()
def index():
    if not request.args.get('find'):
        response = ''
        return render_template('index.html', response = response)
    else: 
        obj = Totalvideos.Totalvideos()
        response = obj.videos()
        return render_template('index.html', response = response)

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        url = request.form.get('content')
        obj = Details.Details()
        details = obj.get_details(url)
        return render_template("results.html", response = details)

    return "Method not accepted!"

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
	#app.run(debug=True)
