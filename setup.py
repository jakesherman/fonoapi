from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))


# Create a long description
# Copied code here from: https://github.com/kdheepak/fono
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    with open(path.join(here, 'README.md')) as f:
        long_description = f.read()


from pip.req import parse_requirements
install_requires = [str(ir.req) for ir in parse_requirements(
    path.join(here, 'requirements.txt'), session=False)]


__title__ = 'fonoapi'
__summary__ = "Access Freshpixl's Fono Api to gain insight into mobile phones"
__uri__ = 'https://github.com/jakesherman/fonoapi'
__author__ = 'shakee93, jesusperiago, jakesherman'
__email__ = 'jake@jakesherman.com'
__license__ = 'MIT License'
__copyright__ = '2016-2017 shakee93, jesusperiago, jakesherman'
__version__ = '0.1.2'


setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    long_description=long_description,
    license=__license__,
    url=__uri__,
    author=__author__,
    author_email=__email__,
    packages=['fonoapi'],
    install_requires=install_requires,
    download_url='{}/archive/v{}.tar.gz'.format(
        __uri__, __version__),
    keywords=['api', 'mobile', 'phone', 'FonoApi']
)
