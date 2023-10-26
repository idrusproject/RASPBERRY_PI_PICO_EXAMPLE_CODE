import machine
import socket
import math
import utime
import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("xxxx","xxxx")
 
# rgb led
red=machine.Pin(13,machine.Pin.OUT)
green=machine.Pin(14,machine.Pin.OUT)
blue=machine.Pin(15,machine.Pin.OUT)
 
# Wait for connect or fail
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    ip=wlan.ifconfig()[0]
    print('IP: ', ip)
 
# Temperature Sensor
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
 
def temperature():
    temperature_value = sensor_temp.read_u16() * conversion_factor 
    temperature_Celcius = 27 - (temperature_value - 0.706)/0.00172169/ 8 
    print(temperature_Celcius)
    utime.sleep(2)
    return temperature_Celcius
 
def webpage(value):
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                    }}
                    
                    h1 {{
                        color: #333;
                    }}
                    
                    button {{
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                    }}
                    
                    p {{
                        font-size: 18px;
                        animation: temperature-animation 2s infinite;
                    }}
                    
                    @keyframes temperature-animation {{
                        0% {{ transform: scale(1); }}
                        50% {{ transform: scale(1.2); }}
                        100% {{ transform: scale(1); }}
                    }}
                </style>
            </head>
            <body>
                <h1>Welcome to the Color Control Page</h1>
                
                <form action="./red">
                    <button style="background-color: #FF4136;">Red</button>
                </form>
                
                <form action="./green">
                    <button style="background-color: #2ECC40;">Green</button>
                </form>
                
                <form action="./blue">
                    <button style="background-color: #0074D9;">Blue</button>
                </form>
                
                <form action="./off">
                    <button style="background-color: #333;">Off</button>
                </form>
                
                <p id="temperature">Temperature is {value} degrees Celsius</p>
                
                <script>
                    var temperatureElement = document.getElementById("temperature");
                    setInterval(function() {{
                        temperatureElement.innerHTML = "Temperature is " + value + " degrees Celsius";
                    }}, 3000);
                    
                    function getRandomTemperature() {{
                        var min = 20;
                        var max = 30;
                        return Math.floor(Math.random() * (max - min + 1)) + min;
                    }}
                </script>
            </body>
            </html>
            """
    return html

 
def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        
        print(request)
        
        if request == '/off?':
            red.low()
            green.low()
            blue.low()
        elif request == '/red?':
            red.high()
            green.low()
            blue.low()
        elif request == '/green?':
            red.low()
            green.high()
            blue.low()
        elif request == '/blue?':
            red.low()
            green.low()
            blue.high()
 
        value='%.2f'%temperature()    
        html=webpage(value)
        client.send(html)
        client.close()
 
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return(connection)
 
 
try:
    if ip is not None:
        connection=open_socket(ip)
        serve(connection)
except KeyboardInterrupt:
    machine.reset()
