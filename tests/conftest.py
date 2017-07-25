"""conftest.py - pytest configuration
"""

import pytest


################################################################################
# Create the apitoken command line parameter (SO #40880259)
# -- While it isn't great practice to make unit tests not self-contained, I
# -- don't want to share a working API token in this package
################################################################################


def pytest_addoption(parser):
    parser.addoption('--apitoken', action='store', default='ABC')


def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.apitoken
    if 'apitoken' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize('apitoken', [option_value])
