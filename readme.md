Jacuzzi and Outside temperature using Micropython
=
### Felix Millqvist
### Abstract
 
This project uses a Lopy4 from Pycom, which provides Micropython,  with two temperature sensors for measurering the temperature of a jacuzzi and outside, however the tutorial can easily be adapted for measure any temperature.

This project will take around 10 hours approximatly which depends on how much you adapt to your purpose.



## Objective 
The objective of this project was to measure the temperature of a jacuzzi at my country house. This is because in the winter when I am not around and for some reason there is a power failure I need to know so the jacuzzi does not freeze and cracks so I need to be notified if the jacuzzi goes below a specific temperature. 

Some insights I have gotten is that it is easier to send data to different services and that LORA needs a clear view to travel a long distance so in this project WIFI will be used because there is no LORA-gateway close to the location of the device.
## Materials

|Component |Function|Price|Link|
|-----|--------|--------|-----|
|LoPy4|Microcontroller|€35|[Pycom](https://pycom.io/product/lopy4/)
|Expansion board  |Development Board|€16|[Pycom](https://pycom.io/product/expansion-board-3-0/)
|DS18B20 (waterproof) |Temperature sensor|€10|[Electrokit](https://www.electrokit.com/produkt/temperatursensor-vattentat-metallholje-ds18b20/)
|DS18B20  |Temperature sensor|€4.2|[Electrokit](https://www.electrokit.com/produkt/temperatursensor-ds18b20/)
|Breadboard|Connect parts|€6|[Electrokit](https://www.electrokit.com/produkt/kopplingsdack-400-anslutningar/)
|Resistor 4.7kΩ|Limit power|€12 (bigpack)|[Kjell](https://www.kjell.com/se/produkter/el-verktyg/elektronik/komponentsatser/playknowlogy-sortiment-med-resistorer-600-pack-p90646)
|Wires|Connect parts|€8 (Bigpack)|[Kjell](https://www.kjell.com/se/produkter/el-verktyg/arduino/tillbehor/kopplingskablar-hane-hane-65-pack-p87212)
I used a LOPY4 with a expantion board to make it easier to develop a prototype for this IOT-device. Then I used two DS18B20 sensors which measure temperatures. The one which is in the jacuzzi is waterproof but has no resistor connected to it. The sensor that measures the outside temperature has already a resistor connected to it, more about this in Section Putting everything together.
## Computer setup 
For this project I used Windows and Atom as the IDE with the extention Pymakr installed. The simple steps to get this to work is
1. Install [Atom.io](https://atom.io/) 
2. Navigate to the Install page, via ```Atom > Preferences > Install```
3. Search for ```pymakr``` and install the plugin form Pycom

To connect to the LOPY via ```USB``` you just connect the device and press ```ctrl-alt-c```
or
To connect to the LOPY via Telnet, navigate to ```Settings > Packages > Pymakr Settings``` and enters the ip-address that the LOPY has, which can easily be found if you are connected to usb and press the ```Get device info``` button. Then you just click ```connect device``` and select the ip-adress.

To uppload your project you just press ```ctrl-alt-s```

## Putting everything together
The following setup is for development purpose and not production. The setup needs to be much more robust build and waterproof to be outside.

First I will explain the DS18B20 sensor. This sensor is a one-wire digital sensor. This means that the sensor only needs one wire to communicate with the microcontroller. 

The sensor has also a unique 64-bit serial code which allows multiple sensors one the same bus. However in this tutorial I used one bus for each sensor to make it easier to understand.

The sensor has three pins ```GND```, ```DQ``` and ```VDD```.
The sensor needs a voltage between 3.0V and 5.5V which is perfect for the LOPY4 which operates on 3.3V

To connect the sensor it is possible to connect it in two ways, *parasite mode* which derive the power from the data line and *normal mode* which powers the sensor from the ```VDD``` pin. In this diagram I will present the *normal mode*

The left waterproofed sensor is connected to ground (black wire), 3.3V (red wire) and the data line (yellow wire) is connected to Pin 10 with a 4.7kΩ resistor to 3.3V. 

The right sensor already has a resistor on the PSB so that is connected to ground (left pin), 3.3V (middle) and data line (right) to Pin 9.


![](https://i.imgur.com/bl3kkaw.jpg)

## Platform 
The data is currently send to Ubidots where the data is save in the cloud. However I have also tried Pybytes but that seemed not that convenient for people that has not developed the system. 

Ubidots have a free service which works fine and present the data well and seems more clean. 

However I tried but without success to sent the data to Telldus which I uses for the home automation in my apartment where I want to display the temperature at the country house aswell. The api for Telldus did not work with Micropython and the time for rewriting this is not enough so maybe this is for later development.
## The code 
The following code is the main.<i></i>py which reads the data from the sensors and sends it to Ubidots aswell as Pybytes for comperission.

So first some neccesary modules are imported. `DS18X20` and `Onewire` comes from the github of Pycom [(link)](https://github.com/pycom/pycom-libraries/blob/1347ec37f17a5981070a30fb8177432eb36a9839/examples/DS18X20/onewire.py).
The `pycom` module is used for the led, `time` module is for delays and `_thread` is for be able to run multiple threads. The module `ubidots_send` is for sending data to Ubidots. This module was adapt to send a json with only one variable so the to sensors can run in parallell.

Then some constans were initialized. 

Then there is the function `DS18B20_func()` which takes the name of the sensor, signal number to pybytes, which pin it is connected to and a temperature prior which is used to detect outliers.

So the function works like follows. A `Pin` object is created to be input to the `Onewire` object which is the input object to the `DS18X20` object. Now we have the sensor object so the data from the sensor can be read. Then a variable with name `temperature_prev` is given the value on `temp_prior` which will be the previous temperature all the time.

So the easy way to explain the code is to first ignore the second while loop and focus on the first while loop which has a `True` expression so it will run for ever. Then we read the temperture from the sensor object. Then the temperature is rounded to 1 decimal and send to Pybytes and blinks red. The `pybytes.send_signal` takes a interger as signal number and a value. Then send to Ubidots and blinks green. The `ubidots_send.post_var` takes the sensor name, variable name and the value of the variable as input. More explaination on Ubidots can be found [here](https://help.ubidots.com/en/articles/961994-connect-any-pycom-board-to-ubidots-using-wi-fi-over-http).

Then the temperature gives its value to temperate_prev when the value has been send.

Then the system has to wait 60 seconds before it starts over.

This was the short and easy explaination of the function however we skipped the second while loop. The seconds while loop runs aslong as the temperature value is `None` or the difference between the current value and the previous value is greater than 5, which I thinks is a outlier and does not represent the real temperature. 

So if the value is not valid the block in the second while loop reinitialzies the `Onewire` object and the `DS18X20` object and then reads a new temperature and checks if this value is valid. 

This solution may not be the best but the modudle from Pycom seems to have some bugs so I sometimes got `None` values which does not changes if I am not reinitializing the objects. 

The two last rows is where a run the function. I start two threads with the parameters for the to sensors so thay can run in parallell. 



```python=
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

```
For Ubidots you need to add your Ubidots token in the ubidots_send.py where it is says `#Put here your TOKEN`
> See full code on Github: [Jacuzzi-and-Outside-temperature-using-Micropython](https://github.com/felixmillqvist/Jacuzzi-and-Outside-temperature-using-Micropython)
## Transmitting the data / connectivity
The data is submitted to Ubidots and Pybytes with a sample rate of 60 seconds. The wireless protocol that is used is WiFi and this is due to the fact that there is no LORA gateway close enough to the device. However the Wifi will work even if there is a power failure at my house because there is routers all over the yard and aslong as there is power in some house the Wifi will work and if all there is a power failure all over the place Ubidots will notify me more on this in the next section.  

The transport protocol that is used for Ubidots is webhook. There is a json format with one varible that is send via a HTTP request. This is a some bytes to many but now when I am using WiFi there is no problem.

The transport protocol for Pybytes is MQTT. However this platform is still there because of comperision reasons.
## Presenting the data
Here I will show the dashboard from Ubidots because that is the main platform that is used.
![](https://i.imgur.com/OkzKolM.png)
The left scope is the temperature of the water in the jacuzzi and the right scope is the outside temperature.
The data is saved every 60 seconds when the data is send. I have chosen Ubidots because it has a free version and has a great event handler which can notify me if the temperature is below a certain point or if the device goes offline for some reason. This is perfect if there is a power failure and the wifi stops working or the jacuzzi does not work properly.

So have made two events:
1. If the temperature is below 34C then it will send me an email and notify me.
2. If the device is inactive for more than 30 minutes then it will send me an and notify me.
## Finalizing the design
The final project ended up well, the project does what it is supposed to do. However it is still just in developing stage and need a housing and better wire connections. As can be seen in the following picture the 4.7kΩ is not there in my country house I did not have that value so I make a connection with a couple resistors which results in 4.7kΩ.  
![](https://i.imgur.com/KDLRH5c.jpg)
There is a powerbank in the picture now but I have ordered a powerbank that is able to charge the powerbank the same time as it is powering the device. So it always has power and if there is a power failure the powerbank can provied power to the device until the device notify me that the temperature of the jacuzzi is too low.
![](https://i.imgur.com/KeWkUnF.jpg)


