import numpy as np


# ---------------------------------------------------------------------------
#   change of generation
# ---------------------------------------------------------------------------

import math




def stability(prev: np.ndarray, curr: np.ndarray) -> float:
    """אחוז תאים שלא השתנו"""
    return np.mean(prev == curr)


def birth_rate(prev: np.ndarray, curr: np.ndarray) -> float:
    """אחוז תאים שעברו 0→1"""
    return np.mean((prev == 0) & (curr == 1))


def death_rate(prev: np.ndarray, curr: np.ndarray) -> float:
    """אחוז תאים שעברו 1→0"""
    return np.mean((prev == 1) & (curr == 0))


# ---------------------------------------------------------------------------
#   global status
# ---------------------------------------------------------------------------



def update_stats(stats, board, board_copy,gen):
    # Convert to np.ndarray once
    prev_np = np.array(board_copy, dtype=int)
    curr_np = np.array(board,      dtype=int)

    # 1) Stability

    curr_stability = stability(prev_np, curr_np)

    stats["Average"]["Stability"]      += curr_stability

    if(stats["Minimum"]["Stability"] > curr_stability):
        stats["Minimum"]["Stability"] = curr_stability

    if(stats["Maximum"]["Stability"] < curr_stability):
        stats["Maximum"]["Stability"] = curr_stability
    if(gen < 2):
        stats["Standard deviation"]["Stability"] = 0
    else:

        stats["Standard deviation"]["Stability"] = update_std(gen-1,stats["Average"]["Stability"]/gen,stats["Standard deviation"]["Stability"],curr_stability)

    # 2) Birth Rate
    curr_birthrate = birth_rate(prev_np, curr_np)
    stats["Average"]["Birth Rate"]     += curr_birthrate

    if (stats["Minimum"]["Birth Rate"] > curr_birthrate):
        stats["Minimum"]["Birth Rate"] = curr_birthrate

    if (stats["Maximum"]["Birth Rate"] < curr_birthrate):
        stats["Maximum"]["Birth Rate"] = curr_birthrate
    if(gen < 2):
        stats["Standard deviation"]["Birth Rate"] = 0
    else:
        stats["Standard deviation"]["Birth Rate"] = update_std(gen-1,
                                                           stats["Average"]["Birth Rate"]/gen,
                                                           stats["Standard deviation"]["Birth Rate"], curr_birthrate)

    # 3) Death Rate
    curr_deathrate = death_rate(prev_np, curr_np)
    stats["Average"]["Death Rate"]     += curr_deathrate

    if (stats["Minimum"]["Death Rate"] > curr_deathrate):
        stats["Minimum"]["Death Rate"] = curr_deathrate

    if (stats["Maximum"]["Death Rate"] < curr_deathrate):
        stats["Maximum"]["Death Rate"] = curr_deathrate
    if(gen < 2):
        stats["Standard deviation"]["Death Rate"] = 0
    else:
        stats["Standard deviation"]["Death Rate"] = update_std(gen-1,stats["Average"]["Death Rate"]/gen,stats["Standard deviation"]["Death Rate"],curr_deathrate)






def update_std(n: int, mean: float, std: float, x: float) -> float:
    """
    Online update for sample‐standard‐deviation.
    n    – count of prior samples
    mean – prior running mean
    std  – prior running sample‐std (uses denom = n-1)
    x    – new sample

    Returns the new sample‐std after incorporating x.
    """
    # Reconstruct previous M2 from std: M2 = std^2 * (n-1)
    if(n == 0):
        mean = x
    else:
        mean = (mean*(n+1)-x)/n
    M2 = std**2 * (n-1) if n > 1 else 0.0

    # Incorporate the new sample
    n1    = n + 1
    delta = x - mean
    mean1 = mean + delta / n1
    M2   += delta * (x - mean1)

    # Compute new sample‐stddev (denom = n1-1)
    return math.sqrt(M2 / (n1 - 1)) if n1 > 1 else 0.0