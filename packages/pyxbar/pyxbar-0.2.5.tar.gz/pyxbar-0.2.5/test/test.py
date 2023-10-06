#!/usr/bin/env python3
import sys
from pathlib import Path


def install(pkg: str, *pipargs: str):
    sys.path += [] if (sp := f"{Path(__file__)}.site-packages") in sys.path else [sp]
    try:
        __import__(pkg)
    except ImportError:
        install_args = ["install", "--upgrade", f"--target={sp}", *(pipargs or [pkg])]
        getattr(__import__("pip"), "main")(install_args)
        __import__(pkg)


install("pyxbar", Path(__file__).parent.parent.as_posix())


from pyxbar import Config, Divider, Menu, MenuItem, get_config  # noqa: E402


class MyConfig(Config):
    MYVARIABLE: bool = True
    ...


CONFIG = get_config(MyConfig)  # type: ignore


if __name__ == "__main__":
    Menu("some title").with_items(
        Divider(),  # shortcut for ---, also handles submenu depth
        MenuItem(
            "👁️ overview",
        )
        .with_submenu(
            MenuItem("hi, i'm a submenu!").with_alternate(
                MenuItem("hi, i'm alternate!"),
            ),
            MenuItem("hi, i'm monospace!", monospace=True),
        )
        .with_alternate("👁️ overview-alt", font="monospace", color="red"),
    ).print()
