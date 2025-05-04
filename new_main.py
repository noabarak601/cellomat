"""
main.py – entry point for Cell‑o‑mat (Pygame version)
"""

import subprocess
import sys

# --- make sure pygame is available ---
try:
    import pygame  # noqa: F401
except ModuleNotFoundError:
    print("⏳  Installing pygame (first run only)…")
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--quiet",
        "pygame",
    ])
    import pygame  # noqa: F401
    print("✅  pygame installed\n")

from gui_pygame import run_game  # now guaranteed to import

# ---------------------------------------------------------------------------
# OPTIONAL – keep the Tkinter welcome screen if you want interactive params:
# from gui import launch_welcome_screen
# size, pattern, p_alive, wraparound, skip_mode = launch_welcome_screen()
# ---------------------------------------------------------------------------

def main() -> None:
    """Launch the Pygame simulation with hard‑coded parameters.
    Replace these constants or gather them from the welcome screen."""
    run_game(
        size=200,            # board size (N×N)
        pattern="random",    # "random" or "special"
        p_alive=0.5,         # probability of 1 for random pattern
        wraparound=True,     # periodic boundaries
        skip_mode="auto",    # "auto" or "click"
    )


if __name__ == "__main__":
    main()
