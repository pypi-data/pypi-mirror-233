# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swarms_torch']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'swarms-torch',
    'version': '0.0.1',
    'description': 'swarms-torch - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Python Package Template\nA easy, reliable, fluid template for python packages complete with docs, testing suites, readme\'s, github workflows, linting and much much more\n\n\n## Installation\n\nYou can install the package using pip\n\n```bash\npip install -e .\n```\n## Structure\n```\n├── LICENSE\n├── Makefile\n├── README.md\n├── agorabanner.png\n├── example.py\n├── package\n│   ├── __init__.py\n│   ├── main.py\n│   └── subfolder\n│       ├── __init__.py\n│       └── main.py\n├── pyproject.toml\n└── requirements.txt\n\n2 directories, 11 files\n```\n# Usage\n\n# Documentation\n\n\n### Code Quality 🧹\n\nWe provide two handy commands inside the `Makefile`, namely:\n\n- `make style` to format the code\n- `make check_code_quality` to check code quality (PEP8 basically)\n\nSo far, **there is no types checking with mypy**. See [issue](https://github.com/roboflow-ai/template-python/issues/4). \n\n### Tests 🧪\n\n[`pytests`](https://docs.pytest.org/en/7.1.x/) is used to run our tests.\n\n### Publish on PyPi 🚀\n\n**Important**: Before publishing, edit `__version__` in [src/__init__](/src/__init__.py) to match the wanted new version.\n\nWe use [`twine`](https://twine.readthedocs.io/en/stable/) to make our life easier. You can publish by using\n\n```\nexport PYPI_USERNAME="you_username"\nexport PYPI_PASSWORD="your_password"\nexport PYPI_TEST_PASSWORD="your_password_for_test_pypi"\nmake publish -e PYPI_USERNAME=$PYPI_USERNAME -e PYPI_PASSWORD=$PYPI_PASSWORD -e PYPI_TEST_PASSWORD=$PYPI_TEST_PASSWORD\n```\n\nYou can also use token for auth, see [pypi doc](https://pypi.org/help/#apitoken). In that case,\n\n```\nexport PYPI_USERNAME="__token__"\nexport PYPI_PASSWORD="your_token"\nexport PYPI_TEST_PASSWORD="your_token_for_test_pypi"\nmake publish -e PYPI_USERNAME=$PYPI_USERNAME -e PYPI_PASSWORD=$PYPI_PASSWORD -e PYPI_TEST_PASSWORD=$PYPI_TEST_PASSWORD\n```\n\n**Note**: We will try to push to [test pypi](https://test.pypi.org/) before pushing to pypi, to assert everything will work\n\n### CI/CD 🤖\n\nWe use [GitHub actions](https://github.com/features/actions) to automatically run tests and check code quality when a new PR is done on `main`.\n\nOn any pull request, we will check the code quality and tests.\n\nWhen a new release is created, we will try to push the new code to PyPi. We use [`twine`](https://twine.readthedocs.io/en/stable/) to make our life easier. \n\nThe **correct steps** to create a new realease are the following:\n- edit `__version__` in [src/__init__](/src/__init__.py) to match the wanted new version.\n- create a new [`tag`](https://git-scm.com/docs/git-tag) with the release name, e.g. `git tag v0.0.1 && git push origin v0.0.1` or from the GitHub UI.\n- create a new release from GitHub UI\n\nThe CI will run when you create the new release.\n\n# Docs\nWe use MK docs. This repo comes with the zeta docs. All the docs configurations are already here along with the readthedocs configs\n\n# Q&A\n\n## Why no cookiecutter?\nThis is a template repo, it\'s meant to be used inside GitHub upon repo creation.\n\n## Why reinvent the wheel?\n\nThere are several very good templates on GitHub, I prefer to use code we wrote instead of blinding taking the most starred template and having features we don\'t need. From experience, it\'s better to keep it simple and general enough for our specific use cases.\n\n# Architecture\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/swarms-pytorch',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
