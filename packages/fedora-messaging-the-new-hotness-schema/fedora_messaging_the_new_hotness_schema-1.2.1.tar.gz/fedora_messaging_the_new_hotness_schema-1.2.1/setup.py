# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hotness_schema', 'hotness_schema.tests']

package_data = \
{'': ['*'], 'hotness_schema.tests': ['fixtures/*']}

install_requires = \
['fedora-messaging>=3.1.0,<4.0.0']

entry_points = \
{'fedora.messages': ['hotness.update.bug.file = hotness_schema:UpdateBugFile',
                     'hotness.update.drop = hotness_schema:UpdateDrop']}

setup_kwargs = {
    'name': 'fedora-messaging-the-new-hotness-schema',
    'version': '1.2.1',
    'description': 'JSON schema definitions for messages published by the-new-hotness',
    'long_description': '.. image:: https://img.shields.io/pypi/v/fedora_messaging_the_new_hotness_schema.svg\n  :target: https://pypi.org/project/fedora_messaging_the_new_hotness_schema/\n\n.. image:: https://readthedocs.org/projects/the-new-hotness-messaging-schema/badge/?version=latest\n  :alt: Documentation Status\n  :target: https://the-new-hotness-messaging-schema.readthedocs.io/en/latest/?badge=latest\n\nthe-new-hotness Message Schema\n==============================\n\nJSON schema definitions for messages published by\n`the-new-hotness <https://github.com/fedora-infra/the-new-hotness>`_.\n\nDocumentation for the-new-hotness Message Schema could be found\n`here <https://the-new-hotness-messaging-schema.readthedocs.io/en/latest>`_.\n\nSee http://json-schema.org/ for documentation on the schema format. See\nhttps://fedora-messaging.readthedocs.io/en/latest/messages.html for\ndocumentation on fedora-messaging.\n',
    'author': 'Fedora Infrastructure Team',
    'author_email': 'infrastructure@lists.fedoraproject.org',
    'maintainer': 'Fedora Infrastructure Team',
    'maintainer_email': 'infrastructure@lists.fedoraproject.org',
    'url': 'https://github.com/fedora-infra/the-new-hotness-messages',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
