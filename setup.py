from os import path
from setuptools import setup
import fonoapi

here = path.abspath(path.dirname(__file__))


# Create a long description
# Borrowed code here from: https://github.com/kdheepak/fono
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    with open(path.join(here, 'README.md')) as f:
        long_description = f.read()


setup(
    name=fonoapi.__title__,
    version=fonoapi.__version__,
    description=fonoapi.__summary__,
    long_description=long_description,
    license=fonoapi.__license__,
    url=fonoapi.__uri__,
    author=fonoapi.__author__,
    author_email=fonoapi.__email__,
    packages=['fonoapi']
)
