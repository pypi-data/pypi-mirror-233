# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swarms_torch']

package_data = \
{'': ['*']}

install_requires = \
['torch']

setup_kwargs = {
    'name': 'swarms-torch',
    'version': '0.0.3',
    'description': 'swarms-torch - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Swarms in Torch\nSwarming algorithms like PSO, Ant Colony, Sakana, and more in PyTorch primitives😊\n\n\n## Installation\n\nYou can install the package using pip\n\n```bash\npip3 install swarms-torch\n```\n\n# Usage\n- We have just PSO now, but we\'re adding in ant colony and others!\n\n```python\nfrom swarms_torch import ParticleSwarmOptimization\n\n#test\npso = ParticleSwarmOptimization(goal="Attention is all you need", n_particles=100)\npso.optimize(iterations=1000)\n```\n\n- Ant Colony Optimization\n```python\nfrom swarms_torch.ant_colony_swarm import AntColonyOptimization\n\n# Usage:\ngoal_string = "Hello ACO"\naco = AntColonyOptimization(goal_string, num_iterations=1000)\nbest_solution = aco.optimize()\nprint("Best Matched String:", best_solution)\n\n```\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/swarms-pytorch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
