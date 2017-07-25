from os import path
from setuptools import setup
import fonoapi

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


setup(
    name=fonoapi.__title__,
    version=fonoapi.__version__,
    description=fonoapi.__summary__,
    long_description=long_description,
    license=fonoapi.__license__,
    url=fonoapi.__uri__,
    author=fonoapi.__author__,
    author_email=fonoapi.__email__,
    packages=['fonoapi'],
    install_requires=install_requires,
    download_url='{}/archive/v{}.tar.gz'.format(
        fonoapi.__uri__, fonoapi.__version__),
    keywords=['api', 'mobile', 'phone', 'FonoApi']
)
