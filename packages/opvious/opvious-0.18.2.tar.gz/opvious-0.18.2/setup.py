# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opvious',
 'opvious.client',
 'opvious.data',
 'opvious.executors',
 'opvious.modeling',
 'opvious.specifications']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=2.2,<3.0',
 'humanize>=4.4.0,<5.0.0',
 'importnb>=2023.1.7,<2024.0.0',
 'numpy>=1.21',
 'pandas>=1.4,<2.0']

extras_require = \
{'aio': ['aiohttp>=3.8,<4.0', 'Brotli>=1.0.9,<2.0.0'],
 'cli': ['docopt>=0.6.2,<0.7.0']}

setup_kwargs = {
    'name': 'opvious',
    'version': '0.18.2',
    'description': 'Opvious Python SDK',
    'long_description': '# Opvious Python SDK  [![CI](https://github.com/opvious/sdk.py/actions/workflows/ci.yml/badge.svg)](https://github.com/opvious/sdk.py/actions/workflows/ci.yml) [![Pypi badge](https://badge.fury.io/py/opvious.svg)](https://pypi.python.org/pypi/opvious/)\n\nAn SDK for solving linear, mixed-integer, and quadratic optimization models via\nthe [Opvious](https://www.opvious.io) API.\n\n## Highlights\n\n### Declarative modeling API\n\n+ Extensive static validations\n+ Exportable to LaTeX\n+ Extensible support for high-level patterns (activation variables, masks, ...)\n\n```python\nimport opvious.modeling as om\n\nclass BinPacking(om.Model):\n  items = om.Dimension()  # All items to bin\n  weight = om.Parameter.non_negative(items)  # Weight per item\n  bins = om.interval(1, om.size(items), name="B")  # Available bins\n  max_weight = om.Parameter.non_negative()  # Maximum weight for each bin\n  assigned = om.Variable.indicator(bins, items)  # Bin to item assignment\n  used = om.fragments.ActivationVariable(assigned, projection=1)  # 1 if a bin is used\n\n  @om.constraint\n  def each_item_is_assigned_once(self):\n    for i in self.items:\n      yield om.total(self.assigned(b, i) for b in self.bins) == 1\n\n  @om.constraint\n  def bin_weights_are_below_max(self):\n    for b in self.bins:\n      bin_weight = om.total(self.weight(i) * self.assigned(b, i) for i in self.items)\n      yield bin_weight <= self.max_weight()\n\n  @om.objective\n  def minimize_bins_used(self):\n    return om.total(self.used(b) for b in self.bins)\n```\n\nAuto-generated specification:\n\n<p align="center">\n  <img alt="Bin package LaTeX specification" src="resources/images/bin-packing-specification.png" width="600px">\n</p>\n\n\n### Transparent remote solves\n\n+ No local solver installation required\n+ Real-time progress notifications\n+ Seamless data import/export via native support for `pandas`\n+ Flexible multi-objective support: weighted sums, epsilon constraints, ...\n+ Built-in debugging capabilities: relaxations, fully annotated LP formatting,\n  ...\n\n```python\nimport opvious\n\nclient = opvious.Client.default()\n\nsolution = await client.solve(\n  opvious.Problem(\n    specification=BinPacking().specification(),\n    parameters={\n      "weight": {"a": 10.5, "b": 22, "c": 48},\n      "binMaxWeight": 50,\n    },\n  ),\n)\nassignments = solution.outputs.variable("assigned") # Optimal values\n```\n\nTake a look at https://opvious.readthedocs.io for the full documentation or\n[these notebooks][notebooks] to see the SDK in action.\n\n[notebooks]: https://github.com/opvious/examples/tree/main/notebooks\n',
    'author': 'Opvious Engineering',
    'author_email': 'oss@opvious.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/opvious/sdk.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
