# FonoApi - Mobile Device Description Api
https://fonoapi.freshpixl.com/

The Fono API is an API which can provide mobile device descriptions such as model, brand, cpu, gpu, dimensions, release date, and more. This Python package provides easy access to the Fono API with the `requests` package.  

The [PHP class used to connect to the API](https://github.com/shakee93/fonoapi) was developed Shakeeb Sadikeen, and the Python package used to communicate with the API was developed by jesusperiago with contributions from Jake Sherman.

## Installation

```bash
# Currently:
pip install git+https://github.com/jakesherman/fonoapi.git

# Eventually:
pip install fonoapi
```

## Example

```python
from fonoapi import FonoAPI

# Use your API token to create the FonoAPI object
fon = FonoAPI('TOKEN')

# Grab device data on the Nokia 3210
device = 'nokia 3210'
phones = fon.getdevice(device)

# Grab the 10 most recent devices by Nokia
brand = 'Nokia'
phones = fon.getlatest(brand, limit=10)
```

## API

Api Url : https://fonoapi.freshpixl.com/v1/

### Method : getdevice (https://fonoapi.freshpixl.com/v1/getdevice)
available options
  - brand -
       pass the Mobile Device Brand (example : "samsung", "htc")
  - device* -
       pass nearly relevent mobile device name (example : "i9305", "A8")
       this might result multiple results at a time.
  - position -
       when a set of results is returned you can get a specific device by passing the position of your device on the result set. count starts from 0
  - token* -
    - you will need a token to access the Api. no registration, nothing, just grab the key.
      you can get it here https://fonoapi.freshpixl.com/token/generate


### Result Array Description

**Note** : Use a "_" before key if the key is starting with a number (example : _2g_bands, _4g_bands)

- DeviceName
- Brand
- technology
- 2g_bands
- gprs
- edge
- announced
- status
- dimensions
- weight
- sim
- type (display type)
- size
- resolution
- card_slot
- phonebook
- call_records
- camera_c (camera availablity)
- alert_types
- loudspeaker_
- 3_5mm_jack_
- sound_c (Sound Quality)
- wlan
- bluetooth
- gps
- infrared_port
- radio
- usb
- messaging
- browser
- clock
- alarm
- games
- languages
- java
- features_c (additional features sperated by "-")
- battery_c (battery information)
- stand_by (standby time)
- talk_time (standby time)
- colors (available colors)
- sensors
- cpu
- internal (memory + RAM)
- os
- body_c (body features seperated by "-")
- keyboard
- primary_ (primary camera)
- video
- secondary (secondary camera)
- 3g_bands
- speed
- network_c
- chipset
- features  (additional features seperated by "-")
- music_play
- protection
- gpu
- multitouch
- loudspeaker
- audio_quality
- nfc
- camera
- display
- battery_life
- 4g_bands
