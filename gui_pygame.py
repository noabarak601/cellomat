import pygame, sys
import tkinter as tk
from tkinter import ttk
from logic import create_random_matrix, create_glider_matrix, nextGen
import copy
from estimators import update_stats
import math

# -------------------------------------------------
WINDOW_PX   = 800
BOTTOM_BAR  = 40               # height of the control bar
ALIVE_COLOR = (220,  70, 120)
DEAD_COLOR  = (250, 250, 200)
GRID_COLOR  = ( 80,  80,  80)
BAR_COLOR   = (230, 230, 230)
BTN_COLOR   = (200, 200, 200)
TXT_COLOR   = ( 30,  30,  30)
FPS         = 30
# -------------------------------------------------




TABLE_ROWS  = [
    "Stability", "Birth Rate", "Death Rate"
]
TABLE_COLS  = ["Average", "Standard deviation", "Maximum", "Minimum"]
def create_map():
    map  = {}
    for par in TABLE_COLS:
        map[par] = {}
    for est in TABLE_ROWS:
        map["Average"][est] = 0
        map["Standard deviation"][est] = float('inf')
        map["Maximum"][est] = float('-inf')
        map["Minimum"][est] = float('inf')
    return map


def show_summary(steps, board_size:int, pattern:str,
                 probability:float, wraparound:bool,
                 stats):
    """
    Pygame summary window with a metrics table.
    `stats` – dict mapping each row heading -> value (None ⇒ blank).
    """


    # ------------- init ----------------------------------------------------
    pygame.init()
    W, H = 1160, 580
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Run summary")

    BG   = (245, 230, 217)
    GRID = (216, 203, 191)
    EDGE = ( 40,  40,  40)
    BOX  = (255, 255, 255)
    BTN  = (220, 220, 220)

    font   = pygame.font.SysFont(None, 24)
    bold   = pygame.font.SysFont(None, 24, bold=True)

    close_rect = pygame.Rect(W-110, H-55, 80, 30)

    # ------------ helpers --------------------------------------------------
    def draw_table(top_x: int, top_y: int, row_h: int, col_w: int):
        # 1) Column headings
        for j, col in enumerate(TABLE_COLS):
            txt = bold.render(col, True, EDGE)
            cell = pygame.Rect(top_x + (j + 1) * col_w, top_y, col_w, row_h)
            pygame.draw.rect(screen, BOX, cell)
            pygame.draw.rect(screen, EDGE, cell, 1)
            screen.blit(txt, txt.get_rect(center=cell.center))

        # 2) Row headings + values for each column
        for i, row in enumerate(TABLE_ROWS, start=1):
            # row heading
            rbox = pygame.Rect(top_x, top_y + i * row_h, col_w, row_h)
            pygame.draw.rect(screen, BOX, rbox)
            pygame.draw.rect(screen, EDGE, rbox, 1)
            txt = bold.render(row, True, EDGE)
            screen.blit(txt, txt.get_rect(center=rbox.center))

            # now draw each of the four columns
            for j, col in enumerate(TABLE_COLS, start=1):
                cell = pygame.Rect(top_x + j * col_w, top_y + i * row_h, col_w, row_h)
                pygame.draw.rect(screen, BOX, cell)
                pygame.draw.rect(screen, EDGE, cell, 1)

                # fetch the value from stats[col][row]
                val = stats.get(col, {}).get(row)
                if val is not None:
                    # format and render
                    vtxt = f"{val:.3g}"
                    surf = font.render(vtxt, True, EDGE)
                    screen.blit(surf, surf.get_rect(center=cell.center))

    # ------------- draw func ----------------------------------------------
    def draw():
        screen.fill(BG)
        for x in range(0, W, 40):
            pygame.draw.line(screen, GRID, (x, 0), (x, H))
        for y in range(0, H, 40):
            pygame.draw.line(screen, GRID, (0, y), (W, y))
        pygame.draw.rect(screen, EDGE, (20, 20, W-40, H-40), 2)



        # info strip (text only)
        info = f"Board Size: {board_size}    Steps: {steps}    Pattern: {pattern}"
        if pattern.startswith("random"):
            info += f"    Probability: {probability}"
        info += f"    Wrap around: {'true' if wraparound else 'false'}"
        screen.blit(bold.render(info, True, EDGE), (40, 50))



        # table
        draw_table(60, 110, row_h=32, col_w=180)

        # close button
        pygame.draw.rect(screen, BTN,  close_rect, border_radius=6)
        pygame.draw.rect(screen, EDGE, close_rect, 1,       border_radius=6)
        screen.blit(font.render("Close", True, EDGE),
                    font.render("Close", True, EDGE).get_rect(center=close_rect.center))

        pygame.display.flip()

    # ---------------- loop -------------------------------------------------
    running = True
    while running:
        draw()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if close_rect.collidepoint(ev.pos):
                    running = False
        pygame.time.wait(30)

    pygame.quit()

def run_game(size=100, pattern="random", p_alive=0.5,
             wraparound=False, skip_mode="auto", steps=250, delay_ms=200):
    skip_mode = "auto" if skip_mode.startswith("auto") else "click"
    FPS = max(1, 1000 // delay_ms)     # 100 ms → 10 FPS, 50 ms → 20 FPS
    if steps == '':
        steps = float('inf')
    board = (create_random_matrix(size, p_alive)
             if pattern == "random"
             else create_glider_matrix(size,pattern))
    gen = 1
    stats = create_map()

    # ---------- pygame init ----------
    pygame.init()
    font = pygame.font.SysFont("arial", 18)
    cell = max(2, WINDOW_PX // size)
    w, h = cell*size, cell*size + BOTTOM_BAR
    screen = pygame.display.set_mode((w, h))
    clock  = pygame.time.Clock()
    paused = (skip_mode == "click")

    # pre-build rectangles
    rects = [[pygame.Rect(c*cell, r*cell, cell-1, cell-1)
              for c in range(size)] for r in range(size)]

    # button geometry
    btn_rect = pygame.Rect(w-160, h-BOTTOM_BAR+5, 150, BOTTOM_BAR-10)

    running = True
    if isinstance(steps, float) and math.isinf(steps):
        limit = None  # no upper bound
    else:
        limit = int(steps)

    while running and (limit is None or gen < limit):
        # ----- events -----
        board_copy = copy.deepcopy(board)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key in (pygame.K_SPACE, pygame.K_UP):
                    paused = not paused
                elif e.key == pygame.K_RIGHT and paused:

                    nextGen(board, gen, wraparound)
                    gen += 1
            elif e.type == pygame.MOUSEBUTTONDOWN and paused and skip_mode == "click":
                if btn_rect.collidepoint(e.pos):

                    nextGen(board, gen, wraparound)
                    gen += 1

        # ----- model update -----
        if not paused and skip_mode == "auto":

            nextGen(board, gen, wraparound)
            gen += 1

        ##stats

        update_stats(stats,board,board_copy,gen-1)


        # ----- draw board -----
        for r, row in enumerate(board):
            for c, val in enumerate(row):
                pygame.draw.rect(screen,
                                 ALIVE_COLOR if val else DEAD_COLOR,
                                 rects[r][c])

        if GRID_COLOR:
            pygame.draw.rect(screen, GRID_COLOR,
                             pygame.Rect(0, 0, w, cell*size), 1)

        # ----- bottom bar & button -----
        pygame.draw.rect(screen, BAR_COLOR,
                         pygame.Rect(0, cell*size, w, BOTTOM_BAR))

        if skip_mode == "click":
            pygame.draw.rect(screen, BTN_COLOR, btn_rect, border_radius=8)
            txt = font.render("Next Generation", True, TXT_COLOR)
            txt_rect = txt.get_rect(center=btn_rect.center)
            screen.blit(txt, txt_rect)

        # ----- caption & flip -----
        pygame.display.set_caption(f"Cell-o-mat – Generation {gen}")
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    for val in stats["Average"]:
        if(gen == 1):
            stats["Average"][val] = stats["Average"][val] / (gen)
        else:
            stats["Average"][val] = stats["Average"][val]/(gen-1)
    show_summary(gen, size, pattern, p_alive, wraparound,stats)


#  sys.exit()


# quick test
if __name__ == "__main__":
    run_game(size=120, pattern="random",
             p_alive=0.5, wraparound=True, skip_mode="click")