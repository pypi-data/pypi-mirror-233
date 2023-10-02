# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['annas_py', 'annas_py.extractors', 'annas_py.models']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.12.2,<5.0.0',
 'lxml>=4.9.3,<5.0.0',
 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'annas-py',
    'version': '0.1.0',
    'description': "Anna's Archive unofficial client based on web scrapping",
    'long_description': '# annas-py\n\nAnna\'s Archive unofficial client library based on web scrapping\n\n## Usage\n\nInstall by running:\n\n```bash\npip install annas-py\n```\n\nUsage example:\n\n```python\nimport annas_py\n\nresults = annas_py.search("python", language=annas_py.models.args.Language.EN)\nfor r in results:\n    print(r.title)\n\ninformation = annas_py.get_informations(results[0].id)\nprint("Title:", information.title)\nprint("Description:", information.description)\nprint("Links:", information.urls)\n```\n',
    'author': 'Dheison Gomes',
    'author_email': 'dheisomgomes0@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
