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
    wd.stop()
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

AFN = addCurrency("AFN")
ALL = addCurrency("ALL")
AMD = addCurrency("AMD")
ANG = addCurrency("ANG")
AOA = addCurrency("AOA")
ARS = addCurrency("ARS")
AUD = addCurrency("AUD")
AWG = addCurrency("AWG")
AZN = addCurrency("AZN")
BAM = addCurrency("BAM")
BBD = addCurrency("BBD")
BDT = addCurrency("BDT")
BGN = addCurrency("BGN")
BHD = addCurrency("BHD")
BIF = addCurrency("BIF")
BMD = addCurrency("BMD")
BND = addCurrency("BND")
BOB = addCurrency("BOB")
BRL = addCurrency("BRL")
BSD = addCurrency("BSD")
BTC = addCurrency("BTC")
BTN = addCurrency("BTN")
BWP = addCurrency("BWP")
BYN = addCurrency("BYN")
BYR = addCurrency("BYR")
BZD = addCurrency("BZD")
CAD = addCurrency("CAD")
CDF = addCurrency("CDF")
CHF = addCurrency("CHF")
CLF = addCurrency("CLF")
CLP = addCurrency("CLP")
CNY = addCurrency("CNY")
COP = addCurrency("COP")
CRC = addCurrency("CRC")
CUC = addCurrency("CUC")
CUP = addCurrency("CUP")
CVE = addCurrency("CVE")
CZK = addCurrency("CZK")
DJF = addCurrency("DJF")
DKK = addCurrency("DKK")
DOP = addCurrency("DOP")
DZD = addCurrency("DZD")
EGP = addCurrency("EGP")
ERN = addCurrency("ERN")
ETB = addCurrency("ETB")
EUR = addCurrency("EUR")
FJD = addCurrency("FJD")
FKP = addCurrency("FKP")
GBP = addCurrency("GBP")
GEL = addCurrency("GEL")
GGP = addCurrency("GGP")
GHS = addCurrency("GHS")
GIP = addCurrency("GIP")
GMD = addCurrency("GMD")
GNF = addCurrency("GNF")
GTQ = addCurrency("GTQ")
GYD = addCurrency("GYD")
HKD = addCurrency("HKD")
HNL = addCurrency("HNL")
HRK = addCurrency("HRK")
HTG = addCurrency("HTG")
HUF = addCurrency("HUF")
IDR = addCurrency("IDR")
ILS = addCurrency("ILS")
IMP = addCurrency("IMP")
INR = addCurrency("INR")
IQD = addCurrency("IQD")
IRR = addCurrency("IRR")
ISK = addCurrency("ISK")
JEP = addCurrency("JEP")
JMD = addCurrency("JMD")
JOD = addCurrency("JOD")
JPY = addCurrency("JPY")
KES = addCurrency("KES")
KGS = addCurrency("KGS")
KHR = addCurrency("KHR")
KMF = addCurrency("KMF")
KPW = addCurrency("KPW")
KRW = addCurrency("KRW")
KWD = addCurrency("KWD")
KYD = addCurrency("KYD")
KZT = addCurrency("KZT")
LAK = addCurrency("LAK")
LBP = addCurrency("LBP")
LKR = addCurrency("LKR")
LRD = addCurrency("LRD")
LSL = addCurrency("LSL")
LTL = addCurrency("LTL")
LVL = addCurrency("LVL")
LYD = addCurrency("LYD")
MAD = addCurrency("MAD")
MDL = addCurrency("MDL")
MGA = addCurrency("MGA")
MKD = addCurrency("MKD")
MMK = addCurrency("MMK")
MNT = addCurrency("MNT")
MOP = addCurrency("MOP")
MRO = addCurrency("MRO")
MUR = addCurrency("MUR")
MVR = addCurrency("MVR")
MWK = addCurrency("MWK")
MXN = addCurrency("MXN")
MYR = addCurrency("MYR")
MZN = addCurrency("MZN")
NAD = addCurrency("NAD")
NGN = addCurrency("NGN")
NIO = addCurrency("NIO")
NOK = addCurrency("NOK")
NPR = addCurrency("NPR")
NZD = addCurrency("NZD")
OMR = addCurrency("OMR")
PAB = addCurrency("PAB")
PEN = addCurrency("PEN")
PGK = addCurrency("PGK")
PHP = addCurrency("PHP")
PKR = addCurrency("PKR")
PLN = addCurrency("PLN")
PYG = addCurrency("PYG")
QAR = addCurrency("QAR")
RON = addCurrency("RON")
RSD = addCurrency("RSD")
RUB = addCurrency("RUB")
RWF = addCurrency("RWF")
SAR = addCurrency("SAR")
SBD = addCurrency("SBD")
SCR = addCurrency("SCR")
SDG = addCurrency("SDG")
SEK = addCurrency("SEK")
SGD = addCurrency("SGD")
SHP = addCurrency("SHP")
SLE = addCurrency("SLE")
SLL = addCurrency("SLL")
SOS = addCurrency("SOS")
SSP = addCurrency("SSP")
SRD = addCurrency("SRD")
STD = addCurrency("STD")
SYP = addCurrency("SYP")
SZL = addCurrency("SZL")
THB = addCurrency("THB")
TJS = addCurrency("TJS")
TMT = addCurrency("TMT")
TND = addCurrency("TND")
TOP = addCurrency("TOP")
TRY = addCurrency("TRY")
TTD = addCurrency("TTD")
TWD = addCurrency("TWD")
TZS = addCurrency("TZS")
UAH = addCurrency("UAH")
UGX = addCurrency("UGX")
UYU = addCurrency("UYU")
UZS = addCurrency("UZS")
VEF = addCurrency("VEF")
VES = addCurrency("VES")
VND = addCurrency("VND")
VUV = addCurrency("VUV")
WST = addCurrency("WST")
XAF = addCurrency("XAF")
XAG = addCurrency("XAG")
XAU = addCurrency("XAU")
XCD = addCurrency("XCD")
XDR = addCurrency("XDR")
XOF = addCurrency("XOF")
XPF = addCurrency("XPF")
YER = addCurrency("YER")
ZAR = addCurrency("ZAR")
ZMK = addCurrency("ZMK")
ZMW = addCurrency("ZMW")
ZWL = addCurrency("ZWL")

