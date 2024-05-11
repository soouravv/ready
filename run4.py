import blynklib
import adafruit_dht
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from time import sleep

# Initialize DHT11 sensor
dht11 = adafruit_dht.DHT11(board.D17)

# Initialize I2C bus and ADC
i2c = board.I2C()
ads = ADS.ADS1115(i2c, address=0x48)

# Define analog input channel for rain sensor
RAIN_SENSOR_CHANNEL = 0
rain_sensor = AnalogIn(ads, RAIN_SENSOR_CHANNEL)

# Initialize Blynk
BLYNK_AUTH = 'GqIOuwJD-m0X_ehKtfnBO40p7Lku7AOX'  # Replace with your Blynk authentication token
blynk = blynklib.Blynk(BLYNK_AUTH)

# Function to read sensor data
def read_sensor_data():
    try:
        temperature = dht11.temperature
        humidity = dht11.humidity
        rain_sensor_value = rain_sensor.value
        return temperature, humidity, rain_sensor_value
    except Exception as e:
        print("Error reading sensor data:", e)
        return None, None, None

# Function to send data to Blynk
def send_data_to_blynk():
    temperature, humidity, rain_sensor_value = read_sensor_data()
    if temperature is not None and humidity is not None and rain_sensor_value is not None:
        blynk.virtual_write(0, temperature)  # Virtual pin V0 for temperature
        blynk.virtual_write(1, humidity)     # Virtual pin V1 for humidity
        blynk.virtual_write(2, rain_sensor_value)  # Virtual pin V2 for rain sensor value

# Register virtual pin handler
@blynk.handle_event('write V10')
def write_virtual_pin_handler(pin, value):
    if value[0] == '1':
        send_data_to_blynk()

while True:
    try:
        temperature, humidity, rain_sensor_value = read_sensor_data()
        if temperature is not None:
            print("Temperature: {:.1f}°C".format(temperature))
        if humidity is not None:
            print("Humidity: {:.1f}%".format(humidity))
        if rain_sensor_value is not None:
            print("Rain Sensor Value: {}".format(rain_sensor_value))
            
        send_data_to_blynk()
        sleep(1)
    except Exception as e:
        print("Error:", e)
