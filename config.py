import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_USERNAME = os.getenv("PROFILE_USERNAME")
GITHUB_TOKEN = os.getenv("PROFILE_GITHUB_TOKEN")

GRAPHQL_URL = "https://api.github.com/graphql"

ASSETS_DIR = "assets"
