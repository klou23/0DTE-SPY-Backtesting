import requests

api_root = 'https://demo.dxfeed.com/webservice/rest/events.json'


def request(params: dict) -> dict:
    req_url = api_root
    first = True

    for key in params:
        req_url += '?' if first else '&'
        first = False
        req_url += str(key)
        req_url += '='
        req_url += str(params[key])

    print(req_url)
    return requests.get(req_url).json()
