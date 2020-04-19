# COVID 19 WebApp
The coronavirus COVID-19 is affecting 210 countries and territories around the world and 2 international conveyances. The list of countries and territories and their continental regional classification is based on the United Nations Geoscheme. The purpose of this webapp is to help people get a clear picutre of the world COVID-19 status in an easy visualized descriptive way. This app makes calls to an external API hosted in https://api.covid19api.com/. 

---

## How it works?

You can check the external APIs and in-built rest services to read, add, update and delete (CRUD) the status of deaths, recovery of patients suffering from COVID -19.

---
## Features:

1. REST-based service interface.
2. Interaction with external REST services.
3. Use of on an external Cloud database(cassandra db) for persisting information. 
4. Support for cloud scalability, deployment in a container environment.
5. Cloud security awareness by running my flask application over HTTPS Using self-signed certificate.
6. Request followup orchestration using HATEOAS.

---

## Terminal Commands

---

### External API

##### *GET* `1. @app.route('/summary')`
Get the summary of all the countries and global stats

##### *GET*  `2. @app.route('/summary/globalByExternalAPI')`
Get the global stats

##### *GET*  `3. @app.route('/summary/countryByExternalAPI')`
Get the summary of all the countries  stats

---
### REST-based Service Interface

#### *GET*  `1. @app.route('/summary/globalByBrowser')`

Get the global stats from cassandra db:

#### *GET*  `2. @app.route('/summary/countryByBrowser')`

Get the all the countries stats from cassandra db:

#### *GET*  `3. @app.route('/summary/country/<name>'),`

Get the stats of a particular country:

#### *POST*  `4. @app.route('/summary/country')`

To add a new country to the database:

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
curl -i -k -H "Content-Type: application/json" -X POST -d '{"Country":"TestCountry","CountryCode":"TC","NewConfirmed":3843,"NewDeaths":442,
"NewRecovered":58,"TotalConfirmed":52279,"TotalDeaths":5385,"TotalRecovered":287}' https://0.0.0.0:443/summary/country
```
----

#### *PUT* `5. @app.route('/summary/country/<name>')`

Update a the contents of a country:

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
curl -i -k -H "Content-Type: application/json" -X PUT -d '{"NewConfirmed":101,"NewDeaths":101,"NewRecovered":101,"TotalConfirmed":101,
"TotalDeaths":101,"TotalRecovered":101}' https://0.0.0.0:443/summary/country/TestCountry
```

#### *DELETE* `6. @app.route('/summary/country/<name>')`

Delete a country:

This is a delete request and will be executed in the following way. In the following curl command I am using a country as "TestCountry" to be deleted in the data base.

```
curl -k -X DELETE https://0.0.0.0:443/summary/country/TestCountry
```

---


### Deployment

0.- Inital Steps
```
sudo apt update
sudo apt install docker.io
sudo docker pull cassandra:latest
```

1.- Run cassandra in a Docker container and expose port 9042:
```
sudo docker run --name cassandra-cont -p 9042:9042 -d cassandra
```

2.- Download Global.csv and Country.csv file
```
wget https://raw.githubusercontent.com/HarnoorOberai/CloudComputingMiniProject/master/Global.csv
wget https://raw.githubusercontent.com/HarnoorOberai/CloudComputingMiniProject/master/Country.csv
```

3.- Puting your data inside cassandra-cont
```
sudo docker cp Global.csv cassandra-cont:/home/Global.csv
sudo docker cp Country.csv cassandra-cont:/home/Country.csv
```

4.- Access the cassandra container in iterative mode:
```
sudo docker exec -it cassandra-cont cqlsh
```

3.- Create a dedicated keyspace inside cassandra for the gym database:
```
cqlsh> CREATE KEYSPACE conv19 WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
```

4.- Create the database table for the global stats:
```
cqlsh> CREATE TABLE conv19.global (
    id int PRIMARY KEY,
    newconfirmed counter,
    newdeaths counter,
    newrecovered counter,
    totalconfirmed counter,
    totaldeaths counter,
    totalrecovered counter
);
```
5.- Create the database table for country: 
```
cqlsh> CREATE TABLE conv19.country (
    Country text PRIMARY KEY,
    CountryCode text,
    Date timestamp,
    NewConfirmed int,
    NewDeaths int,
    NewRecovered int,
    Slug text,
    TotalConfirmed int,
    TotalDeaths int,
    TotalRecovered int
) ;

```
6.- Copy the contents of Global.csv and Country.csv to conv19.global and conv19.country table respectively.
```
cqlsh> COPY conv19.global(ID,NewConfirmed,NewDeaths,NewRecovered,TotalConfirmed,TotalDeaths,TotalRecovered)
FROM '/home/Global.csv' WITH HEADER=TRUE;

cqlsh> COPY conv19.Country(Country,CountryCode,Date, NewConfirmed, NewDeaths, NewRecovered, Slug, TotalConfirmed, TotalDeaths, TotalRecovered)
FROM '/home/Country.csv' WITH HEADER=TRUE;
```

---
### Security

This app is served over https.

I have cert.pem -keyout key.pem with the code. 

No need to do the following step. This is how I added self-signed certificate
```
Self-signed certificate

1. Run in your project folder
$ openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
Generating a RSA private key
.....................................++++
....................................................................................++++
writing new private key to 'key.pem'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:UK
State or Province Name (full name) [Some-State]:London
Locality Name (eg, city) []:Wandsworth
Organization Name (eg, company) [Internet Widgits Pty Ltd]:QMUL MiniProject
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:localhost
Email Address []:

```

Inside app.py
```
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))
```
Adding the ceritficate will add security to our app and will now use *https*.

---
### Execution

```
cd CloudComputingMiniProject/
sudo docker build . --tag=miniproject:v1
sudo docker run -dp 443:443 miniproject:v1
```

` Remember to add https infront of the url.`

---

### Bugs and their resolution:
```
If you are using MAC open the link click on the background and type "thisisunsafe". Other browser proceed anyways.
```

## Licenese and copyright
@HARNOOR SINGH OBERAI, Queen Mary University of London
