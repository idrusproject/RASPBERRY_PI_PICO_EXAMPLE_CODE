import network
import urequests as requests
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# Wi-Fi credentials
SSID = "xxxx"
PASSWORD = "xxxxx"

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    print("Connecting to Wi-Fi...")
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    oled.text("Waiting For", 0, 0)
    oled.text("Connection", 0, 15)
    oled.show()
    oled.fill(0)
    while not wlan.isconnected():
        pass
IP = wlan.ifconfig()[0]
print("Wi-Fi connected!")
print("IP address:", IP)
print()
oled.text("Wi-Fi connected!", 0, 0)
oled.text("IP address:" , 0, 15)
oled.text(IP , 0, 30)
oled.show()
oled.fill(0)

stock_market = ["TSLA", "AAPL", "MCD", "SBUX", "DIS", "MA", "V"]

def get_price(stock):
    # API endpoint URL
    API_URL = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="+stock+"&apikey=xxxx"
    response = requests.get(API_URL)
    json_data = response.json()
    print(json_data)
    try :
        price = json_data["Global Quote"]["05. price"]
        oled.text(stock, 0, 0)
        oled.text("$" + price , 0, 15)
        oled.show()
        oled.fill(0)
        return price
    except:
        print("ERROR")


while True:
    for stock in stock_market:
        print("Start ", stock)
        price = get_price(stock)
        print(stock, " stock price:", price)
        print()