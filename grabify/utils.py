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
from typing import Any, Optional, Union

import requests
from rich.theme import Theme

theme = Theme(
    {
        "info": "bold blue",
        "warn": "bold yellow",
        "err": "bold red",
        "ok": "bold green",
    }
)


def uniquify(path: str) -> str:
    """
    Ensure a filename is unique by adding a number to the end if necessary.
    This is useful for generating filenames that are unique across the filesystem.
    """
    base, ext = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = f"{base}_{counter}{ext}"
        counter += 1

    return path


def save(
    path: str,
    filename: str,
    image_url: Optional[str] = None,
    json_data: Optional[dict] = None,
) -> Union[str, Any]:
    """
    Save file to path. If image_url is provided it will be downloaded
    and saved as jpg file.
    """
    dirc = str(Path(path).resolve()) + os.sep
    os.makedirs(dirc, exist_ok=True)

    ext = ".jpg" if image_url else ".json"
    dist = uniquify(dirc + filename + ext)

    if image_url:
        data = requests.get(image_url, timeout=60).content
        with open(dist, "wb+") as file:
            file.write(data)
    else:
        data = json.dumps(json_data)
        with open(dist, "w+", encoding="utf-8") as file:
            file.write(data)

    return dist


def get_data_dict(raw_data, _type, name, image_url) -> dict:
    """
    Converts data to dict. This is a helper function to make it easier to use in tests
    """
    raw_data = str(raw_data).split(" · ")

    songs = int(raw_data[-1].replace("songs", "").replace(".", ""))

    data = {
        "name": name,
        "image_url": image_url,
        "type": _type,
        "songs": songs,
    }

    if _type != "music.playlist":
        data.update({"year": raw_data[2], "author": raw_data[0]})

    if _type not in ("music.playlist", "music.song"):
        data.update({"songs": songs})

    if _type == "music.song":
        del data["songs"]

    return data
