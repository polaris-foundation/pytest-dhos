# Import fixtures depending on which modules are available in the project.
import configparser
import os
from pathlib import Path

try:
    import flask_batteries_included  # noqa: F401

    from .flask_batteries_fixtures import *  # noqa: F403,F401
except ImportError:
    pass


def pytest_load_initial_conftests(early_config, parser, args):
    """implements the loading of initial conftest files ahead
    of command line option parsing.

    .. note::
        This hook will not be called for ``conftest.py`` files, only for setuptools plugins.

    :param _pytest.config.Config early_config: pytest config object
    :param list[str] args: list of arguments passed on the command line
    :param _pytest.config.Parser parser: to add command line options
    """
    rootdir = Path(early_config.rootdir)
    print("Early setup from tox.ini!")

    print("Load environment from tox.ini", early_config.rootdir)
    tox = rootdir / "tox.ini"
    if tox.exists():
        try:
            from flask_batteries_included.config import Configuration
        except ImportError:
            Configuration = None

        tox_config = configparser.ConfigParser()
        tox_config.read(rootdir / "tox.ini")
        if "testenv" not in tox_config or "setenv" not in tox_config["testenv"]:
            print(f"{tox} section [testenv] setenv not found")
            return

        test_environment = {
            k.strip(): v.strip()
            for k, _, v in [
                line.partition("=")
                for line in tox_config["testenv"]["setenv"].split("\n")
            ]
        }
        for k, v in test_environment.items():
            if k not in os.environ:
                os.environ[k] = v

            if Configuration is not None:
                setattr(Configuration, k, v)

            print(f"ENV {k}={v!r}")
