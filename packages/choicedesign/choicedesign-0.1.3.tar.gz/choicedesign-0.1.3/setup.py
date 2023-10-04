# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['choicedesign']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.4,<2.0.0', 'pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'choicedesign',
    'version': '0.1.3',
    'description': 'Experimental designs for discrete choice models.',
    'long_description': '# ChoiceDesign\n\n**ChoiceDesign** is a Python package tool to construct D-efficient designs for Discrete Choice Experiments. ChoiceDesign combines enough flexibility to construct from simple 2-alternative designs with few attributes, to more complex settings that may involve conditions between attributes. ChoiceDesign is a revamped version of [EDT](https://github.com/ighdez/EDT), a project I created some years ago for the same purpose. ChoiceDesign includes improvements over EDT such as class-based syntax, coding improvements, better documentation and making this package available to install via `pip`.\n\n## Installation\n\nChoiceDesign is available to install via the regular syntax of `pip`:\n\n* ``python3 -m pip install choicedesign``\n\n## Features\n\nThe main features of ChoiceDesign are:\n\n* Allows to customize each attribute in terms of:\n  * Attribute Levels\n  * Continuous or Dummy coding (Effects coding is work-in-progress)\n  * Assignement of prior parameters\n  * Attribute names\n\n* Designs with constraints: ChoiceDesign allows to define conditions over different attribute levels.\n* Designs with blocks.\n* Designs with alternative-specific constants (ASC).\n* Multiple stopping criteria (Fixed number of iterations, iterations without improvement or fixed time).\n\n## Examples\n\nI provide some Jupyter notebooks that illustrate the use of ChoiceDesign in the `examples/` folder of this Git.\n\n## How to contribute?\nAny contributions to ChoiceDesign are welcome via this Git, or to the email joseignaciohernandezh at gmail dot com. \n\n## Disclaimer\n\nThis software is provided for free and as it is, say with **no warranty**, and neither me nor my current institution is liable of any consequence of the use of it. In any case, integrity checks have been performed by comparing results with alternative software.\n\n## References\n* Kuhfeld, W. F. (2005). Experimental design, efficiency, coding, and choice designs. *Marketing research methods in SAS: Experimental design, choice, conjoint, and graphical techniques*, 47-97.\n* Quan, W., Rose, J. M., Collins, A. T., & Bliemer, M. C. (2011). A comparison of algorithms for generating efficient choice experiments.',
    'author': 'José Ignacio Hernández',
    'author_email': 'joseignaciohernandezh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
