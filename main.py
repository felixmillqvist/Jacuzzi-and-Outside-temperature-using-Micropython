# main.py

import time
from machine import Pin
from onewire import DS18X20
from onewire import OneWire
import pycom
import _thread
import ubidots_send

# Init values
JACCUZI_TEMP_SIGNAL = 1
OUTSIDE_TEMP_SIGNAL = 2
OUTLIER_THRESHOLD = 5
DECIMALS = 1
DELAY = 58



def DS18B20_func(sens_name, sig_nbr, pin_str, temp_prior):
    #DS18B20 data line connected to pin pin_str
    pin = Pin(pin_str)
    ow = OneWire(pin)
    temp = DS18X20(ow)
    pycom.heartbeat(False)

    print('\n' + sens_name + ' sensor is initialized to ' + pin_str )

    # Prior needs to be within 5 degrees celsius from actual temp
    temperature_prev = temp_prior
    while True:
        temperature = temp.read_temp_async()
        time.sleep(1)
        #time.sleep(DELAY)
        temp.start_conversion()
        time.sleep(1)
        # Remove None values and outliers
        while temperature is None or abs(temperature - temperature_prev) > OUTLIER_THRESHOLD:
            print(sens_name + ' temperature error: ' + str(temperature))
            # In order to remove the None values I need to reinitialize the sensor
            # it may be a better solution to this
            ow = OneWire(pin)
            temp = DS18X20(ow)
            temperature = temp.read_temp_async()
            time.sleep(1)
            temp.start_conversion()
            time.sleep(1)

        temperature = round(temperature,DECIMALS)
        print(sens_name + ' temperature: ' + str(temperature))

        # Send to pybytes and blink red
        pycom.rgbled(0x330000)
        pybytes.send_signal(sig_nbr,temperature)
        pycom.rgbled(0x000000)

        # Send to ubidots and blink green
        pycom.rgbled(0x003300)
        ubidots_send.post_var("Pycom", sens_name, temperature)
        pycom.rgbled(0x000000)

        temperature_prev = temperature
        time.sleep(DELAY)

_thread.start_new_thread(DS18B20_func, ('JACCUZI', JACCUZI_TEMP_SIGNAL, 'P10', 21))
_thread.start_new_thread(DS18B20_func, ('OUTSIDE', OUTSIDE_TEMP_SIGNAL, 'P9', 21))
