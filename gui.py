import tkinter as tk
from tkinter import ttk, messagebox, font
from logic import create_random_matrix

from gui_pygame import run_game


# gui.py  (תחילת הקובץ)

# --- make sure pygame is available ---
try:
    import pygame
except ModuleNotFoundError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pygame"])
    import pygame
# -------------------------------------

from gui_pygame import run_game      # <-- נוסיף  import חדש


def launch_welcome_screen():
    def is_natural_number(new_value):
        return new_value == "" or (new_value.isdigit() and int(new_value) > 0)

    def is_valid_odds(new_value):
        if new_value == "":
            return True
        try:
            val = float(new_value)
            return 0 <= val <= 1
        except ValueError:
            return False

    def is_valid_delay(new_value):
        return new_value == "" or (new_value.isdigit() and int(new_value) > 0)

    def on_pattern_change(event=None):
        if pattern_var.get() == "random":
            special_frame.pack_forget()
            odds_label.pack(anchor="w", pady=(10, 0))
            odds_entry.pack(fill="x")
        else:
            odds_label.pack_forget()
            odds_entry.pack_forget()
            special_frame.pack(anchor="w", fill="x", pady=(10, 0))

        # Re-pack the start button at the bottom
        start_button.pack_forget()
        start_button.pack(pady=20)

    def show_matrix_as_text(matrix):
        game_root = tk.Tk()
        game_root.title("Cell-o-mat Board")

        for i in range(len(matrix)):
            row_text = "  ".join(str(cell) for cell in matrix[i])
            row_label = tk.Label(game_root, text=row_text, font=("Courier", 14))
            row_label.pack(anchor="w", padx=10)

        game_root.mainloop()

    import tkinter as tk

    from logic import nextGen
    import time

    def show_matrix(matrix,skip_mode,wrap_around = False,initial_generation=1):

        size = len(matrix)
        canvas_size = 600
        cell_size = canvas_size // size
        generation = [initial_generation]

        game_root = tk.Tk()
        game_root.title("Cell-o-mat Board")

        # --- Top Frame ---
        top_frame = tk.Frame(game_root)
        top_frame.pack(fill="x", padx=10, pady=(10, 5))

        gen_label = tk.Label(top_frame, text=f"Generation: {generation[0]}", anchor="w", font=("Helvetica", 12))
        gen_label.pack(side="left")

        title_label = tk.Label(top_frame, text="Cell-O-Mat", font=("Helvetica", 18, "bold"))
        title_label.pack(side="top", expand=True)

        # --- Canvas ---
        canvas = tk.Canvas(game_root, width=canvas_size, height=canvas_size, bg='white', highlightthickness=0)
        canvas.pack()

        # --- Draw once, store refs ---
        cell_rects = [[None for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                x0 = j * cell_size
                y0 = i * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                color = "pink" if matrix[i][j] == 1 else "light yellow"
                rect = canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")
                cell_rects[i][j] = rect

        def step():
            old_matrix = [row[:] for row in matrix]  # Copy current state
            nextGen(matrix, generation[0], wrap_around)
            generation[0] += 1
            gen_label.config(text=f"Generation: {generation[0]}")

            for i in range(size):
                for j in range(size):
                    if matrix[i][j] != old_matrix[i][j]:
                        color = "pink" if matrix[i][j] == 1 else "light yellow"
                        canvas.itemconfig(cell_rects[i][j], fill=color)

        if skip_mode == "click":

            control = tk.Frame(game_root)
            control.pack(fill="x", pady=(5, 10))

            next_btn = tk.Button(control,
                                 text="Next Generation ▶",
                                 command=step,
                                 font=("Helvetica", 12, "bold"))
            next_btn.pack(anchor="ne",padx=10,pady=10)
        else:

        # automatic mode – call step repeatedly

        # --- Efficient update loop ---
            def update_loop():
                start = time.time()

                generation[0] += 1
                nextGen(matrix, generation[0], wraparound=True)
                gen_label.config(text=f"Generation: {generation[0]}")

                for i in range(size):
                    for j in range(size):
                        color = "pink" if matrix[i][j] == 1 else "light yellow"
                        canvas.itemconfig(cell_rects[i][j], fill=color)

                elapsed = (time.time() - start) * 1000  # ms
                delay = max(50, int(100 - elapsed))  # maintain ~100ms/frame
                game_root.after(delay, update_loop)

            game_root.after(100, update_loop)
        game_root.mainloop()

    def on_start():
        size = size_entry.get()
        if not size or int(size) <= 0:
            messagebox.showerror("Invalid Input", "Board size must be a natural number greater than 0.")
            return
        if (int(size)%2 != 0):
            messagebox.showerror("Invalid Input", "Board size must be  Even.")
            return
        skip_mode = skip_var.get()
        wraparound = wraparound_var.get()
        pattern = pattern_var.get()
        if pattern == "special":
            pattern = special_pattern_var.get()
        odds = 0
        if pattern == "random":
            odds_val = odds_entry.get()
            try:
                odds = float(odds_val)
                if not (0 <= odds <= 1):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Input", "Odds must be a number between 0 and 1.")
                return
        delay_val = delay_entry.get() or "200"
        delay_ms = int(delay_val)



        size = int(size)
        root.destroy()

        steps = steps_var.get()
        if steps:
            try:
                steps_int = int(steps)
                if steps_int < 2:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Input", "Steps must be an integer greater than or equal to 2.")
                return
        else:
            steps_int = 0  # or some default if steps are optiona
        run_game(size=size,
                 pattern=pattern,
                 p_alive=odds,
                 wraparound=wraparound,
                 skip_mode=skip_mode,
                 steps=steps,
                 delay_ms=delay_ms)

    # --- Tkinter setup ---
    root = tk.Tk()
    root.title("Welcome to my Cell-o-mat")
    root.geometry("800x800")
    root.resizable(False, False)


    frame = ttk.Frame(root, padding="20")
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Welcome to my Cell-o-mat", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))
    ttk.Label(frame, text="Please fill out your rules:", font=("Helvetica", 12)).pack()

    ttk.Label(frame, text="Board size:", font=("Helvetica", 10)).pack(anchor="w", pady=(10, 0))
    vcmd_size = (root.register(is_natural_number), '%P')
    size_entry = ttk.Entry(frame, validate="key", validatecommand=vcmd_size)
    size_entry.pack(fill="x")

    ttk.Label(frame, text="Skip generation:", font=("Helvetica", 10)).pack(anchor="w", pady=(10, 0))
    skip_var = tk.StringVar(value="automatically")
    ttk.Combobox(frame, textvariable=skip_var, values=["automatically", "click"], state="readonly").pack(fill="x")

    ttk.Label(frame, text="Steps", font=("Helvetica", 10)).pack(anchor="w", pady=(10, 0))
    steps_var = tk.StringVar()
    vcmd_steps = (root.register(is_natural_number), '%P')
    steps_entry = ttk.Entry(frame, textvariable=steps_var, validate="key", validatecommand=vcmd_steps)
    steps_entry.pack(fill="x")

    ttk.Label(frame, text="Pattern:", font=("Helvetica", 10)).pack(anchor="w", pady=(10, 0))
    pattern_var = tk.StringVar(value="random")
    pattern_menu = ttk.Combobox(frame, textvariable=pattern_var, values=["random", "special"], state="readonly")
    pattern_menu.pack(fill="x")
    pattern_menu.bind("<<ComboboxSelected>>", on_pattern_change)

    # For special pattern options (initially hidden)
    special_pattern_var = tk.StringVar(value="Anchors")  # default value

    special_frame = ttk.LabelFrame(frame, text="Special Pattern Options", padding=(10, 5))
    spaceship_E = ttk.Radiobutton(special_frame, text="Spaceship East", variable=special_pattern_var, value="spaceship_E")
    spaceship_W = ttk.Radiobutton(special_frame, text="Spaceship West", variable=special_pattern_var, value="spaceship_W")
    spaceship_N = ttk.Radiobutton(special_frame, text="Spaceship North", variable=special_pattern_var, value="spaceship_N")
    spaceship_S = ttk.Radiobutton(special_frame, text="Spaceship South", variable=special_pattern_var, value="spaceship_S")
    zero = ttk.Radiobutton(special_frame, text="zero", variable=special_pattern_var,value="zero")
    columns = ttk.Radiobutton(special_frame, text="columns", variable=special_pattern_var, value="columns")
    squares = ttk.Radiobutton(special_frame, text="squares", variable=special_pattern_var,value="squares")



    spaceship_E.pack(anchor="w")
    spaceship_W.pack(anchor="w")
    spaceship_N.pack(anchor="w")
    spaceship_S.pack(anchor="w")
    zero.pack(anchor="w")
    columns.pack(anchor="w")
    squares.pack(anchor="w")

    special_frame.pack_forget()  # hide initially


    odds_label = ttk.Label(frame, text="Probability (0 to 1):", font=("Helvetica", 10))
    vcmd_odds = (root.register(is_valid_odds), '%P')
    odds_entry = ttk.Entry(frame, validate="key", validatecommand=vcmd_odds)
    odds_label.pack(anchor="w", pady=(10, 0))
    odds_entry.insert(0,"0.5")
    odds_entry.pack(fill="x")

    ttk.Label(frame, text="Delay between generations (ms):",
              font=("Helvetica", 10)).pack(anchor="w", pady=(10, 0))
    vcmd_delay = (root.register(is_valid_delay), '%P')
    delay_entry = ttk.Entry(frame, validate="key", validatecommand=vcmd_delay)
    delay_entry.insert(0, "200")
    delay_entry.pack(fill="x")


    wraparound_var = tk.BooleanVar(value=False)
    wrap_cb = ttk.Checkbutton(frame, text="Wrap-around",variable=wraparound_var)
    wrap_cb.config(width=250)
    wrap_cb.pack(anchor="w", pady=(10, 0))

    # holds the state
    # tk.Checkbutton(root, text="Wrap-around",  # the checkbox
    #                variable=wraparound_var).pack(anchor="w")
      # ~25 text chars wide


    start_button = ttk.Button(frame, text="Start Game", command=on_start)
    start_button.pack(pady=20)

    root.mainloop()