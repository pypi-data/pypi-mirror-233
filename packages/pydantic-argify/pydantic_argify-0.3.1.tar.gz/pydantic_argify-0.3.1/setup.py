# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_argify']

package_data = \
{'': ['*']}

install_requires = \
['pydantic-settings>=2.0.2,<3.0.0', 'pydantic>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'pydantic-argify',
    'version': '0.3.1',
    'description': 'Build ArgumentParser from pydantic model.',
    'long_description': '# pydantic-argify\n[![Python](https://img.shields.io/pypi/pyversions/pydantic-argify.svg)](https://pypi.org/project/pydantic-argify/)\n[![PyPI version](https://badge.fury.io/py/pydantic-argify.svg)](https://badge.fury.io/py/pydantic-argify)\n[![codecov](https://codecov.io/gh/elda27/pydantic_argify/branch/main/graph/badge.svg?token=GLqGNtE7Df)](https://codecov.io/gh/elda27/pydantic_argify)\n[![Downloads](https://static.pepy.tech/badge/pydantic-argify)](https://pepy.tech/project/pydantic-argify)\n[![License](https://img.shields.io/pypi/l/pydantic-argify.svg)](https://github.com/google/pydantic_argify/blob/main/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nBuild ArgumentParser from pydantic model.\n\n## What\'s difference with other projects.\nThis project is dedicated to crafting an argument parser based on the Pydantic model.\nUnlike many other projects where the ArgumentParser functionality is concealed within the library, \nthis tool aims to simplify its use, even in complex scenarios. \nFor instance, handling nested sub-parsers like `aws s3 cp <some options>` \nor supporting nested Pydantic models has been a challenge in existing solutions. \nThis library overcomes these limitations, allowing you to effortlessly incorporate intricate functionalities.\n\n```python\n```\n\n## Example 1\n\n```python\nfrom argparse import ArgumentParser\nfrom pydantic import BaseModel, Field\nfrom pydantic_argify import build_parser\n\nclass Config(BaseModel):\n    string: str = Field(description="string parameter")\n    integer: int = Field(description="integer parameter")\n\nparser = ArgumentParser()\nbuild_parser(parser)\nparser.print_help()\n```\n\n```\nusage: basic.py [-h] --string STRING --integer INTEGER\n\noptional arguments:\n  -h, --help            show this help message and exit\n\nConfig:\n  --string STRING, -s STRING\n                        a required string\n  --integer INTEGER, -i INTEGER\n                        a required integer\n```\n\n## Example 2\n\n```python\nfrom argparse import ArgumentParser\nfrom pydantic import BaseModel, Field\nfrom pydantic_argify import build_parser\n\nclass SubConfigA(BaseModel):\n    string: str = Field(description="string parameter")\n    integer: int = Field(description="integer parameter")\n\nclass SubConfigB(BaseModel):\n    double: float = Field(description="a required string")\n    integer: int = Field(0, description="a required integer")\n\n\nparser = ArgumentParser()\nsubparsers = parser.add_subparsers()\nbuild_parser(subparsers.add_parser("alpha"), SubConfigA)\nbuild_parser(subparsers.add_parser("beta"), SubConfigB)\nparser.print_help()\n```\n\n```\nusage: sub_parser.py [-h] {alpha,beta} ...\n\npositional arguments:\n  {alpha,beta}\n\noptional arguments:\n  -h, --help    show this help message and exit\n```\n\n## Additional config\nBehaviour of pydantic can be controlled via the `Config` class or extra arguments of `Field`.\n`Config` is affected all fields.\nExtra arguments of `Field` is affected specific field. \n\n\n<dl>\n  <dt><code>cli_disable_prefix</code></dt>\n  <dd>Prefix of argument of boolean type for `store_false`. Default to <code>--disable-</code></dd>\n\n  <dt><code>cli_enable_prefix</code></dt>\n  <dd>Prefix of argument of boolean type for `store_true`. Default to <code>--enable-</code></dd>\n</dl>\n\n\n## Future works\n\n- [ ]: Options completion for bash\n',
    'author': 'elda27',
    'author_email': 'kaz.birdstick@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
