from setuptools import setup, find_packages

VERSION = '0.0.0' 
DESCRIPTION = "Package de manipulation des bases des données"
LONG_DESCRIPTION = "Il s'agit d'un package permet de manipuler plus aisement les bases de données"

# Setting up
setup(
       # the name must match the folder name 'jon'
        name="hiviorm", 
        version=VERSION,
        author="BILONG NTOUBA Célestin",
        author_email="bilongntouba.celestin@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "pytz;python_version>='2022.1'",
            "typing;python_version>='3.7.4.3'",
            "asyncio;python_version>='3.4.3'",
            "jonschema;python_version>='0.0.2'",

            "pg8000;python_version>='1.29.1'",
            "pymysql;python_version>='1.0.2'",
            "tinydb;python_version>='4.7.0'",
            "pymongo;python_version>='4.2.0'",
        ],
        
        keywords=['python', 'jon', 'schema', 'validation'],
        classifiers= [
            # "Headless CMS :: package :: Digibehive",
        ]
)