# ref: https://ipapi.is/developers.html
# ref: https://github.com/ipapi-is/ipapi
# ref: https://internetdb.shodan.io/

import requests


def resp_2_json(resp):
    return resp.json()


def ip_query(ip: str):
    api = "https://api.ipapi.is/?q="
    endpoint = api + ip
    return requests.get(endpoint, timeout=50)


def asn_query(asn: str):
    api = "https://api.ipapi.is/?q="
    endpoint = api + "as" + asn.strip()
    return requests.get(endpoint, timeout=50)


def internet_db_query(ip: str):
    api = "https://internetdb.shodan.io/"
    endpoint = api + ip
    return requests.get(endpoint, timeout=50)