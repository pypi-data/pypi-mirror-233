# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sgdrf']

package_data = \
{'': ['*']}

install_requires = \
['pyro-ppl>=1.8.6,<2.0.0', 'torch>=2.0.1,<3.0.0', 'typer>=0.3,<0.10']

setup_kwargs = {
    'name': 'sgdrf',
    'version': '0.1.1',
    'description': 'Python implementation of Streaming Gaussian Dirichlet Random Fields (San Soucie et al. 2023)',
    'long_description': '# Sgdrf\n\n<!-- markdown-link-check-disable -->\n\n[![Version status](https://img.shields.io/pypi/status/sgdrf)](https://opensource.org/license/mit/)\n\n<!-- markdown-link-check-enable-->\n\n[![License](https://img.shields.io/github/license/san-soucie/sgdrf)]()\n[![Python version compatibility](https://img.shields.io/pypi/pyversions/sgdrf)](https://pypi.org/project/sgdrf)\n[![Version on GitHub](https://img.shields.io/github/v/release/san-soucie/sgdrf?include_prereleases&label=GitHub)](https://github.com/san-soucie/sgdrf/releases)\n[![Version on PyPi](https://img.shields.io/pypi/v/sgdrf)](https://pypi.org/project/sgdrf)\n[![Documentation status](https://readthedocs.org/projects/sgdrf/badge)](https://sgdrf.readthedocs.io/en/latest)\n[![Build (GitHub Actions)](https://img.shields.io/github/actions/workflow/status/san-soucie/sgdrf/push-main.yml?branch=main)](https://github.com/san-soucie/sgdrf/actions)\n[![Test coverage (codecov)](https://codecov.io/github/san-soucie/sgdrf/coverage.svg)](https://codecov.io/gh/san-soucie/sgdrf)\n[![Maintainability (Code Climate)](https://api.codeclimate.com/v1/badges/6b240648883c3a56c309/maintainability)](https://codeclimate.com/github/san-soucie/sgdrf/maintainability)\n[![Created with Tyrannosaurus](https://img.shields.io/badge/Created_with-Tyrannosaurus-0000ff.svg)](https://github.com/dmyersturnbull/tyrannosaurus)\n\nPython implementation of Streaming Gaussian Dirichlet Random Fields (San Soucie et al. 2023).\n\n[See the docs 📚](https://sgdrf.readthedocs.io/) for more info.\n\nLicensed under the terms of the [MIT License](https://spdx.org/licenses/MIT.html).\n[New issues](https://github.com/san-soucie/sgdrf/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/san-soucie/sgdrf/blob/main/CONTRIBUTING.md)\nand [security policy](https://github.com/san-soucie/sgdrf/blob/main/SECURITY.md).\nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).\n',
    'author': 'John San Soucie',
    'author_email': 'None',
    'maintainer': 'John San Soucie',
    'maintainer_email': 'None',
    'url': 'https://github.com/san-soucie/sgdrf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4',
}


setup(**setup_kwargs)
