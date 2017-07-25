# fonoapi - Python wrapper for FonoApi, providing mobile device descriptions

https://fonoapi.freshpixl.com/

The Fono API is an API which can provide mobile device descriptions such as model, brand, cpu, gpu, dimensions, release date, and more. This Python package provides easy access to the Fono API with the `requests` package.  

### Installation

```bash
pip install git+https://github.com/jakesherman/fonoapi.git
```

## Tutorial

Before starting, make sure to install this package (see above) and [generate an API token](https://fonoapi.freshpixl.com/token/generate#). We are going to start by creating a `FonoAPI` object, which we pass our API token to  order to start interacting with the Fono Api.

```python
from __future__ import print_function  # -- for Python 2.7
from fonoapi import FonoAPI
fon = FonoAPI('TOKEN')
```

### Getting devices matching a specific device name

Now, let's imagine that we have a specific mobile device in mind, say, the **iPhone 7**, and we are interested in learning more about this device. We can use the `getdevice` method to call the Fono Api

```python
device = 'iPhone 7'
iPhone_7 = fon.getdevice(device)
print(iPhone_7)
```

    | Phones Object: mobile device data|
    ------------------------------------
    Number of phones : 4
    Input parameters : {'device': 'iPhone 7', 'position': None, 'brand': None}

The `getdevice` method returns a `Phones` object, an object that makes it easy to retrieve data from the Fono Api. Printing out the object gives us information on how many phones we retrieved information for, and what the parameters were to `getdevice` that created the `Phones` object.

We can output the data in the `Phones` object in three ways:
- As a list of dictionaries via the `list_of_dicts` method, with one dictionary per phone
- As a list of lists via the `list_of_lists` method, where each sublist corresponds to a particular phone
- As a Pandas DataFrame via the `dataframe` method, where each row corresponds to a particular phone

Not all mobile phones in the Fono Api have every attribute associated with them (suppose some phones had CPU information associated with them, and some didn't). In the case of `list_of_dicts`, only the attributes associated with each phone is included in each phone's dictionary. In the cases of `list_of_lists` or `dataframe`, you may choose specific columns to include for every phone. In this case, devices with no value for a particular column will have values of `None` or `numpy.nan`, respectively.

In our case, let's look at the attributes `Brand, DeviceName, body_c` for the phones returned by our API call:

```python
print(iPhone_7.dataframe(['Brand', 'DeviceName', 'body_c']))
```

<div>
<table border="1">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Brand</th>
      <th>DeviceName</th>
      <th>body_c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Prestigio</td>
      <td>Prestigio MultiPhone 7500</td>
      <td>None</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Prestigio</td>
      <td>Prestigio MultiPhone 7600 Duo</td>
      <td>None</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Apple</td>
      <td>Apple iPhone 7 Plus</td>
      <td>- IP67 certified - dust and water resistant\r\...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Apple</td>
      <td>Apple iPhone 7</td>
      <td>- IP67 certified - dust and water resistant\r\...</td>
    </tr>
  </tbody>
</table>
</div>

Two interesting things come up:
- There are two non-Apple phones by Prestigio in the list! The model names of the two phones begin with Prestigio Mult**iPhone 7**500, so it's understandable that they would show up if we searched for the string 'iPhone 7'
- The two Prestigio phones don't have a value for the `body_c` attribute, so they have `np.nan` values for that column

In order to get rid of the Prestigio phones in our results, all we have to do is specify the `brand` argument to the `getdevice` method

```python
device, brand = 'iPhone 7', 'Apple'
iPhone_7 = fon.getdevice(device, brand)
print(iPhone_7.dataframe(['Brand', 'DeviceName', 'body_c']))
```

<div>
<table border="1">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Brand</th>
      <th>DeviceName</th>
      <th>body_c</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Apple</td>
      <td>Apple iPhone 7 Plus</td>
      <td>- IP67 certified - dust and water resistant\r\...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Apple</td>
      <td>Apple iPhone 7</td>
      <td>- IP67 certified - dust and water resistant\r\...</td>
    </tr>
  </tbody>
</table>
</div>

### Getting the latest devices for a specific brand

`getlatest` will return information about the most recent phones for a given brand. For example, let's imagine that we wish to get data on the last 5 mobile devices from Apple.

```python
brand = 'Apple'
latest_apples = (
    fon
    .getlatest(brand, limit=5)
    .dataframe(['DeviceName', 'announced', '_3_5mm_jack_', 'talk_time'])
)
print(latest_apples)
```

<div>
<table border="1">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DeviceName</th>
      <th>announced</th>
      <th>_3_5mm_jack_</th>
      <th>talk_time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Apple iPad Pro 12.9</td>
      <td>2017, June</td>
      <td>Yes</td>
      <td>Up to 10 h (multimedia)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Apple iPad Pro 10.5</td>
      <td>2017, June</td>
      <td>Yes</td>
      <td>Up to 10 h (multimedia)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Apple iPad 9.7</td>
      <td>2017, March</td>
      <td>Yes</td>
      <td>Up to 10 h (multimedia)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Apple iPhone 8</td>
      <td>Not announced yet</td>
      <td>No</td>
      <td>None</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Apple Watch Series 1 Sport 42mm</td>
      <td>2016, September</td>
      <td>No</td>
      <td>Up to 3 h 40 min</td>
    </tr>
  </tbody>
</table>
</div>


## Tests

Pass a valid API token to `py.test` to run the package's unit tests.

```bash
py.test --apitoken <TOKEN>
```

## Credit

The [PHP class used to connect to the API](https://github.com/shakee93/fonoapi) was developed Shakeeb Sadikeen. I forked a Python package that jesusperiago created, adding the `getlatest` method, and making other changes to organize this code into a package that could become available on `PyPI`.
