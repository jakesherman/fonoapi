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


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_requires = parse_requirements('requirements.txt')


__title__ = 'fonoapi'
__summary__ = "Access Freshpixl's Fono Api to gain insight into mobile phones"
__uri__ = 'https://github.com/jakesherman/fonoapi'
__author__ = 'shakee93, jesusperiago, jakesherman'
__email__ = 'jake@jakesherman.com'
__license__ = 'MIT License'
__copyright__ = '2016-2019 shakee93, jesusperiago, jakesherman'
__version__ = '0.1.4'


setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    long_description=long_description,
    long_description_content_type='text/markdown',
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
