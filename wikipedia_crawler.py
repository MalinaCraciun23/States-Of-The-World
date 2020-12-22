import requests
from bs4 import BeautifulSoup
from montydb import MontyClient


def get_country_urls():
    country_list_url = "https://ro.wikipedia.org/wiki/Lista_statelor_lumii"
    resp = requests.get(country_list_url)
    soup = BeautifulSoup(resp.text.strip(), "html5lib")
    country_urls = [
        td.b.find("a")["href"] for td in (
            tr.find("td")
            for tr in soup.find("table").tbody.find_all("tr", valign="top"))
    ]
    country_urls.append("/wiki/Kosovo")
    country_urls.append("/wiki/Taiwan")
    return country_urls


def get_property_value(property, soup):
    th = soup.find("th", string=property)
    if not th:
        return None
    td = th.find_next_sibling("td")
    if not td:
        return None
    value = td.find("a", title=True).string.strip() if td.find(
        "a", title=True) else td.text.strip()
    return value


def get_property_values(property, soup):
    th = soup.find("th", string=property)
    if not th:
        return None
    td = th.find_next_sibling("td")
    if not td:
        return None
    li = td.find("li")
    a_list = td.find_all("a", recursive=False) + (li.find_all(
        "a", recursive=False) if li else [])
    values = [a.string.strip() for a in a_list
              if a.string] if len(a_list) > 0 else td.text.strip().split(", ")
    return values


def string_to_int(string):
    return int(string.replace(".", "").replace(",", ""))


def string_to_float(string):
    return float(string.replace(".", "").replace(",", "."))


def extract_country_population_density(country_url, population_density_table):
    a = population_density_table.find("a", href=country_url)
    td = a.parent if a else None
    suprafata_td = td.find_next_sibling("td", align="right") if td else None
    suprafata = string_to_int(
        suprafata_td.text.strip()) if suprafata_td else None
    populatie_td = suprafata_td.find_next_sibling(
        "td", align="right") if td else None
    populatie = string_to_int(
        populatie_td.text.strip()) if populatie_td else None
    densitate_td = populatie_td.find_next_sibling(
        "td", align="right") if td else None
    densitate = string_to_float(
        densitate_td.text.strip()) if densitate_td else None
    return suprafata, populatie, densitate


def get_country_information(country_url, population_density_table):
    wikipedia_url = "https://ro.wikipedia.org"
    resp = requests.get(wikipedia_url + country_url)
    soup = BeautifulSoup(resp.text.strip(), "html5lib")

    nume = soup.find("h1", id="firstHeading").string.strip()

    vecini = get_property_values("Vecini", soup)

    fus_orar = get_property_value("Fus orar", soup)

    limbi = get_property_values("Limbi oficiale", soup)

    sistem_politic = get_property_value("Sistem politic", soup)

    capitala = get_property_value("Capitala", soup)

    moneda = get_property_value("Monedă", soup)

    suprafata, populatie, densitate = extract_country_population_density(
        country_url, population_density_table)

    return {
        "nume": nume,
        "vecini": vecini,
        "fus_orar": fus_orar,
        "limbi": limbi,
        "sistem_politic": sistem_politic,
        "capitala": capitala,
        "moneda": moneda,
        "suprafata": suprafata,
        "populatie": populatie,
        "densitate": densitate
    }


def crawl_countries():
    countries_col = MontyClient().db.countries
    countries_col.drop()

    country_urls = get_country_urls()

    population_density_url = "https://ro.wikipedia.org/wiki/Lista_%C8%9B%C4%83rilor_dup%C4%83_densitatea_popula%C8%9Biei"
    resp = requests.get(population_density_url)
    soup = BeautifulSoup(resp.text.strip(), "html5lib")
    population_density_table = soup.find("table")

    countries = [
        get_country_information(url, population_density_table)
        for url in country_urls
    ]

    countries_col.insert_many(countries)
