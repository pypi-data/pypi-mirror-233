"""autoset_pwd.__init__."""
__version__ = "1.0"
__copyright__ = "Copyright 2023 Libranet."
__license__ = "MIT License"

import os
import pathlib as pl


def entrypoint() -> None:
    """Set $PWD ans environment-variable."""
    pwd_dir = get_cwd()

    # set as env-var
    os.environ["PWD_DIR"] = str(pwd_dir)


def get_cwd() -> pl.Path:
    """Return the current working directory."""
    pwd_dir = pl.Path(os.getcwd())
    return pwd_dir