# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['volttron', 'volttron.services.web']

package_data = \
{'': ['*'],
 'volttron.services.web': ['static/*',
                           'static/js/*',
                           'static/specs/*',
                           'templates/*']}

install_requires = \
['PyJWT==1.7.1',
 'argon2-cffi>=21.3.0,<22.0.0',
 'jinja2-cli>=0.7.0',
 'passlib>=1.7.4,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'treelib>=1.6.1',
 'volttron>=10.0.5rc0,<11.0',
 'werkzeug>=2.1.2',
 'ws4py>=0.5.1']

setup_kwargs = {
    'name': 'volttron-lib-web',
    'version': '0.1.1a8',
    'description': 'The volttron-lib-web library extends the platform by exposing a web based REST api and allows extension web agents to register with the platform.',
    'long_description': 'This package provides web services for the VOLTTRON™ platform.\nThis includes a RESTful API for interacting with the platform\nand utility pages for administration and certificate management.\nThis library cannot be installed as a VOLTTRON agent is.\nRather, it must be installed as a python package.\n\n![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)\n![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)\n[![Run Pytests](https://github.com/eclipse-volttron/volttron-lib-web/actions/workflows/run-tests.yml/badge.svg)](https://github.com/eclipse-volttron/volttron-lib-web/actions/workflows/run-tests.yml)\n[![pypi version](https://img.shields.io/pypi/v/volttron-lib-web.svg)](https://pypi.org/project/volttron-lib-web/)\n\n# Requires\n\n* python >= 3.10\n* volttron >= 10.0\n* jinja2-cli >= 0.7.0\n* passlib >= 1.7.4\n* PyJWT == 1.7.1\n* treelib >= 1.6.1\n* werkzeug >= 2.1.2\n* ws4py = >= 0.5.1\n* requests >= 2.28.1\n* argon2-cffi >= 21.3.0\n\n## Installation\nThis library can be installed using pip:\n\n```bash\n> pip install volttron-lib-web\n```\n\nOnce the library is installed, VOLTTRON will not be able to start until the\nweb service is configured. Configurations for services, including this, reside\nin a service_config.yml file in the VOLTTRON_HOME directory\n(by default ~/.volttron/service_config.yml).\nIf this file does not already exist, create it. To configure the web service,\ninclude the following:\n\n```yaml\nvolttron.services.web:\n  enabled: true\n  kwargs:\n    bind_web_address: http://192.168.0.101:8080\n    web_secret_key: some_string # If not using SSL.\n    web_ssl_cert: /path/to/certificate # Path to the SSL certificate to be used by the web service. \n    web_ssl_key: /path/to/key # Path to the SSL secret key file used by web service.\n```\n\nAdditionally, in order to use many of the API endpoints, an instance name must be set in the VOLTTRON platform\nconfiguration file in VOLTTRON_HOME (by default ~/.volttron/config).  If this file does not already exist, create it.\nEnsure that it contains at least the following (where "my_instance_name" will be the name of this platform):\n\n```ini\n[volttron]\ninstance-name=my_instance_name\n```\n\nThe bind_web_address will typically be the IP address of the host on which the web service is installed.\nSetting the bind_web_address to 0.0.0.0 will bind to all interfaces on the machine. 127.0.0.1 or localhost\ncan be used if it is not desired for the web services to be reachable by other hosts. The port number\n(after the colon) can be any port which is not bound to another service on the host mahcine.\n80 or 8080 are common ports when not using SSL. 443 and 8443 are common ports to use when using SSL.\n\nIf using SSL, both web_ssl_certificate and web_ssl_key are required\nand web_secret_key should not be included. If SSL is not desired,\nprovide a web_secret_key instead and remove the lines for the web_ssl_cert\nand web_ssl_key. Any string can be used for the web_secret_key.\n\nFull VOLTTRON documentation is available at [VOLTTRON Readthedocs](https://eclipse-volttron.readthedocs.io/)\n\n\n## Use\nOnce the web service is installed, a web browser may be directed to the bind_web_address (http://192.168.1.101:8080\nin the case shown in the configuration) to reach an index page. An admin page is also available at the /admin path\nwhich can be used to create a username and password for authentication (http://192.168.1.101:8080/admin in the\nconfiguration shown above). This will create a file called web-users.json in the VOLTTRON_HOME directory.\n\nAdditionally, the web service provides a RESTful API which can be used by other applications. Full documentation for\nthe API is available on \n[Readthedocs](https://eclipse-volttron.readthedocs.io/en/latest/external-docs/volttron-lib-web/docs/source/index.html).\n\nNote that it is necessary for most API endpoints to have previously created a username and password for authentication\nby visiting the /admin page or by manually copying or creating a web-users.json file. Authentication can then be\nperformed by making a POST request to the /authenticate endpoint to obtain an access token. The access token should then\nbe included in any subsequent requests to the API by passing the token as a BEARER token in an HTTP authorization\nheader. A simple example of using the API from a python script to retrieve a json object containing API routes to all\nplatforms known to this host is shown here:\n\n```python\nimport requests\nbind_web_address = \'http://192.168.1.101:8080\'\ntokens = requests.post(url=f\'{bind_web_address}/authenticate\',\n                         json={"username": "my_user", "password": "my_password"})\naccess_token = tokens.json()[\'access_token\']\n\nplatforms = requests.get(url=f\'{bind_web_address}/vui/platforms\',\n                         headers={\'Authorization\': f\'Bearer {access_token}\'}\n                         )\nprint(platforms.json())\n```\n\n## Development\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://eclipse-volttron.readthedocs.io/en/latest/developing-volttron/developing-agents/agent-development.html)\n\n# Disclaimer Notice\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.\n',
    'author': 'VOLTTRON Team',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://volttron.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
