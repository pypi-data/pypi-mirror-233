# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepsurveysim',
 'deepsurveysim.IO',
 'deepsurveysim.Survey',
 'deepsurveysim.Visuals']

package_data = \
{'': ['*'],
 'deepsurveysim': ['.pytest_cache/*', '.pytest_cache/v/cache/*', 'settings/*'],
 'deepsurveysim.IO': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'astroplan>=0.8,<0.9',
 'configparser>=5.3.0,<6.0.0',
 'numexpr>=2.8.4,<3.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'deepsurveysim',
    'version': '0.1.0',
    'description': 'An astrological survey simulation designed for testing MDP-style algorithms',
    'long_description': '\n[![status](https://img.shields.io/badge/License-BSD3-lightgrey)](https://github.com/deepskies/TelescopePositioningSimulation/blob/61abe7a67de72e5a22755c427189fa402f57dc9f/LICENSE)\n[![test-telescope](https://github.com/deepskies/TelescopePositioningSimulation/actions/workflows/test-telescope.yaml/badge.svg?branch=main)]()\n [![PyPI version](https://badge.fury.io/py/deepsurveysim.svg)](https://badge.fury.io/py/deepsurveysim)\n[![Documentation Status](https://readthedocs.org/projects/deepsurveysim/badge/?version=latest)](https://deepsurveysim.readthedocs.io/en/latest/?badge=latest)\n\n# Summary\n\nModern astronomical surveys have multiple competing scientific goals.\nOptimizing the observation schedule for these goals presents significant computational and theoretical challenges, and state-of-the-art methods rely on expensive human inspection of simulated telescope schedules.\nAutomated methods, such as reinforcement learning, have recently been explored to accelerate scheduling.\n**DeepSurveySim** provides methods for tracking and approximating sky conditions for a  set of observations from a user-supplied telescope configuration.\n\n# Documentation\n\n### [ReadTheDocs](https://deepsurveysim.readthedocs.io/en/latest/)\n\n### Build locally\n\nFirst install the package from source, then run\n\n```\npip install sphinx\ncd docs\nmake html\n```\n\nThe folder `docs/_build/html` will be populated with the documentation.\nNavigate to `file:///<path to local install>/docs/_build/html/index.html` in any web browser to view.\n\n\n\n# Installation\n### Install from pip\n\nSimply run\n\n```\npip install DeepSurveySim\n```\n\nThis will install the project with all its mandatory requirements.\n\nIf you wish to include the optional `skybright`, use the command:\n\n```\npip install DeepSurveySim[skybright]\n```\n\nNot installing this will result in loss of the variables `sky_magintude`, `tau`, and `teff`, but will work on most (if not all) machines.\n\n### Install from source\n\nThe project is built with [poetry](https://python-poetry.org/), and this is the recommended install method.\nAll dependencies are resolved in the `poetry.lock` file, so you can install immediately from the command\n\n```\ngit clone https://github.com/deepskies/DeepSurveySim.git\npoetry shell\npoetry install --all-extras\n```\n\nAssuming you have poetry installed on your base environment.\nThis will use lock file to install all the correct versions.\nTo use the installed environment, use the command `poetry shell` to enter it.\nThe command `exit` will take you out of this environment as it would for any other type of virtual environment.\n\nOtherwise, you can use the `pyproject.toml` with your installer of choice.\n\nTo verify all the depedencies are properly installed - run `python run pytest`.\n\n# Example:\n\n## To run as a live envoriment for RL\n\n```\nfrom DeepSurveySim.Survey.survey import Survey\nfrom DeepSurveySim.IO.read_config import ReadConfig\n\nseo_config = ReadConfig(\n        observator_configuration="DeepSurveySim/settings/SEO.yaml"\n    )()\n\nsurvey_config = ReadConfig(\n        observator_configuration="DeepSurveySim/settings/equatorial_survey.yaml",\n        survey=True\n    )()\n\nenv = Survey(seo_config, survey_config)\nobservation = env._observation_calculation()\n\nstop = True\nwhile not stop:\n    action = model.predict_action(observation)\n    observation, reward, stop, log = env.step()\n```\n\n## To generate observations\n\n```\nfrom DeepSurveySim.Survey.survey import Survey\nfrom DeepSurveySim.IO.read_config import ReadConfig\n\nseo_config = ReadConfig(\n        observator_configuration="DeepSurveySim/settings/SEO.yaml"\n    )()\n\nsurvey_config = ReadConfig(\n        observator_configuration="DeepSurveySim/settings/equatorial_survey.yaml",\n        survey=True\n    )()\n\nenv = Survey(seo_config, survey_config)\nobservations = env()\n```\n\n\n# Acknowledgement\nThis work was produced by Fermi Research Alliance, LLC under Contract No. DE-AC02-07CH11359 with the U.S. Department of Energy, Office of Science, Office of High Energy Physics. Publisher acknowledges the U.S. Government license to provide public access under the DOE Public Access Plan DOE Public Access Plan.\n\nWe acknowledge the Deep Skies Lab as a community of multi-domain experts and collaborators who’ve facilitated an environment of open discussion, idea-generation, and collaboration. This community was important for the development of this project.\n\nWe thank Franco Terranova  and Shohini Rhae for their assistance in testing the preliminary version of the package, and Eric Neilsen  Jr. for his domain expertise.\n\n# Citation\n\nIf this package is useful for your work, we request you cite us:\n```\n\n```\n\nIf the `skybright` option is used, we also encourage its citation:\n```\n@misc{skybright_Neilsen:2019,\n    author = "Neilsen, Eric",\n    title = "{skybright}",\n    reportNumber = "FERMILAB-CODE-2019-01",\n    doi = "10.11578/dc.20190212.1",\n    month = "2",\n    year = "2019"\n}\n```\n\n\n',
    'author': 'M. Voetberg',
    'author_email': 'maggiev@fnal.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/deepskies/DeepSurveySim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
