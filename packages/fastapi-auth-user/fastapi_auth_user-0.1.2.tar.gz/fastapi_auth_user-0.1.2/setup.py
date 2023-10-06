# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi-auth-user',
 'fastapi-auth-user.auth',
 'fastapi-auth-user.config',
 'fastapi-auth-user.database',
 'fastapi-auth-user.models',
 'fastapi-auth-user.page',
 'fastapi-auth-user.users']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.12.0,<2.0.0',
 'bcrypt>=4.0.1,<5.0.0',
 'fastapi>=0.95.0,<0.96.0',
 'jinja2>=3.1.2,<4.0.0',
 'passlib>=1.7.4,<2.0.0',
 'psycopg2-binary>=2.9.7,<3.0.0',
 'psycopg2>=2.9.7,<3.0.0',
 'pyjwt>=2.6.0,<3.0.0',
 'python-decouple>=3.8,<4.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'python-jose>=3.3.0,<4.0.0',
 'python-multipart>=0.0.6,<0.0.7',
 'sqlalchemy>=2.0.8,<3.0.0',
 'uvicorn>=0.21.1,<0.22.0']

entry_points = \
{'console_scripts': ['start = fastapi-auth-user.__main__:app']}

setup_kwargs = {
    'name': 'fastapi-auth-user',
    'version': '0.1.2',
    'description': 'auth user',
    'long_description': '<p align="center">\n <img width="100px" src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI">\n</p>\n<p align="center">\n    <em>Default auth service based on FastApi framework</em>\n</p>',
    'author': 'Vittalius',
    'author_email': 'Vittalius@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
