import requests
from bs4 import BeautifulSoup


def get_country_urls():
    country_list_url = "https://ro.wikipedia.org/wiki/Lista_statelor_lumii"
    wikipedia_url = "https://ro.wikipedia.org"
    resp = requests.get(country_list_url)
    soup = BeautifulSoup(resp.text, "html5lib")
    country_urls = [
        wikipedia_url + td.find("a")["href"]
        for td in (tr.find('td') for tr in soup.find("table").tbody.findAll(
            "tr", {"valign": "top"}))
    ]
    country_urls.append("https://ro.wikipedia.org/wiki/Kosovo")
    country_urls.append("https://ro.wikipedia.org/wiki/Taiwan")
    return country_urls


def get_country_information(country_url):
    pass


def crawl_countries():
    country_urls = get_country_urls()
    for url in country_urls:
        pass