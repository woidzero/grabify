"""
Grabify
~~~~~~~~~~~~~~~~~~~

🎼 A command-line tool that allows you to download artwork and metadata from Spotify 
tracks and albums without authentication.

:copyright: (c) 2023 woidzero
:license: MIT, see LICENSE for more details.
"""

import json
import os
from pathlib import Path


class Config:
    def __init__(self) -> None:
        self._path = os.getenv('LOCALAPPDATA') + "\\Grabify"
        self._filepath = self._path + "\\settings.json"

        self._download_path = (Path.home() / "Downloads\\Grabify").resolve()
        self._default_config = {
            "download_path": str(self._download_path),
            "format_filenames": True,
        }
        if not os.path.exists(self._path):
            self.create()

    def create(self) -> None:
        os.makedirs(self._path, exist_ok=True)

        with open(self._filepath, "w") as file:
            json.dump(self._default_config, file)

    def set(self, key, value) -> None:
        with open(self._filepath, "r") as file:
            data = json.load(file)

        data[key] = value
        data.update()

        with open(self._filepath, "w") as file:
            json.dump(data, file)

    def get(self, key) -> None:
        with open(self._filepath, "r") as file:
            data = json.load(file)

        return data[key]

    def to_dict(self) -> dict:
        with open(self._filepath, "r") as file:
            return json.load(file)

    def to_str(self) -> str:
        data = self.to_dict()
        res = ""

        for key in data.keys():
            value = data[key]
            res += f"{key}: {value}\n"

        return res


cfg = Config()
