"""test_fonoapi.py - general tests of the fonoapi package.
"""

import fonoapi
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
