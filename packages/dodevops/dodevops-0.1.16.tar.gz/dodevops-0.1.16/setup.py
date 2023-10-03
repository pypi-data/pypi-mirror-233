# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dodevops']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.28.57,<2.0.0',
 'botocore>=1.31.57,<2.0.0',
 'configparser>=6.0.0,<7.0.0',
 'coverage>=7.3.2,<8.0.0',
 'cryptography>=41.0.4,<42.0.0',
 'inquirer>=3.1.3,<4.0.0',
 'psycopg2-binary>=2.9.8,<3.0.0',
 'pydo>=0.1.7,<0.2.0',
 'python-dotenv>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['dodevops = dodevops.dodevops:main']}

setup_kwargs = {
    'name': 'dodevops',
    'version': '0.1.16',
    'description': 'Devops tool for deploying and managing resources on DigitalOcean',
    'long_description': '# **DoDevOps**\n\nDoDevOps is a tool for creating and managing Django apps on DigitalOcean\'s App Platform. \nIt accesses DigitalOcean through the API, so it requires a DigitalOcean API token,\nand it requires a DigitalOcean Spaces key for storing media uploads.\nAdditionally, you must authorize DigitalOcean to pull your GitHub repos.\n\n## Prerequisites:\n\n1) Python 3.9 on Linux or Mac\n2) DigitalOcean account https://www.digitalocean.com/?refcode=9ef6f738fd8a\n3) DigitalOcean API token: https://cloud.digitalocean.com/account/api/tokens\n4) DigitalOcean S3 keys: https://cloud.digitalocean.com/account/api/spaces\n5) Authorize DigitalOcean to pull your GitHub repos: https://cloud.digitalocean.com/apps/github/install\n\n# Installation\n\nThis tool can be installed with pip. \nIf installed in a Django project, it will try to detect some settings from the project such as repo and branch,\nas well as enable migration of db.json files and media uploads.\n\n```shell\npip install dodevops\n```\n\nTo run the tool:\n\n```shell\ndodevops\n```\n\n# Quickstart\n\n## Migrate an existing Django project to DigitalOcean App Platform\n\n1) Create a virtual environment \n   ```mkvirtualenv dodevops```\n2) Make sure pip is up to date\n   ```pip install --upgrade pip```\n3) Install dodevops\n   ```pip install dodevops```\n4) Change directory to wherever your Django app is\n5) Export environment variables\n    ```\n    export DIGITALOCEAN_API_TOKEN=dop_v1_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n    export AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxx\n    export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n    export MIGRATE_SCRIPT_1="python manage.py shell -c \\"import some_module; some_module.some_function()\\""\n    export MIGRATE_SCRIPT_2=""\n    ```\n6) Run dodevops\n    ```dodevops```\n\nTechnically the DoDevOps doesn\'t need it\'s own environment and can be installed in existing environments,\nbut sometimes isolation is nice.\n\nDoDevOps doesn\'t have to be run from within a Django folder,\nbut if .env or .git are available it will try and guess some of your settings for your. \nIt does require a /media folder in order to upload media folder to s3,\nand it does require db.json if migrating a previous database.\nExporting environment variables isn\'t required, if not supplied DoDevOps will ask the user to enter them at runtime. \n\nThe environment variables MIGRATE_SCRIPT_x can be used to hold lines of user supplied scripts for the migration job. \nThese are single shell lines executed as a pre-deploy task on the live DO server.\n\n# Details\n\n## Generating DO API token\n\nIn order for this app to work it needs a valid DigitalOcean Personal Access Token. \nThe token is not required after this is run, so it is okay to recyle the token when finished. \nThe token can either be stored in a .env file or env variable, or it can be pasted into the app at run time. \n\n### To generating a new token\n\nGo here: https://cloud.digitalocean.com/account/api/tokens\n\nPick whatever name you want for the token, it doesn\'t matter. \nPick whatever token expiration you want depending on your personal paranoia level. \nWrite permissions are required. \n\nOnce the token is generated copy it and paste it somewhere safe like a password manager such as 1password. \nThe token won\'t be displayed again, so if you don\'t get it saved somewhere safe you\'ll have to regenerate it.\n\nProtect your token well. \nAnyone with access to your token has the ability to create and destroy things and incur you costs, so be careful with it. \nThis is opensource so that you can read the code if you want and verify how the token is used. \nStoring the token in the .env file is convenient, but it is not the most secure, so if you feel paranoid don\'t do that. \n\nIf you want more info about DO tokens, see here: https://docs.digitalocean.com/reference/api/create-personal-access-token/\n\n## Generating DO Spaces Key\n\nA DO Spaces key is required for storing a media upload folder, as app platform doesn\'t have storage. \n\n### To generate an app spaces key \n\nGo here: https://cloud.digitalocean.com/account/api/spaces \n\nYou can use whatever name you want for the key, it doesn\'t matter. \nIt will display two values, a key ID and a longer access key, save both somewhere safe like a password manager. \nIt won\'t display the access key again, so if you don\'t save it you\'ll have to regenerate it. \n\nYou can put the values in an .env file, or enter it at runtime.\n\nProtect the token well.\n\nTo learn more about DO Spaces keys, go here: https://docs.digitalocean.com/products/spaces/how-to/manage-access/#access-keys\n\n## Filling out .env file\n\nA .env file isn\'t required, but if you store values in it then it will save effort.\nBut if you feel storing values in the .env file isn\'t secure enough for your personal paranoia levels you can instead enter things at runtime.\n\nThe format of the env file is:\n\n```\nDIGITALOCEAN_TOKEN=dop_v1_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nAWS_ACCESS_KEY_ID=DOxxxxxxxxxxxxxxxxxxx\nAWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n# AWS_REGION=ams3\n# APP_NAME=example-rest-app\n# COMPONENT_NAME=example-rest\n# APP_PREFIX=example\n# GH_REPO=xusernamex/xrepox\n# GH_BRANCH=main\n# DJANGO_ROOT_MODULE=example\n# DJANGO_USER_MODULE=core\n# SECRET_KEY_ENV_KEY=SECRET_KEY\n# SECRET_KEY=change_me\n# ALLOWED_HOSTS_ENV_KEY=ALLOWED_HOSTS\n# DEBUG=1\n# DOMAIN=rest.example.com\n# PARENT_DOMAIN=example.com\n# OIDC="\\"-----BEGIN RSA PRIVATE KEY-----\\\\n_xxx_\\\\n-----END RSA PRIVATE KEY-----\\\\n\\""\n```\n\n## Linux and Mac\n\nThis project uses inquirer to get user input. As far as I know it only works on linux and mac. \nWhen debugging in pycharm, you may need to set the run/debug settings to use the terminal emulation.\nYou can find a link with more info here: https://intellij-support.jetbrains.com/hc/en-us/community/posts/360003383619-Pycharm-2019-termios-error-25-Inappropriate-ioctl-for-device-?page=1#community_comment_6589796593042 and here https://github.com/magmax/python-readchar/issues/11\n',
    'author': 'Abby Oakwright',
    'author_email': 'abby.oakwright@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Oakwright/dodevops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
