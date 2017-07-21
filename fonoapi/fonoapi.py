"""fonoapi.py - includes the FonoApi class for accessing Freshpixl's Fono Api.
"""

import json
import requests


class FonoAPI(object):
    """FonoApi - class for accessing Freshpixl's Fono Api. This is an Api which
    can provide mobile device descriptions such as model, brand, cpu, gpu,
    dimensions, release date, etc. Learn more at https://fonoapi.freshpixl.com/.
    """


    def __init__(self, api_key, api_url='https://fonoapi.freshpixl.com/v1/'):
        """Initialize the FonApi object.
        :param api_key: API token. Generate a new token at
            https://fonoapi.freshpixl.com/token/generate
        :param api_url: (Optional) the URL to the API
        """
        self.api_key = api_key
        self.api_url = api_url


    def getdevice(self, device, position=None, brand=None):
        """Get device data object and return a json list
        :param device: Pass nearly relevent mobile device name
            (example : "i9305", "A8") this might result multiple results at a
            time
        :param position: (Optional) When a set of results is returned you can
            get a specific device by passing the position of your device on the
            result set. count starts from 0
        :param brand: Pass the Mobile Device Brand (example : "samsung", "htc")
        :return device list: List of dictionaries
        """
        url = self.api_url + 'getdevice'
        postdata = {'brand': brand,
                    'device': device,
                    'position': position,
                    'token': self.api_key}
        headers = {'content-type': 'application/json'}
        result = self.sendpostdata(url, postdata, headers)
        try:
            return result.json()
        except AttributeError:
            return result


    def getlatest(self, brand, limit=None):
        """Get latest data object and return a json list
        :param brand: Pass the Mobile Device Brand (example : "samsung", "htc")
        :param limit: Number of results returned (max and default is 100)
        :return device list: List of dictionaries
        """
        url = self.api_url + 'getlatest'
        postdata = {'brand': brand,
                    'limit': limit,
                    'token': self.api_key}
        headers = {'content-type': 'application/json'}
        result = self.sendpostdata(url, postdata, headers)
        try:
            return result.json()
        except AttributeError:
            return result


    @staticmethod
    def sendpostdata(url, postdata, headers, result=None):
        """Send data to the server
        :param url:
        :param postdata:
        :param headers:

        :return requests.post result:
        """
        try:
            result = requests.post(url, data=json.dumps(postdata),
                                   headers=headers)

            # Consider any status other than 2xx an error
            if not result.status_code // 100 == 2:
                return "Error status page: " + str(result)
            # Try send the result text else send the error
            try:
                if result.json()['status'] == 'error':

                    invalid_token_message = ('Invalid Token. Generate a Token '
                                             'at fonoapi.freshpixl.com.')
                    if result.json()['message'] == invalid_token_message:
                        return "Check api_key"

                return result.json()['message']
            except:
                pass

            return result
        except requests.exceptions.RequestException as e:
            # A serious problem happened, like an SSLError or InvalidURL
            return "Connect error. Check URL"
