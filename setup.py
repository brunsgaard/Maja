from setuptools import setup, find_packages
from os.path import dirname, join
import ocid


def readfile(filename):
    with open(join(dirname(__file__), filename), 'r') as f:
        return f.read()

setup(
    name="ocid",
    description="SSO solution for OnlineCity services",
    install_requires=[
        'Flask',
        'Flask-CORS',
        'Flask-Sqlalchemy',
        'psycopg2',
        'uwsgi',
        'requests',
        'Flask-Cache',
        'babel',
        'pytz',
        'simplejson',
        'jsonschema',
        'Flask-Ocid',
        'Flask-Jsonschema',
    ],
    keywords="oc",
    package_data={
        'ocid': ['schemas/*.json'],
    },
    long_description=readfile("README.rst"),
    url="http://id.oc.dk",
    version=ocid.__version__,
    packages=find_packages(),
    maintainer="Jonas Brunsgaard",
    maintainer_email="jonas.brunsgaard@gmail.com",
)
