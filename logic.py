import random

def print_matrix(matrix):
    for row in matrix:
        # Print the row with fixed-width characters for alignment
        print(' '.join(f'{cell:2}' for cell in row))
    print()

def nextGen(matrix, generation, wraparound):
    m = (generation + 1) % 2
    n = len(matrix)
    for i in range(0, n - 1-m, 2):
        for j in range(0, n - 1-m, 2):
            change(matrix, i, j, m, n)
    if(wraparound and m == 1):
        wrap_around(matrix)

##change qquere
def change(matrix,i,j,m,n):
    life = 0
    ##count life
    if (matrix[i + m][j + m] == 1): life += 1
    if (matrix[(i + m + 1)%n][j + m] == 1): life += 1
    if (matrix[i + m][(j + m + 1)%n] == 1): life += 1
    if (matrix[(i + m + 1)%n][(j + m + 1)%n] == 1): life += 1
    ##change cells
    if (life == 2): return
    if (life == 3):
        if (matrix[i + m][j + m] == 0 or matrix[(i + m + 1)%n][(j + m + 1)%n] == 0):
            matrix[(i + m + 1)%n][j + m] = 0
            matrix[i + m][(j + m + 1)%n] = 0
        elif (matrix[(i + m + 1)%n][j + m] == 0 or matrix[i + m][(j + m + 1)%n] == 0):
            matrix[i + m][j + m] = 0
            matrix[(i + m + 1)%n][(j + m + 1)%n] = 0

    else:
        matrix[i + m][j + m] = (matrix[i + m][j + m] + 1) % 2
        matrix[(i + m + 1)%n][j + m] = (matrix[(i + m + 1)%n][j + m] + 1) % 2
        matrix[i + m][(j + m + 1)%n] = (matrix[i + m][(j + m + 1)%n] + 1) % 2
        matrix[(i + m + 1)%n][(j + m + 1)%n] = (matrix[(i + m + 1)%n][(j + m + 1)%n] + 1) % 2

def wrap_around(matrix):
    n = len(matrix)
    for i in range(1,n-1,2):
        change(matrix,i,n-1,0,n)
        change(matrix,n-1,i,0,n)
    change(matrix,n-1,n-1,0,n)

def create_random_matrix(size, p):
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if random.random() <= p:
                matrix[i][j] = 1
    return matrix
def create_anchor_matrix(size,glider):

    grid = [[0] * size for _ in range(size)]
    anchors = random_anchors(size)

    if anchors is None:
        anchors = [(size // 2 - 2, size // 2 - 2)]

    for r, c in anchors:
        if r >= size or c >= size or r < 0 or c < 0:
            continue
        grid[r][c] = 1

    return grid

import random

# ---- pattern dictionaries --------------------------------------------------

SPACESHIP_W = [(1,0),(1,3),(0,2),(0,1)]
SPACESHIP_E = [(0,0),(0,3),(1,2),(1,1)]
SPACESHIP_N = [(0,1),(3,1),(2,0),(1,0)]
SPACESHIP_S = [(0,0),(3,0),(2,1),(1,1)]


PATTERNS = {
    "spaceship_W":          SPACESHIP_W,
    "spaceship_E":        SPACESHIP_E,
    "spaceship_N":            SPACESHIP_N,
    "spaceship_S":              SPACESHIP_S,
}


# ---- helper ----------------------------------------------------------------

def create_glider_matrix(size: int, glider: str):
    """
    Return an `size × size` list‑of‑lists containing exactly one copy of the
    requested pattern in a random legal position (fully inside the board).

    Parameters
    ----------
    size : int
        Board side length  (must be >= pattern width/height)
    glider : str
        One of:  "SE_glider", "R_pantomino", "Diehard",
                 "Acron", "Gosper_Glider_Gun"

    Returns
    -------
    list[list[int]]
        Matrix filled with 0 (dead) except the pattern cells (1).
    """
    if glider not in PATTERNS:
        raise ValueError(f"Unknown pattern '{glider}'. "
                         f"Choose from {', '.join(PATTERNS)}")

    coords = PATTERNS[glider]

    # find pattern bounding box
    xs = [x for x, y in coords]
    ys = [y for x, y in coords]
    w = max(xs) - min(xs) + 1
    h = max(ys) - min(ys) + 1

    if size < max(w, h):
        raise ValueError(f"Board too small: pattern needs at least {max(w,h)}×{max(w,h)}")

    # choose random top‑left such that pattern fits

    left = random.randrange(1, size - w + 1, 2)
    top = random.randrange(1, size - h + 1, 2)



    # build empty matrix
    board = [[0] * size for _ in range(size)]

    # plant the pattern
    xmin, ymin = min(xs), min(ys)
    for x, y in coords:
        board[top + (y - ymin)][left + (x - xmin)] = 1

    return board


def random_anchors(size):
    anchors = []
    for i in range(1,size,2):
        for j in range(1,size,2):
            if(random.random() <= 1):
                anchors.append((i,j))
    return anchors








