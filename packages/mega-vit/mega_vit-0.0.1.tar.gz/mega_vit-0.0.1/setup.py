# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mega_vit']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch']

setup_kwargs = {
    'name': 'mega-vit',
    'version': '0.0.1',
    'description': 'mega-vit - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# MegaVit\nA simple implementation of a CLIP that splits up an image into quandrants and then gets the embeddings for each quandrant\n\n\n[Paper Link](https://arxiv.org/pdf/2302.05442.pdf)\n\n# Appreciation\n* Lucidrains\n* Agorians\n\n\n\n# Install\n\n# Usage\n\n# Architecture\n\n# Todo\n\n\n# License\nMIT\n\n# Citations\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/mega-vit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
