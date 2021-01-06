"""
Wikipedia Flask API.

Provide routes to get data about countries from Wikipedia.
"""
from flask import Flask, jsonify
from montydb import MontyClient
from wikipedia_crawler import crawl_countries
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
countries_col = MontyClient().db.countries


@app.errorhandler(Exception)
def handle_error(e):
    """Catch exceptions and return a proper response."""
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


@app.route("/toate-tarile")
def get_countries():
    """Get all countries from the database."""
    countries = countries_col.find({}, {"_id": False})
    return jsonify(list(countries))


@app.route("/tara/<name>")
def get_country(name):
    """Get a country by name from the database."""
    country = countries_col.find_one({"nume": name}, {"_id": False})
    if country:
        return country
    else:
        return "Country not found", 404


@app.route("/vecini/<name>")
def get_neighbours(name):
    """Get a country's neighbours from the database."""
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
    """Get a country's capital from the database."""
    country = countries_col.find_one({"nume": name}, {
        "capitala": 1,
        "_id": False
    })
    if country:
        return country["capitala"]
    else:
        return "Country not found", 404


@app.route("/tari-care-folosesc-moneda/<moneda>")
def get_countries_by_currency(moneda):
    """Get all countries that use a certain currency."""
    countries = countries_col.find({"moneda": moneda}, {
        "nume": 1,
        "_id": False
    })
    return jsonify([country["nume"] for country in list(countries)])


@app.route("/top-10-tari-suprafata-max")
def get_countries_max_surface():
    """Get the top 10 countries with maximum surface."""
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
    """Get the top 10 countries with minimum surface."""
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
    """Get the top 10 countries with maximum population."""
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
    """Get the top 10 countries with minimum population."""
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
    """Get the top 10 countries with maximum density."""
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
    """Get the top 10 countries with minimum density."""
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
def get_countries_by_time_zone(fus_orar):
    """Get all countries in a certain timezone."""
    countries = countries_col.find({"fus_orar": fus_orar}, {
        "nume": 1,
        "_id": False
    })
    return jsonify([country["nume"] for country in list(countries)])


@app.route("/tari-care-vorbesc-limba/<limba>")
def get_countries_by_language(limba):
    """Get all countries that use a certain language."""
    countries = countries_col.find({"limbi": limba}, {"nume": 1, "_id": False})
    return jsonify([country["nume"] for country in list(countries)])


@app.route("/tari-care-au-sistemul-politic/<sistem_politic>")
def get_countries_by_political_system(sistem_politic):
    """Get all countries that use a certain political system."""
    countries = countries_col.find({"sistem_politic": sistem_politic}, {
        "nume": 1,
        "_id": False
    })
    return jsonify([country["nume"] for country in list(countries)])


@app.route("/tari-care-incep-cu/<litera>")
def get_countries_by_starting_letter(litera):
    """Get all countries which name starts with a certain letter."""
    countries = countries_col.find({"nume": {
        "$regex": "^" + litera
    }}, {
        "nume": 1,
        "_id": False
    })
    return jsonify([country["nume"] for country in list(countries)])


if __name__ == "__main__":
    print("Started crawling wikipedia...")
    crawl_countries()
    print("Finished crawling wikipedia")
    app.run(host="localhost", port=8000, debug=True, use_reloader=False)
