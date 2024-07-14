"""
Hardcoded settings for providing constants to the app.

I could have used .env file, but i would like keep it simple.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATE_FORMATE = '%d.%m.%Y %H:%M:%S'
REPO_ROOT_URL = 'https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents'
