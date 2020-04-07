import requests
from flask import Flask

app = Flask(__name__)
@app.route('/')
def hello():
    return('<h1>Hello World!</h1>')

# make call to external API
@app.route('/summary', methods=['GET'])
def get_conv19_summary():
    url = "https://api.covid19api.com/summary"
    headers ={}
    payload ={}
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json()



if __name__ == '__main__':
    app.run(host='0.0.0.0')