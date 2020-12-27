import re
import requests

api_url = "http://localhost:8000"
routes = [
    "/toate-tarile", "/tara/<name>", "/vecini/<name>", "/capitala/<name>",
    "/tari-care-folosesc-moneda/<moneda>", "/top-10-tari-suprafata-max",
    "/top-10-tari-suprafata-min", "/top-10-tari-populatie-max",
    "/top-10-tari-populatie-min", "/top-10-tari-densitate-max",
    "/top-10-tari-densitate-min", "/tari-care-au-fusul-orar/<fus_orar>",
    "/tari-care-vorbesc-limba/<limba>",
    "/tari-care-au-sistemul-politic/<sistem_politic>",
    "/tari-care-incep-cu/<litera>"
]

if __name__ == "__main__":
    for num, route in enumerate(routes, start=1):
        print("Route {}: {}".format(num, route))
    while True:
        choice = int(input("Pick a route: "))
        route = routes[choice - 1]
        variable = re.search(r'(?<=<).*(?=>)', route)
        value = input("Enter value of " + variable.group() +
                      ": ") if variable else ""
        r = requests.get(api_url + re.sub(r'<.*>', value, route))
        print(r.text)
