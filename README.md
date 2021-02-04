# sensor.mopeka_pro_check
Home Assistant custom component to support Mopeka Pro Check Tank Level Sensors
A custom component for [Home Assistant](https://www.home-assistant.io) that listens for the advertisement message broadcast by Mopeka Bluetooth propane tank level sensors.

## Supported Devices

* Mopeka Pro check <https://mopeka.com/product/mopeka-check-pro-lp-sensor/>

## Installation

**1. Install the custom component:**

* The easiest way is to install it with [HACS](https://hacs.xyz/). First install [HACS](https://hacs.xyz/) if you don't have it yet. After installation, the custom component can be found in the HACS store under integrations.

* Alternatively, you can install it manually. Just copy paste the content of the `sensor.mopeka_pro_check/custom_components` folder in your `config/custom_components` directory.
     As example, you will get the `sensor.py` file in the following path: `/config/custom_components/mopeka_pro_check/sensor.py`.

**2. Restart Home Assistant:**

* Restarts just make everything better.

**3. Add the platform to your configuration.yaml file (see [below](#configuration))**

**4. Restart Home Assistant:**

* A second restart may be required to load the configuration. Within a few minutes, the sensors should be added to your home-assistant automatically (at least two [period](#period) may be required.  If the [period](#period) is set to a time greater than two minutes, at least four [period](#period) may be required).

* Make sure you have woken up the sensor by following the directions supplied with your sensor.  Sensors
are shipped from the factory in a low power mode and will need to be woken up to start reporting.

* Physically install the sensor following the supplied directions.

## Troubleshooting and help

This is still a work in progress with very limited testing.
Please use github issues, pull requests, and discussion to provide feedback, open issues, or ask questions.
I am new to developing for HomeAssistant so for general questions or system questions using
the home assistant forums would be better.  Eventually it looks like most add a community post
and i will do so once this component works or is in shape for sharing.

## Configuration Variables

Specify the sensor platform `mopeka_pro_check` and a list of devices with unique MAC address.

*NOTE*: device name is optional.  If not provided, devices will be labeled using the MAC address

``` yaml
sensor:
  - platform: mopeka_pro_check
    mopeka_devices:
      # Just use default tank type
      - mac: "A1:B2:C3:D4:E5:F6"
        name: RV Right Tank
      # Set the tank type to a standard 20lbs vertical tank
      - mac: "A6:B5:C4:D3:E2:F1"
        name: RV Left Tank
        tank_type: "standard"
        std_tank: "20lb_v"
      # Set the max height in MM using custom tank 
      - mac: "A0:B0:C0:D0:E0:F0"
        name: BBQ
        tank_type: "custom"
        max_height: 452.10
        
```

### Additional configuration options

| Option | Type |Default Value | Description |  
| -- | -- | -- | -- |
| `period` | positive integer | `60` | The period in seconds during which the sensor readings are collected and transmitted to Home Assistant after averaging. The Mopeka device broadcast rate is configurable using the sensor buttons but this period helps to limit the amount of mostly duplicate data stored in  Home Assistant's database since tank level should not change that quickly |
| `hci_device`| string | `hci0` | HCI device name used for scanning. |

## Credits

This sensor component was copied from [custom-components/sensor.groveetemp_bt_hci](https://github.com/Home-Is-Where-You-Hang-Your-Hack/sensor.goveetemp_bt_hci) at commit [84cd857ec71e5c076fb37f6748d514aed3c0d210](https://github.com/Home-Is-Where-You-Hang-Your-Hack/sensor.goveetemp_bt_hci/commit/84cd857ec71e5c076fb37f6748d514aed3c0d210)

That repo also mentions

>This was originally based on/shamelessly copied from [custom-components/sensor.mitemp_bt](https://github.com/custom-components/sensor.mitemp_bt).  I want to thank [@tsymbaliuk](https://community.home-assistant.io/u/tsymbaliuk) and [@Magalex](https://community.home-assistant.io/u/Magalex) for providing a blueprint for developing my Home Assistant component.

So I want to thank the work of [@Thrilleratplay](https://community.home-assistant.io/u/thrilleratplay) as well as those mentioned above.  

Finally, [Mopeka Products](https://mopeka.com/) was extremely helpful.  There support has been great and the short time I have used their sensor I have been happy with its capability. I would recommend their sensor.

## Notices

Since this is a copy of [custom-components/sensor.mitemp_bt](https://github.com/custom-components/sensor.mitemp_bt) many components will retain that projects copyright.

``` txt
MIT License

Copyright (c) 2020 Home-Is-Where-You-Hang-Your-Hack

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```