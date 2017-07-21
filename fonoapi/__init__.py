from fonoapi import FonoAPI


__all__ = (
    "__title__", "__summary__", "__uri__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__",
)


def __get_version():
    """Borrowed from Borrowed code here from: https://github.com/kdheepak/fono
    """
    from os import path
    here = path.abspath(path.dirname(__file__))
    return(open(path.join(here, 'version.py')).read())


exec(__get_version())


# Included in setup.py
__title__ = 'fonoapi'
__summary__ = "Access Freshpixl's Fono API to gain insight into mobile phones"
__uri__ = 'https://github.com/jakesherman/fonoapi'
__author__ = 'shakee93, jesusperiago, jakesherman'
__email__ = 'jake@jakesherman.com'
__license__ = 'MIT License'
__copyright__ = '2016, 2017 shakee93, jesusperiago, jakesherman'
