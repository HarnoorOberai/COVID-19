# COVID 19 WebApp
The coronavirus COVID-19 is affecting 210 countries and territories around the world and 2 international conveyances. The list of countries and territories and their continental regional classification is based on the United Nations Geoscheme. The purpose of this webapp is to help people get a clear picutre of the world COVID-19 status in an easy visualized descriptive way. This app makes calls to an external API hosted in https://api.covid19api.com/. 

---

## How it works?

You can check the external APIs and in-built rest services to read, add, update and delete (CRUD) the status of deaths, recovery of patients suffering from COVID -19.

### Terminal Commands


#### External API

###### `1. @app.route('/summary')`
Get the summary of all the countries and global stats

###### `2. @app.route('/summary/globalByExternalAPI')`
Get the global stats

###### `3. @app.route('/summary/countryByExternalAPI')`
Get the summary of all the countries  stats



#### To add a new country to the database:

`@app.route('/summary/country')`

The user must provide:
* Country
* CountryCode
* NewConfirmed
* NewDeaths
* NewRecovered
* TotalConfirmed
* TotalDeaths
* TotalRecovered

This is a post request and will be executed in the following way. In the following curl command I am using a country as "TestCountry" to be added in the data base.
```
curl -i -H "Content-Type: application/json" -X POST -d '{"Country":"Test Country","CountryCode":"TC","NewConfirmed":3843,"NewDeaths":442,"NewRecovered":58,"TotalConfirmed":52279,"TotalDeaths":5385,"TotalRecovered":287}' http://0.0.0.0:80/summary/country
```

#### Update a the contents of a country:

`@app.route('/summary/country/<name>')`

The user must provide:
* CountryCode
* NewConfirmed
* NewDeaths
* NewRecovered
* TotalConfirmed
* TotalDeaths
* TotalRecovered

This is a put request and will be executed in the following way. In the following curl command I am using a country as "TestCountry" to be updated in the data base.

```
curl -i -H "Content-Type: application/json" -X PUT -d '{"NewConfirmed":101,"NewDeaths":101,"NewRecovered":101,"TotalConfirmed":101,
"TotalDeaths":101,"TotalRecovered":101}' http://0.0.0.0:80/summary/country/TestCountry
```

#### Delete a country:

`@app.route('/summary/country/<name>')`

This is a delete request and will be executed in the following way. In the following curl command I am using a country as "TestCountry" to be deleted in the data base.

```
curl -X DELETE http://0.0.0.0:80/summary/country/TestCountry
```

---
## Licenese and copyright
@HARNOOR SINGH OBERAI, Queen Mary University of London
