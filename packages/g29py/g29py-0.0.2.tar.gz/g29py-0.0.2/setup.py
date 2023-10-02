# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['g29py']

package_data = \
{'': ['*']}

install_requires = \
['hid==1.0.4']

setup_kwargs = {
    'name': 'g29py',
    'version': '0.0.2',
    'description': 'python driver for g29 wheel/pedals',
    'long_description': '# g29py\n> python driver for logitech g29 wheel/pedals\n\n![](etc/g29py.jpg)\n\n#### install\n```bash\npip install g29py\n```\n\n```python\nfrom g29py import G29\ng29 = G29()\ng29.reset() # wheel cal\n```\n\n```python\n# write \ng29.set_range(500)\ng29.set_friction(0.5)\n```\n\n```python\n#read\ng29.start_pumping() # thread\nwhile 1:\n    state = g29.get_state()\n    print("steering:", state["steering"])\n    print("brake:", state["brake"])\n```\n\n#### sources\n\n- Commands based on nightmode\'s [logitech-g29](https://github.com/nightmode/logitech-g29) node.js driver.\n- Interface uses libhidapi ctype bindings from apmorton\'s [pyhidapi](https://github.com/apmorton/pyhidapi).\n\n\n### support\n\nOnly Logitech G29 Driving Force Racing Wheels & Pedals kit supported on linux in ps3 mode.\n\nOn linux, remove sudo requirements by adding udev rule.\n\n```bash\necho \'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"\' \\\n    | sudo tee /etc/udev/rules.d/99-hidraw-permissions.rules\nsudo udevadm control --reload-rules\n```\n',
    'author': 'sean pollock',
    'author_email': 'seanap@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
