from .quantity import *
import requests
import json
from datetime import date
import os

# https://stackoverflow.com/questions/16148735/how-to-implement-a-watchdog-timer-in-python
from threading import Timer
class Watchdog(Exception):
    def __init__(self, timeout, userHandler=None):  # timeout in seconds
        self.timeout = timeout
        self.handler = userHandler if userHandler is not None else self.defaultHandler
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def defaultHandler(self):
        raise self


_directory = os.path.dirname(os.path.abspath(__file__))
_exchangeRatePath = _directory+"/exchange.json"
_keyPath = _directory+"/api_key.txt"
_url = "https://api.apilayer.com/exchangerates_data/latest?symbols=&base=USD"
_payload = {}
try:
    with open(_keyPath, "r") as key:
        lines = key.readlines()
        apiKey = lines[0].strip()
except:
    with open(_keyPath, 'w') as f:
        f.write("<replace with API key string>")
    raise NotImplementedError('could not find api key for currency conversion! go to https://apilayer.com/marketplace/exchangerates_data-api to get a key, and put it in the api_key.txt file!')
_headers= {
  "apikey": apiKey
}
_conversions = {}

def getRates():
    conv = {}
    try:
        with open(_exchangeRatePath, "r") as f:
            conv = json.load(f)
        s = conv["date"]
        if s != str(date.today()):
            print("making currency conversion request...")
            with open(_exchangeRatePath, "w") as f:
                f.write(makeRequest())
            with open(_exchangeRatePath, "r") as f:
                conv = json.load(f)
    except:
        print("making currency conversion request...")
        with open(_exchangeRatePath, "w") as f:
            f.write(makeRequest())
        with open(_exchangeRatePath, "r") as f:
            conv = json.load(f)
    return conv.copy()

def makeRequest():
    wd = Watchdog(60)
    response = requests.request("GET", _url, headers=_headers, data = _payload)
    status_code = response.status_code
    result = response.text
    return result


def addCurrency(name):
    try:
        rate = _conversions["rates"][name]
        return Unit.derived(USD, name, 1/rate)
    except:
        print("unsupported currency symbol \""+name+"\"!")

_conversions = getRates()
USD = Unit({"$": 1}, "USD")
addBaseUnit(USD)

kUSD = kilo(USD)

EUR = addCurrency("EUR")
JPY = addCurrency("JPY")
GBP = addCurrency("GBP")
BTC = addCurrency("BTC")
