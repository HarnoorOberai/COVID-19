import requests
from flask import Flask, request, jsonify, make_response, abort, render_template
import requests_cache
from cassandra.cluster import Cluster
import datetime
from helpfulFunction import *

# cluster = Cluster(contact_points=['172.17.0.2'], port=9042)
cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
session = cluster.connect()

requests_cache.install_cache('conv19', backend='sqlite', expire_after=36000)

SUMMARY_JSON = {}
GLOBAL_JSON = {}
COUNTRIES_JSON = {}

app = Flask(__name__)


# Inital call
@app.route('/')
def hello():
    return render_template("index.html", content_year="2020")


# External API call
# Summary information : Includes country stats and global stats
@app.route('/summary', methods=['GET'])
def get_conv19_summary():
    url = "https://api.covid19api.com/summary"
    headers = {}
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.ok:
        global SUMMARY_JSON
        SUMMARY_JSON = response.json()
        return SUMMARY_JSON
    else:
        print(response.reason)


# External API call
# Summary about Total Global Stats
@app.route('/summary/globalByExternalAPI', methods=['GET'])
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


# All the Countries Stats
# External API Call : GET
@app.route('/summary/countryByExternalAPI', methods=['GET'])
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

# All global stats using Cassandra db
@app.route('/summary/globalByBrowser', methods=['GET'])
def get_conv19_Browser_summaryGlobalCount():
    rows = session.execute(""" SELECT * FROM conv19.global where id = 1 """)
    r = rows.one()
    result = []

    result.append(
        {
            "NewConfirmed": r.newconfirmed,
            "NewDeaths": r.newdeaths,
            "NewRecovered": r.newrecovered,
            "TotalConfirmed": r.totalconfirmed,
            "TotalDeaths": r.totaldeaths,
            "TotalRecovered": r.totalrecovered
        })
    if len(result) == 0:
        abort(404, description="No such country or check country spellings")

    return render_template("GlobalStats.html", GLOBAL_JSON=result)


# All countries list Using Cassandra Db
@app.route('/summary/countryByBrowser', methods=['GET'])
def get_conv19_Browser_summaryAllCountryCount():
    rows = session.execute(""" SELECT * FROM conv19.Country""")
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
        abort(404, description="No such country or check country spellings")

    return render_template("CountriesStats.html", COUNTRIES_JSON=result)


# Specific Country Stats
@app.route('/summary/country/<name>', methods=['GET'])
def get_conv19_summaryByCountry(name):
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
        abort(404, description="No such country or check country spellings")
    return jsonify(result), 200

@app.route('/curlCommands')
def curlCommands():
    return render_template("curlCommands.html")

# Adding a Country as Post Request
# request json of type
# Country,
# CountryCode,
# Date,
# NewConfirmed,
# NewDeaths,
# NewRecovered,
# slug,
# TotalConfirmed,
# TotalDeaths,
# TotalRecovered
@app.route('/summary/country', methods=['POST'])
def addCountry():
    if not request.json or not 'Country' in request.json \
            or not 'CountryCode' in request.json \
            or not 'NewConfirmed' in request.json \
            or not 'NewDeaths' in request.json \
            or not 'NewRecovered' in request.json \
            or not 'TotalConfirmed' in request.json \
            or not 'TotalDeaths' in request.json \
            or not 'TotalRecovered' in request.json:
        abort(400, 'Bad Request. Check your parameters')

    Country = request.json['Country']
    CountryCode = request.json['CountryCode']
    Date = getDateTimeStamp()  # datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
    NewConfirmed = request.json['NewConfirmed']
    NewDeaths = request.json['NewDeaths']
    NewRecovered = request.json['NewRecovered']
    Slug = Country.lower().replace(' ', '-')
    TotalConfirmed = request.json['TotalConfirmed']
    TotalDeaths = request.json['TotalDeaths']
    TotalRecovered = request.json['TotalRecovered']

    result = session.execute("""select count(*) from conv19.Country where Country='{}'""".format(Country))
    if result.was_applied == 0:
        queryAddCountry = """INSERT into conv19.Country(Country,CountryCode,Date,NewConfirmed,NewDeaths,NewRecovered,Slug,TotalConfirmed,TotalDeaths,TotalRecovered) 
        VALUES ('{}', '{}','{}', {},{}, {},'{}', {},{}, {})
        """.format(Country, CountryCode, Date, NewConfirmed, NewDeaths, NewRecovered, Slug, TotalConfirmed, TotalDeaths,
                   TotalRecovered)
        session.execute(queryAddCountry)

        queryUpdateGlobal = """UPDATE conv19.global SET NewConfirmed = NewConfirmed + {}, NewDeaths = NewDeaths + {}, NewRecovered = NewRecovered +{}, TotalConfirmed = TotalConfirmed+ {}, 
        TotalDeaths = TotalDeaths +{}, TotalRecovered = TotalRecovered+ {} WHERE Id = 1
        """.format(NewConfirmed, NewDeaths, NewRecovered, TotalConfirmed, TotalDeaths, TotalRecovered)
        session.execute(queryUpdateGlobal)
        return "Success", 201

    else:
        abort(406, description="The country already exist in the database")


@app.route('/summary/country/<name>', methods=['PUT'])
def updateCountry(name):
    if not request.json:
        abort(400, 'Bad Request. Check your parameters')
    if 'NewConfirmed' in request.json and type(request.json['NewConfirmed']) is not int:
        abort(400)
    if 'NewDeaths' in request.json and type(request.json['NewDeaths']) is not int:
        abort(400)
    if 'TotalConfirmed' in request.json and type(request.json['TotalConfirmed']) is not int:
        abort(400)
    if 'TotalDeaths' in request.json and type(request.json['TotalDeaths']) is not int:
        abort(400)
    if 'TotalRecovered' in request.json and type(request.json['TotalRecovered']) is not int:
        abort(400)

    Country = name
    Date = getDateTimeStamp()
    NewConfirmed = request.json['NewConfirmed']
    NewDeaths = request.json['NewDeaths']
    NewRecovered = request.json['NewRecovered']
    TotalConfirmed = request.json['TotalConfirmed']
    TotalDeaths = request.json['TotalDeaths']
    TotalRecovered = request.json['TotalRecovered']

    OrignalNewConfirmed, OrignalNewDeaths, OrignalNewRecovered, OrignalTotalConfirmed, OrignalTotalDeaths, OrignalTotalRecovered = 0, 0, 0, 0, 0, 0

    results = session.execute(""" SELECT * FROM conv19.Country where Country = '{}'""".format(Country))
    if len(results.current_rows) == 0:
        abort(404, description="No such country or check country spellings. Country Name:{}".format(Country))
    else:
        r = results.one()
        OrignalNewConfirmed = r.newconfirmed
        OrignalNewDeaths = r.newdeaths
        OrignalNewRecovered = r.newrecovered
        OrignalTotalConfirmed = r.totalconfirmed
        OrignalTotalDeaths = r.totaldeaths
        OrignalTotalRecovered = r.totalrecovered

        queryUpdateGlobal = """UPDATE conv19.global SET NewConfirmed = NewConfirmed - {}, NewDeaths = NewDeaths - {}, NewRecovered = NewRecovered -{}, TotalConfirmed = TotalConfirmed- {}, 
                TotalDeaths = TotalDeaths -{}, TotalRecovered = TotalRecovered - {} WHERE Id = 1
                """.format(OrignalNewConfirmed, OrignalNewDeaths, OrignalNewRecovered, OrignalTotalConfirmed,
                           OrignalTotalDeaths, OrignalTotalRecovered)
        # print("queryUpdateGlobal: ", queryUpdateGlobal)
        session.execute(queryUpdateGlobal)

        queryToUpdateCountry = """UPDATE conv19.Country SET Date = toTimestamp(now()), NewConfirmed = {} , NewDeaths = {}, NewRecovered = {}, TotalConfirmed = {}, TotalDeaths = {}, TotalRecovered={} WHERE Country='{}'""" \
            .format(NewConfirmed, NewDeaths, NewRecovered, TotalConfirmed, TotalDeaths, TotalRecovered, Country)
        # print("queryToUpdateCountry :", queryToUpdateCountry)
        session.execute(queryToUpdateCountry)

        queryUpdateGlobal = """UPDATE conv19.global SET NewConfirmed = NewConfirmed + {}, NewDeaths = NewDeaths + {}, NewRecovered = NewRecovered +{}, TotalConfirmed = TotalConfirmed+ {}, 
                TotalDeaths = TotalDeaths +{}, TotalRecovered = TotalRecovered+ {} WHERE Id = 1
                """.format(NewConfirmed, NewDeaths, NewRecovered, TotalConfirmed, TotalDeaths, TotalRecovered)
        session.execute(queryUpdateGlobal)
        # print("queryUpdateGlobal: ", queryUpdateGlobal)

        return "Success", 201


@app.route('/summary/country/<Country>', methods=['DELETE'])
def deleteCountry(Country):
    print("hello")
    results = session.execute(""" SELECT * FROM conv19.Country where Country = '{}'""".format(Country))
    if len(results.current_rows) == 0:
        abort(404, description="{} does not exist.".format(Country))
    # update Global table
    r = results.one()
    OrignalNewConfirmed = r.newconfirmed
    OrignalNewDeaths = r.newdeaths
    OrignalNewRecovered = r.newrecovered
    OrignalTotalConfirmed = r.totalconfirmed
    OrignalTotalDeaths = r.totaldeaths
    OrignalTotalRecovered = r.totalrecovered

    # Updating Global table
    queryUpdateGlobal = """UPDATE conv19.global SET NewConfirmed = NewConfirmed - {}, NewDeaths = NewDeaths - {}, NewRecovered = NewRecovered -{}, TotalConfirmed = TotalConfirmed- {}, 
                    TotalDeaths = TotalDeaths -{}, TotalRecovered = TotalRecovered - {} WHERE Id = 1
                    """.format(OrignalNewConfirmed, OrignalNewDeaths, OrignalNewRecovered, OrignalTotalConfirmed,
                               OrignalTotalDeaths, OrignalTotalRecovered)
    # print(queryUpdateGlobal)
    session.execute(queryUpdateGlobal)

    # Delete the country
    session.execute("DELETE from conv19.Country where Country = '{}'".format(Country))

    return "Success", 201


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(406)
def not_acceptable(e):
    return jsonify(error=str(e)), 406


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
