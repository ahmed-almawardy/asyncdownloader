"""
Hardcoded settings for providing constants to the app.

I could have used .env file, but i would like keep it simple.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'https://gitea.radium.group/'
API_VERSION = 'api/v1/'
REPO_ROOT_URL = '{0}{1}repos/radium/project-configuration/contents'.format(
    BASE_URL,
    API_VERSION,
)
