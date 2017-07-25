"""fonoapi.py - includes the FonoApi class for accessing Freshpixl's Fono Api.
"""

from __future__ import print_function
import json
import numpy as np
import pandas as pd
import requests


################################################################################
# Custom exceptions
################################################################################


class InvalidAPITokenException(Exception):
    """User tried to use an invalid API token.
    """
    pass


class StatusCodeErrorNon200Exception(Exception):
    """Requests.post returned a non-200 HTTP status code.
    """
    pass


class StatusCodeError200Exception(Exception):
    """Requests.post returned a 200 HTTP status code, but there was an error
    associated with the status code.
    """
    pass


class NoAPIResultsException(Exception):
    """No results returned from the API. This exception is only raised when the
    user sets the no_results_exception argument to true in the getdevice or
    getlatest methods.
    """
    pass


################################################################################
# Phones class - the FonoAPI class outputs objects of this class
################################################################################


class Phones(object):
    """Phones - takes a list of dictionaries, where each element in the list is
    a particular mobile phone, and each key/vaue pair in each dictionary is an
    attribute and value about the phone, and creates an object that makes it
    easy to extract information about the mobile phones.
    """


    # Likely all of the API attributes. I came up with a list of the most common
    # brands, ran .getdevice for each, and took the union of the resulting keys
    _all_attributes = [
        u'Brand',
        u'DeviceName',
        u'_2g_bands',
        u'_3_5mm_jack_',
        u'_3g_bands',
        u'_4g_bands',
        u'alert_types',
        u'announced',
        u'audio_quality',
        u'battery_c',
        u'bluetooth',
        u'body_c',
        u'browser',
        u'build',
        u'call_records',
        u'camera',
        u'camera_c',
        u'card_slot',
        u'chipset',
        u'colors',
        u'cpu',
        u'dimensions',
        u'display',
        u'display_c',
        u'edge',
        u'features',
        u'features_c',
        u'games',
        u'gprs',
        u'gps',
        u'gpu',
        u'infrared_port',
        u'internal',
        u'java',
        u'keyboard',
        u'loudspeaker',
        u'loudspeaker_',
        u'memory_c',
        u'messaging',
        u'multitouch',
        u'music_play',
        u'network_c',
        u'nfc',
        u'os',
        u'performance',
        u'phonebook',
        u'price',
        u'primary_',
        u'protection',
        u'radio',
        u'resolution',
        u'sar',
        u'sar_eu',
        u'sar_us',
        u'secondary',
        u'sensors',
        u'sim',
        u'size',
        u'sound_c',
        u'speed',
        u'stand_by',
        u'status',
        u'talk_time',
        u'technology',
        u'type',
        u'usb',
        u'video',
        u'weight',
        u'wlan'
    ]


    def __init__(self, phones, **kwargs):
        """Initialize the Phones object.

        Parameters
        ----------
        phones : list of dictionaries
            The list of dictionaries where each dictionary corresponds to a
            mobile phone, and the dictionary contains phone attributes. An empty
            list corresponds to no resuls returned from the API.

        kwargs : Dict (optional)
            A dict of keyword arguments to the .getdevice or .getlatest methods.
            Does not serve an explicit purpose, but can be useful when looking
            at Phones objects who are null, and determining what keyword
            arguments were passed to .getdevice or .getlatest that resulted in a
            null object. See the kwargs by using the input_parameters class
            attribute.

        Returns
        -------
        self : Phones object
            Return self
        """
        assert isinstance(phones, list)

        # If phones is an empty list, set self.not_null/null appropriately
        if phones:
            assert all([isinstance(obj, dict) for obj in phones])
            self.not_null, self.null = True, False
        else:
            self.not_null, self.null = False, True
        self.input_parameters, self.phones = kwargs, phones


    def keys_union(self):
        """Get the union of the sets of keys in each dictionary that is part of
        the self.phones list of dictionaries.
        """
        list_of_keys = [dict_.keys() for dict_ in self.phones]
        columns = reduce(lambda x, y: set(x).union(set(y)), list_of_keys)
        return sorted(columns)


    def list_of_dicts(self):
        """Return exactly what comes out of the API - a list of dictionaries.
        In cases where this object is null, an empty list will be returned.

        Returns
        -------
        lod - a list of dictionaries, where elements in the list corresponds to
            mobile phones, and key/value pairs in the dictionaries correspond to
            attributes about those phones.
        """
        return self.phones


    def list_of_lists(self, columns=None):
        """Create a list of lists, where each sublist is a row of information
        for a particular phone.

        Parameters
        ----------
        columns - list of strings
            The specific attributes to include in each sublist. If a mobile
            phone (represented as a sublist, aka a row) is missing a specific
            attribute, there will be a value of None in the position in the
            sublist corresponding to that specific attribute. If left blank, the
            entire list of 69 possible attributes will be used as columns (see
            them with the _all_attributes class attribute).

        Returns
        -------
        lol - a list of lists, where each sublist is basically a row
        """
        if self.null:
            return self.phones, []
        if columns is None:
            columns = self._all_attributes
        rows = []
        for phone in self.phones:
            row = []
            for column in columns:
                row.append(phone.get(column))
            rows.append(row)
        return rows, columns


    def dataframe(self, columns=None):
        """Constructs a Pandas DataFrame where columns correspond to attributes.

        Parameters
        ----------
        columns - list of strings
            The specific attributes to include in each sublist. If a mobile
            phone (represented as a sublist, aka a row) is missing a specific
            attribute, there will be a value of None in the position in the
            sublist corresponding to that specific attribute. If left blank, the
            entire list of 69 possible attributes will be used as columns (see
            them with the _all_attributes class attribute).

        Returns
        -------
        df - a Pandas DataFrame
        """
        if self.null:
            pd.DataFrame(self.phones)
        rows, columns = self.list_of_lists(columns=columns)
        return pd.DataFrame(rows, columns=columns).fillna(value=np.nan)


    def __str__(self):
        string = '| Phones Object: mobile device data|'
        string += '\n------------------------------------'
        string += '\nNumber of phones : {}'.format(str(len(self.phones)))
        string += '\nInput parameters : {}'.format(str(self.input_parameters))
        return string


    __repr__ = __str__


################################################################################
# FonoAPI - the main class for this package
################################################################################


class FonoAPI(object):
    """FonoApi - class for accessing Freshpixl's Fono API. The Fono API provides
    device attributes for mobile phones. Example attributes include model,
    brand, CPU info, GPU info, release date, and more. Learn more at
    https://fonoapi.freshpixl.com/.
    """


    def __init__(self, api_key, api_url='https://fonoapi.freshpixl.com/v1/'):
        """Initialize the FonApi object.

        Parameters
        ----------
        api_key : string
            The API token. Generate a new token at:
            https://fonoapi.freshpixl.com/token/generate

        api_url : string (optional)
            URL of the API. The default should work.

        Returns
        -------
        self : FonoAPI object
            Return self
        """
        self.api_key = api_key
        self.api_url = api_url


    def getdevice(self, device, position=None, brand=None,
                  no_results_exception=False, verbose=True):
        """Given the name of a device (does not need to be an exact name),
        return device informaton from the Fono API in the form of a Phone
        object.

        Parameters
        ----------
        device : string
            Pass nearly relevent mobile device name (example : "i9305", "A8").
            Note: this might result multiple results at a time

        position : integer (optional)
            When a set of results is returned you can get a specific device by
            passing the position of your device on the result set. Count starts
            from 0

        brand : string (optional)
            Pass the Mobile Device Brand (example : "samsung", "htc")

        no_results_exception : boolean (default is False)
            If set to True, if no results are returned from the API, an
            NoAPIResultsException is raised. If False, no API results will lead
            to a Phone object whose not_null attribute is False and whose null
            attribute is True.

        verbose : boolean (default is True)
            If set to True, when no results are returned by the API print out
            the name of the device that lead to no results.

        Returns
        -------
        phones : Phones object
            API results
        """
        assert isinstance(device, str)
        if brand:
            assert isinstance(brand, str)
        url = self.api_url + 'getdevice'
        postdata = {
            'brand'    : brand,
            'device'   : device,
            'position' : position,
            'token'    : self.api_key
        }
        headers = {
            'content-type': 'application/json'
        }
        result = self.process_request(url, postdata, headers,
                                      no_results_exception)
        phones = Phones(result, device=device, position=position, brand=brand)
        if verbose:
            if phones.null:
                print(('Could not retrieve device information for device'
                       ' {} from the Fono API').format(device))
        return phones


    def getlatest(self, brand, limit=100, no_results_exception=False,
                  verbose=True):
        """Given the name of a device (does not need to be an exact name),
        return device informaton from the Fono API in the form of a Phone
        object.

        Parameters
        ----------
        brand : string
            Pass the Mobile Device Brand (example : "samsung", "htc")

        limit : int i, where 1 <= i <= 100 (default is 100)
            Number of results returned

        no_results_exception : boolean (default is False)
            If set to True, if no results are returned from the API, an
            NoAPIResultsException is raised. If False, no API results will lead
            to a Phone object whose not_null attribute is False and whose null
            attribute is True.

        verbose : boolean (default is True)
            If set to True, when no results are returned by the API print out
            the name of the device that lead to no results.

        Returns
        -------
        phones : Phones object
            API results
        """
        assert isinstance(brand, str)
        assert 1 <= limit <= 100, 'Limit must be between 1 and 100'
        url = self.api_url + 'getlatest'
        postdata = {
            'brand' : brand,
            'limit' : limit,
            'token' : self.api_key
        }
        headers = {
            'content-type': 'application/json'
        }
        result = self.process_request(url, postdata, headers,
                                      no_results_exception)
        phones = Phones(result, brand=brand, limit=limit)
        if verbose:
            if phones.null:
                print(('Could not retrieve brand information for brand'
                       ' {} from the Fono API.').format(brand))
        return phones


    @staticmethod
    def http_exception_message(status_code, result_json):
        """Craft a short Exception message given an HTTP status code, error, and
        message.
        """
        error = result_json['status']
        message = result_json['message']
        return 'HTTP Exception: Status code: {}; Error: {}, Message: {}'.format(
            status_code, error, message)


    def process_request(self, url, postdata, headers,
                        no_results_exception=False):
        """Uses the requests library to call the Fono API.
        """
        result = requests.post(
            url, data=json.dumps(postdata), headers=headers)
        invalid_token = ('Invalid or Blocked Token. Generate a Token at '
                         'fonoapi.freshpixl.com')
        no_results = 'No Matching Results Found.'
        status_code = result.status_code
        result_json = result.json()

        # If the HTTP status code is not 200 (OK), raise an Exception
        if status_code != 200:
            StatusCodeErrorNon200Exception(self.http_exception_message(
                status_code, result_json))

        # If the result json is a dictionary, some problem happened
        if isinstance(result_json, dict):
            result_message = result_json['message']
            if result_message == invalid_token:
                message = 'Your API token, {}, is not valid'.format(
                    self.api_key)
                raise InvalidAPITokenException(message)
            elif result_message == no_results:
                if no_results_exception:
                    raise NoAPIResultsException('No results found in the API')
                else:
                    return []
            else:
                raise StatusCodeError200Exception(self.http_exception_message(
                    status_code, result_json))

        # If the result json is a list it means that we got results
        elif isinstance(result_json, list):
            if result_json == [[]]:
                if no_results_exception:
                    raise NoAPIResultsException('No results found in the API')
                else:
                    return []
            return result_json

        # If the result json isn't a list/dict :(
        else:
            raise Exception(
                'Requets returned an object that is not a list or a dict')


    def __str__(self):
        string = '| FonoAPI Object: Use to connect to the FonoApi |'
        string += '\n-------------------------------------------------'
        string += '\nAPI URL   : {}'.format(self.api_url)
        string += '\nAPI Token : {}'.format(self.api_key)
        return string


    __repr__ = __str__
