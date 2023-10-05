# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['okareo']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.25.0,<0.26.0', 'pytest-httpx>=0.26.0,<0.27.0']

setup_kwargs = {
    'name': 'okareo',
    'version': '0.0.1',
    'description': 'Python SDK for intercating with Okareo Cloud APIs',
    'long_description': "# Okareo Python SDK\n\n[![PyPI](https://img.shields.io/pypi/v/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)\n[![PyPI - License](https://img.shields.io/pypi/l/okareo?style=flat-square)](https://pypi.python.org/pypi/okareo/)\n\n---\n\n**Documentation**: [https://okareo-ai.github.io/okareo](https://okareo-ai.github.io/okareo)\n\n**Source Code**: [https://github.com/okareo-ai/okareo](https://github.com/okareo-ai/okareo)\n\n**PyPI**: [https://pypi.org/project/okareo/](https://pypi.org/project/okareo/)\n\n---\n\nPython SDK for intercating with Okareo Cloud APIs\n\n## Installation\n\n```sh\npip install okareo\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.8+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Testing\n\n```sh\npytest\n```\n\n### Documentation\n\nThe documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings\n of the public signatures of the source code. The documentation is updated and published as a [Github project page\n ](https://pages.github.com/) automatically as part each release.\n\n### Releasing\n\nTrigger the [Draft release workflow](https://github.com/okareo-ai/okareo/actions/workflows/draft_release.yml)\n(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.\n\nFind the draft release from the\n[GitHub releases](https://github.com/okareo-ai/okareo/releases) and publish it. When\n a release is published, it'll trigger [release](https://github.com/okareo-ai/okareo/blob/master/.github/workflows/release.yml) workflow which creates PyPI\n release and deploys updated documentation.\n\n### Pre-commit\n\nPre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality\n checks to make sure the changeset is in good shape before a commit/push happens.\n\nYou can install the hooks with (runs for each commit):\n\n```sh\npre-commit install\n```\n\nOr if you want them to run only for each push:\n\n```sh\npre-commit install -t pre-push\n```\n\nOr if you want e.g. want to run all checks manually for all files:\n\n```sh\npre-commit run --all-files\n```\n\n---\n\nAll rights reserved for Okareo Inc\n",
    'author': 'berni',
    'author_email': 'info@okareo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://okareo-ai.github.io/okareo',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
