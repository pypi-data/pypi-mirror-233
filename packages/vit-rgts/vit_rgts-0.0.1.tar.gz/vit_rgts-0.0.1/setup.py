# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vit_rgts']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'pytorch']

setup_kwargs = {
    'name': 'vit-rgts',
    'version': '0.0.1',
    'description': 'vit-registers - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# VISION TRANSFORMERS NEED REGISTERS\nThe vit model from the paper "VISION TRANSFORMERS NEED REGISTERS"\n\n[Paper Link](https://arxiv.org/pdf/2309.16588.pdf)\n\n# Appreciation\n* Lucidrains\n* Agorians\n\n# Install\n`pip install vit-registers`\n\n# Usage\n\n# Architecture\n\n# Todo\n\n\n# License\nMIT\n\n# Citations\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Vit-RGTS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
