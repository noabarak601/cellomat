from logic import print_matrix, nextGen
from ui import show_welcome_popup
from gui import launch_welcome_screen

def main():
    show_welcome_popup()

import sys, subprocess

# ---------------------------------------------------------------------------
#  On‑demand installation of required third‑party packages
# ---------------------------------------------------------------------------
def ensure_package(pkg_name: str):
    """
    Try to import *pkg_name*; if it fails, pip‑install it silently and re‑import.
    """
    try:
        __import__(pkg_name)
    except ModuleNotFoundError:
        print(f"⏳  Installing {pkg_name} (first run only)…")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--quiet", pkg_name
        ])
        __import__(pkg_name)
        print(f"✅  {pkg_name} installed\n")

# install-on‑demand
ensure_package("pygame")
ensure_package("numpy")
# ---------------------------------------------------------------------------

import pygame      # noqa: F401  (already guaranteed present)
import numpy as np # noqa: F401
4
if __name__ == "__main__":
    launch_welcome_screen()
