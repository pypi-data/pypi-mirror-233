# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['chameleontools',
 'chameleontools.ChromatoSeq',
 'chameleontools.CodonAnalyzer',
 'chameleontools.CodonShuffle',
 'chameleontools.FastAreader',
 'chameleontools.ORFfinder',
 'chameleontools.SeqParser',
 'chameleontools.Stealth',
 'chameleontools.StealthParser']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.81,<2.0', 'scipy>=1.10.1,<2.0.0', 'tqdm>=4.66.1,<5.0.0']

entry_points = \
{'console_scripts': ['pstealth = chameleontools.pstealth:main']}

setup_kwargs = {
    'name': 'chameleontools',
    'version': '0.1.2',
    'description': 'A Stealth-based pipeline that optimizes plasmids for bacterial transformations in non-model organisms.',
    'long_description': "# Team UCSC 2023 Software Tool\n\nIf you team competes in the [**Software & AI** village](https://competition.igem.org/participation/villages) or wants to\napply for the [**Best Software Tool** prize](https://competition.igem.org/judging/awards), you **MUST** host all the\ncode of your team's software tool in this repository, `main` branch. By the **Wiki Freeze**, a\n[release](https://docs.gitlab.com/ee/user/project/releases/) will be automatically created as the judging artifact of\nthis software tool. You will be able to keep working on your software after the Grand Jamboree.\n\n> If your team does not have any software tool, you can totally ignore this repository. If left unchanged, this\nrepository will be automatically deleted by the end of the season.\n\n\n\n## Description\nLet people know what your project can do specifically. Provide context and add a link to any reference visitors might\nbe unfamiliar with (for example your team wiki). A list of Features or a Background subsection can also be added here.\nIf there are alternatives to your project, this is a good place to list differentiating factors.\n\n## Installation\nWithin a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew.\nHowever, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing\nspecific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a\nspecific context like a particular programming language version or operating system or has dependencies that have to be\ninstalled manually, also add a Requirements subsection.\n\n## Usage\nUse examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of\nusage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably\ninclude in the README.\n\n## Contributing\nState if you are open to contributions and what your requirements are for accepting them.\n\nFor people who want to make changes to your project, it's helpful to have some documentation on how to get started.\nPerhaps there is a script that they should run or some environment variables that they need to set. Make these steps\nexplicit. These instructions could also be useful to your future self.\n\nYou can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce\nthe likelihood that the changes inadvertently break something. Having instructions for running tests is especially\nhelpful if it requires external setup, such as starting a Selenium server for testing in a browser.\n\n## Authors and acknowledgment\nShow your appreciation to those who have contributed to the project.\n",
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.igem.org/2023/software-tools/ucsc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.13',
}


setup(**setup_kwargs)
