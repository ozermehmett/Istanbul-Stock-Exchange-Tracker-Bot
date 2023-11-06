import http.client
import json
from main import API


def get_data(api_key):
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': api_key
    }

    conn.request("GET", "/economy/hisseSenedi", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data


def get():
    stock_data = get_data(API)
    data_dict = json.loads(stock_data)
    results = data_dict["result"]

    with open("stock_last_prices.txt", "w") as file:
        for symbol_info in results:
            symbol = symbol_info["code"]
            last_price = symbol_info["lastpricestr"]
            file.write(symbol + "-" + last_price + "\n")
