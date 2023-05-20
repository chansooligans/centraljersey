import os
from pathlib import Path

import yaml


def setup():
    secrets_file = Path(__file__).resolve().parent.parent.joinpath("secrets.yml")
    if os.path.isfile(secrets_file):
        with open(secrets_file, "r") as file:
            secrets = yaml.load(file, Loader=yaml.FullLoader)
    else:
        secrets = {
            "census": {"api_key": os.environ["CENSUS_API_KEY"]},
        }
    return secrets