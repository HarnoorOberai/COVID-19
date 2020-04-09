import requests
from flask import Flask, request, jsonify
import requests_cache
from cassandra.cluster import Cluster

# cluster = Cluster(contact_points=['172.17.0.2'], port=9042)
cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
session = cluster.connect()

requests_cache.install_cache('conv19', backend='sqlite', expire_after=36000)

SUMMARY_JSON = {}
GLOBAL_JSON = {}
COUNTRIES_JSON = {}

app = Flask(__name__)


@app.route('/')
def hello():
    return ('<h1>Welcome Conv19 API</h1>')


# make call to external API
@app.route('/summary', methods=['GET'])
def get_conv19_summary():
    url = "https://api.covid19api.com/summary"
    headers = {}
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.ok:
        SUMMARY_JSON = response.json()
        return SUMMARY_JSON
    else:
        print(response.reason)


@app.route('/summary/global', methods=['GET'])
def get_conv19_summaryGlobalCount():
    url = "https://api.covid19api.com/summary"
    headers = {}
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.ok:
        SUMMARY_JSON = response.json()
        GLOBAL_JSON = SUMMARY_JSON["Global"]
        return GLOBAL_JSON
    else:
        print(response.reason)


@app.route('/summary/country', methods=['GET'])
def get_conv19_summaryAllCountryCount():
    url = "https://api.covid19api.com/summary"
    headers = {}
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.ok:
        SUMMARY_JSON = response.json()
        COUNTRIES_JSON = {"Countries": SUMMARY_JSON["Countries"]}
        return COUNTRIES_JSON
    else:
        print(response.ok)


@app.route('/summary/country/<name>', methods=['GET'])
def get_conv19_summaryByCountry(name):
    print(""" SELECT * FROM conv19.Country where Country = '{}'""".format(name))
    rows = session.execute(""" SELECT * FROM conv19.Country where Country = '{}'""".format(name))
    result = []
    for r in rows:
        result.append(
            {
                'Country': r.country,
                'CountryCode': r.countrycode,
                'Date': r.date,
                'NewConfirmed': r.newconfirmed,
                'NewDeaths': r.newdeaths,
                'NewRecovered': r.newrecovered,
                'Slug': r.slug,
                'TotalConfirmed': r.totalconfirmed,
                'TotalDeaths': r.totaldeaths,
                'TotalRecovered': r.totalrecovered
            }
        )
    if len(result) == 0:
        return '<h1>Check spelling!!!</h1>'
    return jsonify(result)






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
