# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bacnet_proxy']

package_data = \
{'': ['*']}

install_requires = \
['bacpypes==0.16.7', 'volttron>=10.0.5rc0,<11.0.0']

entry_points = \
{'console_scripts': ['volttron-bacnet-proxy = bacnet_proxy.agent:main']}

setup_kwargs = {
    'name': 'volttron-bacnet-proxy',
    'version': '0.2.0rc1',
    'description': 'BACnet Proxy is an agent that supports communication and management of BACnet devices.',
    'long_description': '# BACnet Proxy Agent\n\n![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)\n![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)\n[![Passing?](https://github.com/eclipse-volttron/volttron-bacnet-proxy/actions/workflows/run-tests.yml/badge.svg)](https://github.com/eclipse-volttron/volttron-bacnet-proxy/actions/workflows/run-tests.yml)\n[![pypi version](https://img.shields.io/pypi/v/volttron-bacnet-proxy.svg)](https://pypi.org/project/volttron-bacnet-proxy/)\n\nBACnet Proxy is an agent that supports communication and management of BACnet devices.\n\nCommunication with a BACnet device on a network happens via a single virtual BACnet device. In the VOLTTRON driver framework,\nwe use a separate agent specifically for communicating with BACnet devices and managing the virtual BACnet device.\n\n# Requires\n\n* python >= 3.10\n* volttron >= 10.0\n* bacpypes == 0.16.7\n\n# Documentation\nMore detailed documentation can be found on [ReadTheDocs](https://volttron.readthedocs.io/en/modular/). The RST source\nof the documentation for this component is located in the "docs" directory of this repository.\n\n# Installation\n\nBefore installing, VOLTTRON should be installed and running.  Its virtual environment should be active.\nInformation on how to install of the VOLTTRON platform can be found\n[here](https://github.com/eclipse-volttron/volttron-core).\n\nInstall and start the BACnet proxy agent.\n\n```shell\nvctl install volttron-bacnet-proxy --agent-config <path to bacnet proxy config file> \\\n--vip-identity platform.bacnet_proxy \\\n--start\n```\n\nView the status of the installed agent\n\n```shell\nvctl status\n```\n\n# Development\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)\n\n\n# Disclaimer Notice\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.\n',
    'author': 'Mark Bonicillo',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eclipse-volttron/volttron-bacnet-proxy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
