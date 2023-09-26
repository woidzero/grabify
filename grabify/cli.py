"""
Grabify
~~~~~~~~~~~~~~~~~~~

🎼 A command-line tool that allows you to download artwork and metadata from Spotify 
tracks and albums without authentication.

:copyright: (c) 2023 woidzero
:license: MIT, see LICENSE for more details.
"""

import click
import requests
from bs4 import BeautifulSoup
from rich.console import Console

from . import __version__
from .config import cfg
from .utils import get_data_dict, save, theme

console = Console(theme=theme)


@click.group("grabify")
@click.version_option(__version__, "-v", "--version")
def grabify() -> None:
    """A command-line tool that allows you to download
    artwork and metadata from Spotify tracks and albums.
    """


@grabify.group("config")
def _config() -> None:
    """Manage config settings"""
    pass


@_config.command("set")
@click.argument("key")
@click.argument("value")
def _set(key, value) -> None:
    """Set config value"""
    try:
        if key not in cfg.to_dict():
            return console.print(f"[err]✖[/] No '{key}' found in the config.")

        cfg.set(key, value)

        console.print(f"[ok]✔[/] Config updated! '{key}' is set to '{value}'")
    except Exception as err:
        console.print(f"[err]✖[/] Unknown error: {err}")


@_config.command("view")
def _view() -> None:
    """View config values"""
    console.print(f"Config path: {cfg._filepath}\n")
    console.print(cfg.to_str())


@_config.command("reset")
def _reset() -> None:
    """Restore default settings"""
    cfg.create()
    console.print("[ok]✔[/] Config restored to default settings")


@grabify.command("art")
@click.argument("url")
@click.option("--path", "-p", help="Download path", default=cfg.get("download_path"))
def _art(url, path) -> None:
    """Downloads album/playlist/track artwork"""
    try:
        image_url = ""
        name = ""

        response = requests.get(url, timeout=60)
        soup = BeautifulSoup(response.text, features="lxml")

        for meta in soup.find_all("meta"):
            if meta.get("property") == "og:title":
                name = meta.get("content")
            if meta.get("property") == "og:image":
                image_url = meta.get("content")

        if None in (image_url, name):
            console.print("[err]✖[/] Failed to fetch data")

        saved_path = save(path, name, image_url=image_url)
        console.print(f"[ok]✔[/] Saved to {saved_path}")
    except requests.exceptions.MissingSchema:
        console.print("[err]✖[/] Incorrect URL")
    except requests.exceptions.Timeout:
        console.print("[err]✖[/] Connection timed out, try again later")


@grabify.command("data")
@click.argument("url")
@click.option("--path", "-p", help="Download path", default=cfg.get("download_path"))
def _data(url: str, path: str) -> None:
    """Downloads album/playlist/track metadata"""
    try:
        name = ""
        image_url = ""
        desc = ""
        _type = ""
        raw_data = ""

        response = requests.get(url, timeout=60)
        soup = BeautifulSoup(response.text, features="lxml")

        for meta in soup.find_all("meta"):
            if meta.get("property") == "og:title":
                name = meta.get("content")
            if meta.get("property") == "og:image":
                image_url = meta.get("content")
            if meta.get("property") == "og:description":
                raw_data = meta.get("content")
            if meta.get("property") == "og:type":
                _type = meta.get("content")

        if None in (image_url, name, desc):
            console.print("[err]✖[/] Failed to fetch data")

        data = get_data_dict(raw_data, _type, name, image_url)

        if cfg.get("format_filenames") is True:
            name = name.lower().replace(" ", "_")

        saved_path = save(path, name, json_data=data)
        console.print(f"[ok]✔[/] Saved to {saved_path}")
    except requests.exceptions.MissingSchema:
        console.print("[err]✖[/] Incorrect URL")
    except requests.exceptions.Timeout:
        console.print("[err]✖[/] Connection timed out, try again later")
