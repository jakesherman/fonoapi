# coding=utf-8

"""test_fonoapi.py - general tests of the fonoapi package.
"""

import fonoapi
import pandas as pd
import pytest


################################################################################
# Ensure that an exception is raised when giving a bad API token
################################################################################


def raise_InvalidAPITokenException():
    """Goal is to raise an InvalidAPITokenException by initializing a FonoAPI
    object with a bad token.
    """
    fon = fonoapi.FonoAPI('ABC')
    return fon.getdevice(device='iPhone 7', brand='Apple')


def test_InvalidAPITokenException():
    with pytest.raises(fonoapi.InvalidAPITokenException):
        raise_InvalidAPITokenException()


################################################################################
# Ensure that proper exceptions are raised when no results are returned
################################################################################


def raise_NoAPIResultsException1(token):
    """Goal is to raise an NoAPIResultsException by choosing a device name that
    is clearly non-existant.
    """
    fon = fonoapi.FonoAPI(token)
    return fon.getdevice(device='madeupcellphone', no_results_exception=True)


@pytest.mark.unit
def test_NoAPIResultsException1(apitoken):
    with pytest.raises(fonoapi.NoAPIResultsException):
        raise_NoAPIResultsException1(apitoken)


def raise_NoAPIResultsException2(token):
    """Goal is to raise an NoAPIResultsException by choosing a brand name that
    is clearly non-existant.
    """
    fon = fonoapi.FonoAPI(token)
    return fon.getlatest(brand='madeupbrand', no_results_exception=True)


@pytest.mark.unit
def test_NoAPIResultsException2(apitoken):
    with pytest.raises(fonoapi.NoAPIResultsException):
        raise_NoAPIResultsException2(apitoken)


################################################################################
# Some random tests to ensure that the API is working ...
################################################################################


def expected_result1():
    """Expected results functions return the following:
    1) Method to call on the FonoAPI object, 2) Kwargs to that method,
    3) Method to call on the results, 4) Kwargs to the second method,
    5) The expected output.
    """
    method1, method1_kwargs = 'getdevice', {'device':'LG Stylo 3 Plus'}
    method2, method2_kwargs = 'list_of_dicts', {}
    output = [{
        u'DeviceName': u'LG Stylo 3 Plus',
        u'Brand': u'LG',
        u'technology': u'GSM / HSPA / LTE',
        u'gprs': u'Yes',
        u'edge': u'Yes',
        u'announced': u'2017, May',
        u'status': u'Available. Released 2017, May',
        u'dimensions': u'155.7 x 79.8 x 7.4 mm (6.13 x 3.14 x 0.29 in)',
        u'weight': u'150 g (5.29 oz)',
        u'sim': u'Nano-SIM',
        u'type': u'IPS LCD capacitive touchscreen, 16M colors',
        u'size': u'5.7 inches, 89.6 cm2 (~72.1% screen-to-body ratio)',
        u'resolution': u'1080 x 1920 pixels, 16:9 ratio (~386 ppi density)',
        u'card_slot': u'microSD, up to 256 GB',
        u'alert_types': u'Vibration; MP3, WAV ringtones',
        u'loudspeaker_': u'Yes',
        u'wlan': u'Wi-Fi 802.11 b/g/n, WiFi Direct, hotspot',
        u'bluetooth': u'4.2, A2DP, LE',
        u'gps': u'Yes, with A-GPS',
        u'radio': u'To be confirmed',
        u'usb': u'microUSB 2.0',
        u'messaging': u'SMS(threaded view), MMS, Email, Push Mail, IM',
        u'browser': u'HTML5',
        u'java': u'No',
        u'features_c': u'- MP4/H.264 player\r\n  - MP3/WAV/eAAC+ player\r\n  - Photo/video editor\r\n  - Document viewer',
        u'battery_c': u'Li-Ion 3080 mAh battery',
        u'stand_by': u'Up to 456 h (3G)',
        u'talk_time': u'Up to 14 h (3G)',
        u'colors': u'Titan',
        u'sensors': u'Fingerprint (rear-mounted), accelerometer, gyro, proximity, compass',
        u'cpu': u'Octa-core 1.4 GHz Cortex-A53',
        u'internal': u'32 GB, 2 GB RAM',
        u'os': u'Android 7.0 (Nougat)',
        u'body_c': u'- Stylus',
        u'primary_': u'13 MP (1/3", 1.12 Âµm), autofocus, LED flash',
        u'video': u'1080p@30fps',
        u'secondary': u'5 MP, LED flash',
        u'speed': u'HSPA 42.2/5.76 Mbps, LTE-A (2CA) Cat6 300/50 Mbps',
        u'chipset': u'Qualcomm MSM8940 Snapdragon 435',
        u'features': u'Geo-tagging, touch focus, face detection',
        u'gpu': u'Adreno 505',
        u'multitouch': u'Yes',
        u'nfc': u'Yes',
        u'price': u'About 260 EUR',
        u'_2g_bands': u'GSM 850 / 900 / 1800 / 1900 ',
        u'_3_5mm_jack_': u'Yes',
        u'_3g_bands': u'HSDPA 850 / 1700(AWS) / 1900 / 2100 ',
        u'_4g_bands': u'LTE band 2(1900), 4(1700/2100), 5(850), 12(700), 66(1700/2100)'
    }]
    return method1, method1_kwargs, method2, method2_kwargs, output


def expected_result2():
    """See expected_result1 docstring.
    """
    method1, method1_kwargs = 'getdevice', {
        'device':'iPhone 7',
        'brand':'Apple'
    }
    method2, method2_kwargs = 'list_of_lists', {
        'columns':['Brand', 'DeviceName', 'alert_types', 'battery_c']
    }
    output = (
        [
            [
                u'Apple',
                u'Apple iPhone 7 Plus',
                u'Vibration, proprietary ringtones',
                u'Non-removable Li-Ion 2900 mAh battery (11.1 Wh)'
                ],
            [
                u'Apple',
                u'Apple iPhone 7',
                u'Vibration, proprietary ringtones',
                u'Non-removable Li-Ion 1960 mAh battery (7.45 Wh)'
                ]
            ],
        ['Brand', 'DeviceName', 'alert_types', 'battery_c']
        )
    return method1, method1_kwargs, method2, method2_kwargs, output


def expected_result3():
    """See expected_result1 docstring.
    """
    method1, method1_kwargs = 'getdevice', {'device':'Huawei Honor 9'}
    method2, method2_kwargs = 'dataframe', {
        'columns':['Brand', 'DeviceName', 'alert_types', 'announced']
    }
    output = pd.DataFrame({
        u"Brand": [u"Huawei"] * 2,
        u"DeviceName": [u"Huawei Honor 9", u"Huawei Honor 9 Lite"],
        u"alert_types": [u"Vibration; MP3, WAV ringtones"] * 2,
        u"announced": [u"2017, June", u"2017, December"]
    })
    return method1, method1_kwargs, method2, method2_kwargs, output


def expected_result4():
    """See expected_result1 docstring.
    """
    method1, method1_kwargs = 'getlatest', {'brand':'LG', 'limit':10}
    method2, method2_kwargs = 'list_of_lists', {'columns':['Brand']}
    output = (
        [
            [u'LG'],
            [u'LG'],
            [u'LG'],
            [u'LG'],
            [u'LG'],
            [u'LG'],
            [u'LG'],
            [u'LG'],
            [u'LG'],
            [u'LG']],
        ['Brand']
        )
    return method1, method1_kwargs, method2, method2_kwargs, output


@pytest.mark.unit
def test_expected_results(apitoken):
    """Test the methods of FonoAPI against expected results for a few specific
    test cases.
    """
    fon = fonoapi.FonoAPI(apitoken)
    results_funcs = [expected_result1, expected_result2, expected_result3,
                     expected_result4]
    for results_func in results_funcs:
        method1, method1_kwargs, method2, method2_kwargs, expected_output = \
            results_func()
        tested_method1 = getattr(fon, method1)(**method1_kwargs)
        tested_method2 = getattr(tested_method1, method2)(**method2_kwargs)
        if isinstance(expected_output, pd.DataFrame):
            assert expected_output.equals(tested_method2)
        else:
            assert expected_output == tested_method2
