import requests
from flask import Flask
import requests_cache
requests_cache.install_cache('conv19', backend='sqlite', expire_after=36000)

SUMMARY_JSON = {}
GLOBAL_JSON = {}
COUNTRIES_JSON = {}

app = Flask(__name__)
@app.route('/')
def hello():
    return('<h1>Welcome Conv19 API</h1>')

# make call to external API
@app.route('/summary', methods=['GET'])
def get_conv19_summary():
    url = "https://api.covid19api.com/summary"
    headers ={}
    payload ={}
    response = requests.request("GET", url, headers=headers, data = payload)
    SUMMARY_JSON = response.json()
    return SUMMARY_JSON

@app.route('/summary/global', methods=['GET'])
def get_conv19_summaryGlobal():
    url = "https://api.covid19api.com/summary"
    headers ={}
    payload ={}
    response = requests.request("GET", url, headers=headers, data = payload)
    SUMMARY_JSON = response.json()
    GLOBAL_JSON = SUMMARY_JSON["Global"]
    return GLOBAL_JSON

@app.route('/summary/country', methods=['GET'])
def get_conv19_summaryByCountry():
    url = "https://api.covid19api.com/summary"
    headers ={}
    payload ={}
    response = requests.request("GET", url, headers=headers, data = payload)
    SUMMARY_JSON = response.json()
    COUNTRIES_JSON = {"Countries" : SUMMARY_JSON["Countries"]}
    return COUNTRIES_JSON


if __name__ == '__main__':
    app.run(host='0.0.0.0')