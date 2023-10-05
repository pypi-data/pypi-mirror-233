# -*- coding: utf-8 -*-
from setuptools import setup

with open("README.md", "r", encoding="utf-8-sig") as fh:
    long_description = fh.read()

packages = \
['sescore2',
 'sescore2.inference',
 'sescore2.preprocess',
 'sescore2.syn_data',
 'sescore2.train'
 ]

package_data = \
{'': ['*']}

install_requires = \
['transformers',
'accelerate==0.20.3',
'sentencepiece',
'protobuf==3.20.*',
'python-snappy',
'pandas',
'nvitop',
'click',
'datasets',
'wandb',
'scipy',
'absl-py',
'torch',
'torchvision',
'torchaudio']

setup_kwargs = {
    'name': 'sescore2',
    'version': '1.0.4',
    'description': 'SESCORE2: Learning Text Generation Evaluation via Synthesizing Realistic Mistakes',
    'long_description': long_description,
    'long_description_content_type': "text/markdown",
    'author': 'Wenda Xu, Xian Qian, Mingxuan Wang, Lei Li, William Yang Wang',
    'author_email': 'wendaxu@ucsb.edu',
    'maintainer': 'Wenda Xu, Zihan Ma',
    'maintainer_email': 'zihan_ma@ucsb.edu',
    'url': 'https://github.com/xu1998hz/SEScore2_archive',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
