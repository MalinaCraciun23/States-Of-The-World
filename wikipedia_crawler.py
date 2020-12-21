import requests
from bs4 import BeautifulSoup


def get_country_urls():
    country_list_url = "https://ro.wikipedia.org/wiki/Lista_statelor_lumii"
    wikipedia_url = "https://ro.wikipedia.org"
    resp = requests.get(country_list_url)
    soup = BeautifulSoup(resp.text, "html5lib")
    country_urls = [
        wikipedia_url + td.b.find("a")["href"]
        for td in (tr.find('td') for tr in soup.find("table").tbody.find_all(
            "tr", {"valign": "top"}))
    ]
    country_urls.append("https://ro.wikipedia.org/wiki/Kosovo")
    country_urls.append("https://ro.wikipedia.org/wiki/Taiwan")
    return country_urls


def get_property_value(property, soup):
    th = soup.find("th", string=property)
    if not th:
        return None
    td = th.find_next_sibling("td")
    if not td:
        return None
    value = td.find('a', title=True).string if td.find('a',
                                                       title=True) else td.text
    return value


def get_property_values(property, soup):
    th = soup.find("th", string=property)
    if not th:
        return None
    td = th.find_next_sibling("td")
    if not td:
        return None
    li = td.find('li')
    a_list = td.find_all('a', recursive=False) + (li.find_all(
        'a', recursive=False) if li else [])
    values = [a.string for a in a_list
              if a.string] if len(a_list) > 0 else td.text.split(", ")
    return values


def get_country_information(country_url):
    resp = requests.get(country_url)
    soup = BeautifulSoup(resp.text, "html5lib")

    nume = soup.find("h1", {"id": "firstHeading"}).string

    vecini = get_property_values("Vecini", soup)

    fus_orar = get_property_value("Fus orar", soup)

    limbi = get_property_values("Limbi oficiale", soup)

    sistem_politic = get_property_value("Sistem politic", soup)

    capitala = get_property_value("Capitala", soup)

    moneda = get_property_value("Monedă", soup)

    return {
        "nume": nume,
        "vecini": vecini,
        "fus_orar": fus_orar,
        "limbi": limbi,
        "sistem_politic": sistem_politic,
        "capitala": capitala,
        "moneda": moneda
    }


def crawl_countries():
    country_urls = get_country_urls()
    for url in country_urls:
        country_information = get_country_information(url)
        print(country_information)


crawl_countries()