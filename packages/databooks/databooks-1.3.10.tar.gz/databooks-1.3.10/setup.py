# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databooks', 'databooks.data_models']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.24,<4.0.0',
 'pydantic>=2.3,<3.0',
 'rich>=12.6.0,<13.0.0',
 'tomli>=2.0.1,<3.0.0',
 'typer>=0.4.0,<1.0.0',
 'typing-extensions>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['databooks = databooks.cli:app']}

setup_kwargs = {
    'name': 'databooks',
    'version': '1.3.10',
    'description': 'A CLI tool to resolve git conflicts and remove metadata in notebooks.',
    'long_description': '<p align="center">\n  <a href="https://datarootsio.github.io/databooks/"><img alt="logo" src="https://raw.githubusercontent.com/datarootsio/databooks/main/docs/images/logo.png"></a>\n</p>\n<p align="center">\n  <a href="https://dataroots.io"><img alt="Maintained by dataroots" src="https://dataroots.io/maintained-rnd.svg" /></a>\n  <a href="https://pypi.org/project/databooks/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/databooks" /></a>\n  <a href="https://pypi.org/project/databooks/"><img alt="PiPy" src="https://img.shields.io/pypi/v/databooks" /></a>\n  <a href="https://pepy.tech/project/databooks"><img alt="Downloads" src="https://pepy.tech/badge/databooks" /></a>\n  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>\n  <a href="http://mypy-lang.org/"><img alt="Mypy checked" src="https://img.shields.io/badge/mypy-checked-1f5082.svg" /></a>\n  <a href="https://pepy.tech/project/databooks"><img alt="Codecov" src="https://codecov.io/github/datarootsio/databooks/main/graph/badge.svg" /></a>\n  <a href="https://github.com/datarootsio/databooks/actions"><img alt="test" src="https://github.com/datarootsio/databooks/actions/workflows/test.yml/badge.svg" /></a>\n</p>\n\n\n`databooks` is a package to ease the collaboration between data scientists using\n[Jupyter notebooks](https://jupyter.org/), by reducing the number of git conflicts between\ndifferent notebooks and resolution of git conflicts when encountered.\n\nThe key features include:\n\n- CLI tool\n  - Clear notebook metadata\n  - Resolve git conflicts\n- Simple to use\n- Simple API for using modelling and comparing notebooks using [Pydantic](https://pydantic-docs.helpmanual.io/)\n\n## Requirements\n\n`databooks` is built on top of:\n\n- Python 3.7+\n- [Typer](https://typer.tiangolo.com/)\n- [Rich](https://rich.readthedocs.io/en/latest/)\n- [Pydantic](https://pydantic-docs.helpmanual.io/)\n- [GitPython](https://gitpython.readthedocs.io/en/stable/tutorial.html)\n- [Tomli](https://github.com/hukkin/tomli)\n\n## Installation\n\n```\npip install databooks\n```\n\n## Usage\n\n### Clear metadata\n\nSimply specify the paths for notebook files to remove metadata. By doing so, we can\nalready avoid many of the conflicts.\n\n```console\n$ databooks meta [OPTIONS] PATHS...\n```\n\n![databooks meta demo](https://raw.githubusercontent.com/datarootsio/databooks/main/docs/images/databooks-meta.gif)\n\n### Fix git conflicts for notebooks\n\nSpecify the paths for notebook files with conflicts to be fixed. Then, `databooks` finds\nthe source notebooks that caused the conflicts and compares them (so no JSON manipulation!)\n\n```console\n$ databooks fix [OPTIONS] PATHS...\n```\n\n![databooks fix demo](https://raw.githubusercontent.com/datarootsio/databooks/main/docs/images/databooks-fix.gif)\n\n### Assert notebook metadata\n\nSpecify paths of notebooks to be checked, an expression or recipe of what you\'d like to\nenforce. `databooks` will run your checks and raise errors if any notebook does not\ncomply with the desired metadata values. This advanced feature allows users to enforce\ncell tags, sequential cell execution, maximum number of cells, among many other things!\n\nCheck out our [docs](https://databooks.dev/latest/usage/overview/#databooks-assert) for more!\n\n```console\n$ databooks assert [OPTIONS] PATHS...\n```\n\n![databooks assert demo](https://raw.githubusercontent.com/datarootsio/databooks/main/docs/images/databooks-assert.gif)\n\n### Show rich notebook\n\nInstead of launching Jupyter and opening the browser to inspect notebooks, have a quick\nlook at them in the terminal. All you need is to specify the path(s) of the notebook(s).\n\n```console\n$ databooks show [OPTIONS] PATHS...\n```\n\n![databooks show demo](https://raw.githubusercontent.com/datarootsio/databooks/main/docs/images/databooks-show.gif)\n\n### Show rich notebook diffs\n\nSimilar to git diff, but for notebooks! Show a rich diff of the notebooks in the\nterminal. Works for comparing git index with the current working directory, comparing\nbranches or blobs.\n\n```console\n$ databooks diff [OPTIONS] [REF_BASE] [REF_REMOTE] [PATHS]...\n```\n\n![databooks diff demo](https://raw.githubusercontent.com/datarootsio/databooks/main/docs/images/databooks-diff.gif)\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Murilo Cunha',
    'author_email': 'murilo@dataroots.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://datarootsio.github.io/databooks/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
