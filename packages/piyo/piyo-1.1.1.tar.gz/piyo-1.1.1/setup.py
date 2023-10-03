# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piyo']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'piyo',
    'version': '1.1.1',
    'description': '',
    'long_description': '# 🐣 piyo\nesa API v1 client library, written in Python\n\n## Installation\n\nInstall this library using pip from [PyPI](https://pypi.org/project/piyo/)\n\n``` shell\npip install piyo\n```\n\n## Usage By purpose\n\n### Preparation\n\n```python\nfrom piyo import Client\n\nclient = Client(access_token=\'<access_token>\', current_team=\'<team_name>\')\n``` \n\n### Search article\n\nSet search keywords and options.\n\nSee official documents for details: https://docs.esa.io/posts/102#%E8%A8%98%E4%BA%8B\n\n``` python\nkeywords = ["diary", "secret"]\nsearch_options = {\n    "sort": "created"\n}\nposts = client.posts(keywords=keywords, search_options=search_options)\n``` \n\n## Usage\n\n``` python\nfrom piyo import Client\n\nclient = Client(access_token=\'<access_token>\', current_team=\'<team_name>\')\n# Client will look up environment variables "ESA_ACCESS_TOKEN", so you can set access token \n# to ESA_ACCESS_TOKEN instead of pass it to Client.\n\nclient.user()\n#=> GET /v1/user\n\nclient.teams()\n#=> GET /v1/teams\n\nclient.team()\n#=> GET /v1/teams/<team_name>\n\nclient.stats()\n#=> GET /v1/teams/<team_name>/stats\n\nclient.members()\n#=> GET /v1/teams/<team_name>/members\n\nclient.delete_member()\n#=> DELETE /v1/teams/<team_name>/members/1\n\nclient.posts(keywords=["diary secret"], search_options={"sort": "created"})\n#=> GET /v1/teams/<team_name>/posts\n\nclient.post(1)\n#=> GET /v1/teams/<team_name>/posts/1\n\nclient.create_post({post: {name: "hi!"}})\n#=> POST /v1/teams/<team_name>/posts\n\nclient.update_post(1, {post: {name: "hi!"}})\n#=> PATCH /v1/teams/<team_name>/posts/1\n\nclient.delete_post(1)\n#=> DELETE /v1/teams/<team_name>/posts/1\n\nclient.comments()\n#=> GET /v1/teams/<team_name>/comments\n\nclient.comments(1)\n#=> GET /v1/teams/<team_name>/posts/1/comments\n\nclient.create_comment(1, {"comment":{"body_md":"LGTM!"}})\n#=> POST /v1/teams/<team_name>/posts/1/comments\n\nclient.update_comment(234, {"comment":{"body_md":"LGTM!"}})\n#=> PATCH /v1/teams/<team_name>/comments/234\n\nclient.delete_comment(234)\n#=> DELETE /v1/teams/<team_name>/comments/234\n\nclient.comment(234)\n#=> GET /v1/teams/<team_name>/comments/234\n\nclient.add_post_star(1)\n#=> POST /v1/teams/<team_name>/posts/1/star\n\nclient.delete_post_star(1)\n#=> DELETE /v1/teams/<team_name>/posts/1/star\n\nclient.stargazers(1)\n#=> GET /v1/teams/<team_name>/posts/1/stargazers\n\nclient.add_comment_star(234)\n#=> POST /v1/teams/<team_name>/comment/234/star\n\nclient.delete_comment_star(234)\n#=> DELETE /v1/teams/<team_name>/comment/234/star\n\nclient.watchers(1)\n#=> POST /v1/teams/<team_name>/posts/1/watchers\n\nclient.add_watch(1)\n#=> POST /v1/teams/<team_name>/posts/1/watch\n\nclient.delete_watch(1)\n#=> DELETE /v1/teams/<team_name>/posts/1/watch\n\nclient.batch_move({})\n#=> POST /v1/teams/<team_name>/posts/1/watch\n\nclient.regenerate_invitation()\n#=> POST /v1/teams/<team_name>/invitation_regenerator\n\nclient.send_invitation({"member": {"emails": ["foo@example.com"]})\n#=> POST /v1/teams/<team_name>/invitations\n\nclient.delete_invitation("mee93383edf699b525e01842d34078e28")\n#=> DELETE /v1/teams/<team_name>/invitations/mee93383edf699b525e01842d34078e28\n\nclient.invitations()\n#=> GET /v1/teams/<team_name>/invitations\n\nclient.emojis()\n#=> GET /v1/teams/<team_name>/emojis\n\nclient.create_emoji({"emoji": {"code": "funny", "image": base64}})\n#=> POST /v1/teams/<team_name>/emojis\n\nclient.delete_emoji("test_emoji")\n#=> DELETE /v1/teams/<team_name>/emojis/test_emoji\n\n```\n\n## Development\n\nissues and pull requests are always welcome!\n\nrun integration test\n\n``` shell\npython3 tests/integration_test.py\n```\n\nrun unit test\n\n``` shell\npython3 tests/<test_file>.py -v\n```',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
