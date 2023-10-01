from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = "Package accelerateur de developpement sur python à l'aide de FLASK"
LONG_DESCRIPTION = "Il s'agit d'un package multi fonction qui augmente la vitesse de réalisation avec FLASK après une configuration simple et minutieuse"

# Setting up
setup(
       # the name must match the folder name 'hivipy'
        name="hivipy", 
        version=VERSION,
        author="BILONG NTOUBA Célestin",
        author_email="bilongntouba.celestin@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "Flask[async];python_version>='2.1.2'",
            # "flask[async];python_version>=''",
            "Flask-Cors;python_version>='3.0.10'",
            "flask-ipban;python_version>='1.1.5'",
            "Flask-IPFilter;python_version>='0.0.5'",
            "Flask-Limiter;python_version>='2.4.6'",
            "Flask-WeasyPrint;python_version>='0.6'",
            "Flask-Session;python_version>='0.4.0'",
            "configparser;python_version>='5.2.0'",
            "xmltodict;python_version>='0.13.0'",
            "pytz;python_version>='2022.1'",
            "typing;python_version>='3.7.4.3'",
            "SQLAlchemy;python_version>='1.4.39'",
            "sqlalchemy-utils;python_version>='0.38.3'",
            "pg8000;python_version>='1.29.1'",
            "pymysql;python_version>='1.0.2'",
            "asyncio;python_version>='3.4.3'",
            "python-dateutil;python_version>='2.8.2'",
            "pandas;python_version>='1.4.3'",
            "pyexcel_xls;python_version>='0.7.0'",
            "pyexcel_xlsx;python_version>='0.6.0'",
            "weasyprint;python_version>='55.0'",
            "qrcode;python_version>='7.3.1'",
            "alembic;python_version>='1.8.0'",
            "pycryptodome;python_version>='3.15.0'",
            "openpyxl;python_version>='3.0.10'",
            # "pyjwt;python_version>='2.4.0'",
            "vulture;python_version>='2.5'",
            "pdoc3;python_version>='0.10.0'",
            "pygeoip;python_version>='0.3.2'",
            "tinydb;python_version>='4.7.0'",
            "pymongo;python_version>='4.2.0'",
            "Jinja2;python_version>='3.1.2'",
            "python-datauri;python_version>='1.1.0'",
            "twilio;python_version>='7.16.0'",
            "google-currency;python_version>='1.0.10'",

            "jonschema;python_version>='0.0.2'"
        ],
        
        keywords=['python', 'flask', 'headless-cms', 'package'],
        classifiers= [
            # "Headless CMS :: package :: Digibehive",
        ]
)