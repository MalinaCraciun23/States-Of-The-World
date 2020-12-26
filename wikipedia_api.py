from flask import Flask, jsonify
from montydb import MontyClient
from wikipedia_crawler import crawl_countries

app = Flask(__name__)
countries_col = MontyClient().db.countries

if __name__ == '__main__':
    crawl_countries()
    app.run(host="localhost", port=8000, debug=True)