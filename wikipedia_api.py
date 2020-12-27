from flask import Flask, jsonify
from montydb import MontyClient
from wikipedia_crawler import crawl_countries

app = Flask(__name__)
countries_col = MontyClient().db.countries


@app.route("/toate-tarile")
def get_countries():
    countries = countries_col.find({}, {"_id": False})
    return jsonify(list(countries))


@app.route("/tara/<name>")
def get_country(name):
    country = countries_col.find_one({"nume": name}, {"_id": False})
    if country:
        return country
    else:
        return "Country not found", 404


@app.route("/vecini/<name>")
def get_neighbours(name):
    country = countries_col.find_one({"nume": name}, {
        "vecini": 1,
        "_id": False
    })
    if country:
        return jsonify(country["vecini"])
    else:
        return "Country not found", 404


@app.route("/capitala/<name>")
def get_capital(name):
    country = countries_col.find_one({"nume": name}, {
        "capitala": 1,
        "_id": False
    })
    if country:
        return country["capitala"]
    else:
        return "Country not found", 404


@app.route("/tari-care-folosesc-moneda/<moneda>")
def get_contries_by_currency(moneda):
    countries = countries_col.find({"moneda": moneda}, {
        "nume": 1,
        "_id": False
    })
    return jsonify([country["nume"] for country in list(countries)])


@app.route("/top-10-tari-suprafata-max")
def get_countries_max_surface():
    countries = countries_col.find({
        "suprafata": {
            "$ne": None
        }
    }, {
        "nume": 1,
        "suprafata": 1,
        "_id": False
    }).sort([("suprafata", -1)]).limit(10)
    return jsonify(list(countries))


@app.route("/top-10-tari-suprafata-min")
def get_countries_min_surface():
    countries = countries_col.find({
        "suprafata": {
            "$ne": None
        }
    }, {
        "nume": 1,
        "suprafata": 1,
        "_id": False
    }).sort([("suprafata", 1)]).limit(10)
    return jsonify(list(countries))


@app.route("/top-10-tari-populatie-max")
def get_countries_max_population():
    countries = countries_col.find({
        "populatie": {
            "$ne": None
        }
    }, {
        "nume": 1,
        "populatie": 1,
        "_id": False
    }).sort([("populatie", -1)]).limit(10)
    return jsonify(list(countries))


@app.route("/top-10-tari-populatie-min")
def get_countries_min_population():
    countries = countries_col.find({
        "populatie": {
            "$ne": None
        }
    }, {
        "nume": 1,
        "populatie": 1,
        "_id": False
    }).sort([("populatie", 1)]).limit(10)
    return jsonify(list(countries))


@app.route("/top-10-tari-densitate-max")
def get_countries_max_density():
    countries = countries_col.find({
        "densitate": {
            "$ne": None
        }
    }, {
        "nume": 1,
        "densitate": 1,
        "_id": False
    }).sort([("densitate", -1)]).limit(10)
    return jsonify(list(countries))


@app.route("/top-10-tari-densitate-min")
def get_countries_min_density():
    countries = countries_col.find({
        "densitate": {
            "$ne": None
        }
    }, {
        "nume": 1,
        "densitate": 1,
        "_id": False
    }).sort([("densitate", 1)]).limit(10)
    return jsonify(list(countries))


@app.route("/tari-care-au-fusul-orar/<fus_orar>")
def get_contries_by_time_zone(fus_orar):
    countries = countries_col.find({"fus_orar": fus_orar}, {
        "nume": 1,
        "_id": False
    })
    return jsonify([country["nume"] for country in list(countries)])


if __name__ == "__main__":
    crawl_countries()
    app.run(host="localhost", port=8000, debug=True)