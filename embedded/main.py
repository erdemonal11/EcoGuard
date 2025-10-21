from machine import Pin, I2C
import time
from scd4x import SCD4X
from ssd1306 import SSD1306_I2C

# pin configuration
i2c = I2C(0, scl=Pin(22, Pin.PULL_UP), sda=Pin(23, Pin.PULL_UP), freq=400000)

scd4x = SCD4X(i2c)
scd4x.start_periodic_measurement()

oled = SSD1306_I2C(128, 32, i2c, addr=0x3C)

# to check the air quality
def air_q(co2):
    if co2 < 800:
        return "Good"
    elif co2 < 1500:
        return "Moderate"
    else:
        return "Poor"

# dispaly resutl
def readings(co2, temp, hum):
    aq = air_q(co2)
    oled.fill(0)
    oled.text("Temp: {:.1f}C".format(temp), 0, 0)
    oled.text("Hum: {:.1f}%".format(hum), 0, 10)
    oled.text("CO2: {} ppm".format(co2), 0, 20)
    # oled.text("Air Quality: {}".format(aq), 0, 30)
    oled.show()
    print("CO2: {} ppm | Temp: {:.1f}C | Hum: {:.1f}% | Air: {}".format(co2, temp, hum, aq))


print("Waiting for first SCD41 reading...")
while True:
    try:
        if scd4x.data_ready:
            co2, temp, hum = scd4x.measurement
            readings(co2, temp, hum)
        else:
            oled.fill(0)
            oled.text("Waiting...", 0, 10)
            oled.show()
            print("SCD41 data not ready yet...")
    except OSError as e:
        oled.fill(0)
        oled.text("Sensor Error", 0, 10)
        oled.show()
        print("Sensor read error:", e)

    time.sleep(5)

