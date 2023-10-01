#!//usr/local/bin/python

import utils.utils as Utils


def ip_2_cve(ip: str):
    ip = "131.170.250.236"
    result = Utils.internet_db_query(ip)
    print(Utils.resp_2_json(result))

ip_2_cve(None)