# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['minifold']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4',
 'ldap3',
 'lxml',
 'pycountry',
 'pymongo',
 'requests',
 'requests-cache',
 'tweepy',
 'urllib3',
 'xmltodict']

setup_kwargs = {
    'name': 'minifold',
    'version': '0.10.0',
    'description': 'Minifold is a Python module able to interact with various data sources (e.g. CSV, LDAP, SQL, twitter, etc.) and to query/combine/aggregate them with database-like operators.',
    'long_description': '# Minifold\n\n[![PyPI](https://img.shields.io/pypi/v/minifold.svg)](https://pypi.python.org/pypi/minifold/)\n[![Build](https://github.com/nokia/minifold/workflows/build/badge.svg)](https://github.com/nokia/minifold/actions/workflows/build.yml)\n[![Documentation](https://github.com/nokia/minifold/workflows/docs/badge.svg)](https://github.com/nokia/minifold/actions/workflows/docs.yml)\n[![ReadTheDocs](https://readthedocs.org/projects/minifold/badge/?version=latest)](https://minifold.readthedocs.io/en/)\n[![codecov](https://codecov.io/gh/nokia/minifold/branch/master/graph/badge.svg?token=OZM4J0Y2VL)](https://codecov.io/gh/nokia/minifold)\n\n## Overview\n\n[Minifold](https://github.com/nokia/minifold.git) is a [Python](http://python.org/) module able to interact with various data sources (e.g. CSV, LDAP, SQL, twitter, etc.) and to query/combine/aggregate them with database-like operators.\n\n## Use cases\n\nThis framework has been in various Nokia projects. It also used in the [LINCS](https://www.lincs.fr) website to generate:\n\n* [trombinoscope](https://www.lincs.fr/people/)\n* [homepages](https://www.lincs.fr/people/?more=marc_olivier_buob)\n* [co-author graph](https://www.lincs.fr/research/lincs-graph/), thanks to [pyBGL](https://github.com/nokia/pybgl.git) and [GraphViz](http://graphviz.org/)\n\nFor more information, feel free to visit the [wiki](https://github.com/nokia/minifold/wiki):\n\n* [Overview](https://github.com/nokia/minifold/wiki/Overview)\n* [Installation](https://github.com/nokia/minifold/wiki/Installation)\n* [Tutorial](https://github.com/nokia/minifold/wiki/Tutorial)\n* [Design](https://github.com/nokia/minifold/wiki/Design)\n* [Configuration](https://github.com/nokia/minifold/wiki/Configuration)\n* [Framework](https://github.com/nokia/minifold/wiki/Framework)\n* [Tests](https://github.com/nokia/minifold/wiki/Tests)\n* [Packaging](https://github.com/nokia/minifold/wiki/Packaging)\n\n# License\n\nThis project is licensed under the BSD-3-Clause license - see the [LICENSE](https://github.com/nokia/minifold/blob/master/LICENSE).\n',
    'author': 'Marc-Olivier Buob',
    'author_email': 'marc-olivier.buob@nokia-bell-labs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
