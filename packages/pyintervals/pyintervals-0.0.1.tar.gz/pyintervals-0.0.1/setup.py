# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyintervals']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1,<5']}

setup_kwargs = {
    'name': 'pyintervals',
    'version': '0.0.1',
    'description': 'Efficient interval operations.',
    'long_description': "📐 pyintervals\n===============================\n\n**Execute efficient interval operations in Python.**\n\n*(Currently in active development. Leave a* ⭐️ *on GitHub if you're interested how this develops!)*\n\nWhy?\n--------\n\nInspired by a discussion and initial implementation in a professional project\nand a library I've been using in one of my previous jobs, **pyintervals** is born.\n\nIntervals pop-up frequently in programming, specifically in domains where you\nhave an activity or a proxy for it. Suppose you are implementing a single machine scheduling algorithm.\nIn order to schedule an operation, you need to makes sure that the machine is available\nduring your desired time of operation. Or you are implementing a booking system and need to check\nthat the hotel has at least 1 room with desired number of beds for the dates selected.\nFor such cases, you need to control some information overlapping with an interval.\n\nAcknowledgements\n----------------\n\nFollowing resources and people have inspired **pyintervals**:\n\n- `Always use [closed, open) intervals <https://fhur.me/posts/always-use-closed-open-intervalshttps://fhur.me/posts/always-use-closed-open-intervals>`_\n- `Arie Bovenberg <https://github.com/ariebovenberg>`_\n- `pdfje (for initial setup of this project) <https://github.com/ariebovenberg/pdfje>`_\n- Sam de Wringer\n- Tim Lamballais-Tessensohn\n",
    'author': 'Serkan Kalay',
    'author_email': 'serkanosmankalay@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/serkankalay/pyintervals',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
