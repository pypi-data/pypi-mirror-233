#!/usr/bin/env python

import os
import sys

import numpy as np

from emzed.remote_package import RemoteModule, setup_remote_venv
from emzed.config import folders

if "pyopenms" not in sys.modules:
    print("start remote ip", sys.executable)

    env_path = os.path.join(folders.get_emzed_folder(), "pyopenms_venv")

    PYOPENMS_VERSION = "3.0.0"

    python_venv_exe = setup_remote_venv(
        env_path,
        [
            ("pyopenms", PYOPENMS_VERSION),
            ("numpy", str(np.__version__)),
        ],
    )

    pyopenms = sys.modules["pyopenms"] = RemoteModule(python_venv_exe, "pyopenms")
    here = os.path.dirname(os.path.abspath(__file__))
    pyopenms.load_optimizations(os.path.join(here, "optimizations.py"))

else:
    print("skip start remote pyopenms.")


def encode(s):
    if isinstance(s, str):
        return s.encode("utf-8")
    return s


def decode(s):
    if isinstance(s, bytes):
        return str(s, "utf-8")
    return s
