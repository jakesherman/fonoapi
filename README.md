# fonoapi - Python wrapper around the FonoApi

https://fonoapi.freshpixl.com/

The Fono API is an API which can provide **mobile device descriptions** such as model, brand, cpu, gpu, dimensions, release date, and more. This package package provides a convenient wrapper around the Fono Api via the `requests` package.

The [API](https://github.com/shakee93/fonoapi) was developed [shakee93](https://github.com/shakee93). This package started off as a fork of a [package](https://github.com/jesusperiago/fonoapi) written by [jesusperiago](https://github.com/jesusperiago) - I added the `getlatest` method to take advantage of the [getlatest API method](https://fonoapi.freshpixl.com/v1/getlatest), and make a lot of under-the-hood organizational changes in order to submit this package to `PyPI` to make it more easily available.

### Installation

```bash
pip install git+https://github.com/jakesherman/fonoapi.git
```

## Tutorial

Before starting, make sure to [generate an API token](https://fonoapi.freshpixl.com/token/generate#). We are going to start by creating a `FonoAPI` object, which we initialize with our API token in order to start interacting with the FonoApi:

```python
from __future__ import print_function  # -- for Python 2.7

from fonoapi import FonoAPI
fon = FonoAPI('TOKEN')
```

### Getting devices matching a specific device name

We have a specific device in mind, the **iPhone 7**, what we wish to learn more about. We can use the `getdevice` method to return information from the API about a specific device:

```python
device = 'iPhone 7'
iPhone_7 = fon.getdevice(device)
print(iPhone_7)
```

    | Devices Object: mobile device data|
    ------------------------------------
    Number of devices : 4
    Input parameters : {'device': 'iPhone 7', 'position': None, 'brand': None}

The `getdevice` method returns a `Devices` object, an object that makes it easy to retrieve data from the Fono Api. Printing out the object gives us information on how many devices we retrieved information for, and what the parameters were given to `getdevice`.

We can output the data in the `Devices` object in three ways by calling the following methods on the `Devices` object:
- `dataframe` : As a Pandas DataFrame, where each row corresponds to a phone
- `list_of_dicts` : As a list of dictionaries, with one dict per phone
- `list_of_lists : `As a list of lists, where each sublist corresponds to a phone

Not all mobile devices in the FonoApi have every possible attribute associated with them. In the case of `list_of_dicts`, only the attributes associated with each phone is included in each phone's dictionary. In the cases of `dataframe` or `list_of_lists`, you may choose specific columns to include for every phone. In this case, devices with no value for a particular column will have values of `numpy.nan` or `None`, respectively.

In our case, let's look at the attributes `Brand, DeviceName, body_c` for the devices returned by our API call:

```python
print(iPhone_7.dataframe(['Brand', 'DeviceName', 'body_c']))
```

Brand | DeviceName | body_c |
| --- | --- | --- | --- |
| 0 | Prestigio | Prestigio MultiPhone 7500 | None |
| 1 | Prestigio | Prestigio MultiPhone 7600 Duo | None |
| 2 | Apple | Apple iPhone 7 Plus | - IP67 certified - dust and water resistant\r\... |
| 3 | Apple | Apple iPhone 7 | - IP67 certified - dust and water resistant\r\... |

- There are two non-Apple devices by Prestigio in the list! The model names of the two devices begin with Prestigio Mult*iPhone 7*500, so it's understandable that they would show up when we searched for the string 'iPhone 7'
- The two Prestigio devices don't have a value for the `body_c` attribute, so they have `np.nan` values for that column

In order to get rid of the Prestigio devices in our results, all we have to do is specify the `brand` argument to the `getdevice` method:

```python
device, brand = 'iPhone 7', 'Apple'
iPhone_7 = fon.getdevice(device, brand)
print(iPhone_7.dataframe(['Brand', 'DeviceName', 'body_c']))
```

Brand | DeviceName | body_c |
| --- | --- | --- | --- |
| 0 | Apple | Apple iPhone 7 Plus | - IP67 certified - dust and water resistant\r\... |
| 1 | Apple | Apple iPhone 7 | - IP67 certified - dust and water resistant\r\... |

### Getting the latest devices for a specific brand

`getlatest` will return information about the most recent devices for a given brand. For example, let's imagine that we wish to get data on the lastest mobile devices from Apple:

```python
brand = 'Apple'
latest_apples = (
    fon
    .getlatest(brand, limit=5)
    .dataframe(['DeviceName', 'announced', '_3_5mm_jack_', 'talk_time'])
)
print(latest_apples)
```

DeviceName | announced | _3_5mm_jack_ | talk_time |
| --- | --- | --- | --- | --- |
| 0 | Apple iPad Pro 12.9 | 2017, June | Yes | Up to 10 h (multimedia) |
| 1 | Apple iPad Pro 10.5 | 2017, June | Yes | Up to 10 h (multimedia) |
| 2 | Apple iPad 9.7 | 2017, March | Yes | Up to 10 h (multimedia) |
| 3 | Apple iPhone 8 | Not announced yet | No | None |
| 4 | Apple Watch Series 1 Sport 42mm | 2016, September | No | Up to 3 h 40 min |

Finally, perhaps we want to retrieve data on the most recent mobile devices for a whole host of brands ... but we're not sure if we spelled the brand names correctly. By default, when `getlatest` (or `getdevice`) don't retrieve any results from the API, they return an empty `Devices` object. That empty `Devices` object has a value of `True` for its `null` class attribute (and a value of `False` for its `not_null` class attribute). For example:

```python
brands = ['Apple', 'Samsung', 'LG', 'Huawei', 'SonyEricsson']
brand_devices = []
for brand in brands:
    devices = fon.getlatest(brand, limit=3)
    brand_devices.append(devices)
```

    Could not retrieve brand information for brand SonyEricsson from the Fono API.


```python
# Print out the Devices object for SonyEricsson
print(brand_devices[-1])
```

    | Devices Object: mobile device data|
    ------------------------------------
    Number of devices : 0
    Input parameters : {'brand': 'SonyEricsson', 'limit': 3}

The problem here is that there is no brand SonyEricsson in the API, the correct name would have been just Ericsson. Let's say that we want to take all of the device information that we stored in `brand_devices`, a list of `Devices` object, and create a single Pandas DataFrame:

```python
import pandas as pd
columns = ['Brand', 'DeviceName', 'announced', 'talk_time']
brand_devices = [devices.dataframe(columns) for devices
                 in brand_devices if devices.not_null]
all_brands = pd.concat(brand_devices)
print(all_brands)
```

Brand | DeviceName | announced | talk_time |
| --- | --- | --- | --- | --- |
| 0 | Apple | Apple iPad Pro 12.9 | 2017, June | Up to 10 h (multimedia) |
| 1 | Apple | Apple iPad Pro 10.5 | 2017, June | Up to 10 h (multimedia) |
| 2 | Apple | Apple iPad 9.7 | 2017, March | Up to 10 h (multimedia) |
| 0 | Samsung | Samsung Galaxy Tab A 8.0 (2017) | Not announced yet | NaN |
| 1 | Samsung | Samsung Galaxy C10 | Not announced yet | NaN |
| 2 | Samsung | Samsung Galaxy J5 (2017) | 2017, June | Up to 21 h (3G) |
| 0 | LG | LG V30 | Not announced yet | NaN |
| 1 | LG | LG X venture | 2017, May | Up to 24 h (3G) |
| 2 | LG | LG Stylo 3 Plus | 2017, May | Up to 14 h (3G) |
| 0 | Huawei | Huawei MediaPad M3 Lite 8 | 2017, June | NaN |
| 1 | Huawei | Huawei Honor 9 | 2017, June | NaN |
| 2 | Huawei | Huawei nova 2 plus | 2017, May | NaN |

## Tests

Pass a valid API token to `py.test` to run the package's unit tests.

```bash
py.test --apitoken <TOKEN>
```
