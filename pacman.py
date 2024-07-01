import tkinter as tk
from PIL import Image, ImageTk
import winsound
import random

# Constants
CELL_SIZE = 40
WALL_COLOR = 'blue'
FOOD_COLOR = 'white'
BG_COLOR = 'black'
Delay = 500

# Game data
maze = [
    "**********************",
    "*....................*",
    "*..*...***.......***.*",
    "*..*...*....*..*..p*.*",
    "*..**....*.....*.*...*",
    "......................",
    ".......*.**p**........",
    "*.*..***.*ppp*..**.*.*",
    "*.*......pppp*..**.*.*",
    "*.**.....*****.......*",
    "*....***........****.*",
    "*.*..***...*..*......*",
    "*....***.*......*....*",
    "*.**.......*.*..***..*",
    "*........*...........*",
    "**********************"
]

maze_height = len(maze)
maze_width = max(len(row) for row in maze)

def create_maze(canvas):
    for row in range(maze_height):
        for col in range(maze_width):
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            if col >= len(maze[row]):
                canvas.create_rectangle(x1, y1, x2, y2, fill=WALL_COLOR)
            elif maze[row][col] == '*':
                canvas.create_rectangle(x1, y1, x2, y2, fill=WALL_COLOR)
            elif maze[row][col] == '.':
                food_id = canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=FOOD_COLOR, outline=BG_COLOR)
                food_positions.append((row, col, food_id))

def move_pacman(event):
    key = event.keysym
    if key == 'Up':
        rotate_pacman(270)
        move(0, -1)
    elif key == 'Down':
        rotate_pacman(90)
        move(0, 1)
    elif key == 'Left':
        rotate_pacman(180)
        move(-1, 0)
    elif key == 'Right':
        rotate_pacman(0)
        move(1, 0)

def rotate_pacman(angle):
    global pacman_image

    if angle == 0:
        pacman_image = pacman_right
    elif angle == 90:
        pacman_image = pacman_down
    elif angle == 180:
        pacman_image = pacman_left
    elif angle == 270:
        pacman_image = pacman_up

    canvas.itemconfig(pacman, image=pacman_image)


def game_over_win():
    canvas.delete('all')
    scored = 206 - (len(food_positions))
    canvas.create_text(canvas_width / 2, canvas_height / 2 - 50, text="VICTORY!!!", fill='white', font=('Arial', 20),
                       justify=tk.CENTER)
    button_no = tk.Button(canvas, text="EXIT", width=10, command=root.quit)
    button_no.place(x=canvas_width / 2 - 50, y=canvas_height / 2)
    button_sc = tk.Button(canvas, text=f"Score : {scored}", width=10)
    button_sc.place(x=canvas_width / 2 - 50, y=canvas_height / 1.7)
    

def game_over_lose():
    canvas.delete('all')
    scores = 206 - (len(food_positions))
    canvas.create_text(canvas_width / 2, canvas_height / 2 - 50, text="GAME OVER", fill='white', font=('Arial', 20),
                       justify=tk.CENTER)
    button_no = tk.Button(canvas, text="EXIT", width=10, command=root.quit)
    button_no.place(x=canvas_width / 2 - 50, y=canvas_height / 2)
    button_sc = tk.Button(canvas, text=f"Score : {scores}", width=10)
    button_sc.place(x=canvas_width / 2 - 50, y=canvas_height / 1.7)
    
    

def play_eat_sound():
    winsound.PlaySound("pacman_assets/pacman_eat.wav", winsound.SND_ASYNC)

def play_victory_sound():
    winsound.PlaySound("pacman_assets/victory.wav", winsound.SND_ASYNC)

def play_collision_sound():
    winsound.PlaySound("pacman_assets/lost.wav", winsound.SND_ASYNC)

def move(dx, dy):
    pacman_coords = canvas.coords(pacman)
    x = pacman_coords[0] + dx * CELL_SIZE
    y = pacman_coords[1] + dy * CELL_SIZE

    if 0 <= x < canvas_width and 0 <= y < canvas_height:
        if maze[int(y/CELL_SIZE)][int(x/CELL_SIZE)] != '*':
            check_food_collision(int(y/CELL_SIZE), int(x/CELL_SIZE))
            check_ghost_collision(int(y/CELL_SIZE), int(x/CELL_SIZE))
            canvas.move(pacman, dx * CELL_SIZE, dy * CELL_SIZE)


def check_food_collision(row, col):
    for i, (food_row, food_col, food_id) in enumerate(food_positions):
        if row == food_row and col == food_col:
            canvas.delete(food_id)
            del food_positions[i]
            play_eat_sound()
            break
    if len(food_positions) == 0:
        play_victory_sound()
        game_over_win()

def check_ghost_collision(row, col):
    global ghost, ghost2_pink, ghost3_blue

    ghost_coords = canvas.coords(ghost)
    ghost_x = int(ghost_coords[0] / CELL_SIZE)
    ghost_y = int(ghost_coords[1] / CELL_SIZE)

    if row == ghost_y and col == ghost_x:
        play_collision_sound()
        game_over_lose()

    ghost_coords2 = canvas.coords(ghost2_pink)
    ghost2_pink_x = int(ghost_coords2[0] / CELL_SIZE)
    ghost2_pink_y = int(ghost_coords2[1] / CELL_SIZE)

    if row == ghost2_pink_y and col == ghost2_pink_x:
        play_collision_sound()
        game_over_lose()

    ghost_coords3 = canvas.coords(ghost3_blue)
    ghost3_blue_x = int(ghost_coords3[0] / CELL_SIZE)
    ghost3_blue_y = int(ghost_coords3[1] / CELL_SIZE)

    if row == ghost3_blue_y and col == ghost3_blue_x:
        play_collision_sound()
        game_over_lose()

root = tk.Tk()
root.title("Pac-Man")
canvas = tk.Canvas(root, width=maze_width * CELL_SIZE, height=maze_height * CELL_SIZE, bg=BG_COLOR)
canvas.pack()

food_positions = []  # List to store food oval positions
create_maze(canvas)

# Load the Pac-Man images
pacman_right_image = Image.open("pacman_assets/pacman_right.png").resize((CELL_SIZE, CELL_SIZE))
pacman_left_image = Image.open("pacman_assets/pacman_left.png").resize((CELL_SIZE, CELL_SIZE))
pacman_up_image = Image.open("pacman_assets/pacman_up.png").resize((CELL_SIZE, CELL_SIZE))
pacman_down_image = Image.open("pacman_assets/pacman_down.png").resize((CELL_SIZE, CELL_SIZE))
pacman_close_1 = Image.open("pacman_assets/pacman_closed_right.png").resize((CELL_SIZE, CELL_SIZE))
pacman_close_2 = Image.open("pacman_assets/pacman_closed_left.png").resize((CELL_SIZE, CELL_SIZE))
pacman_close_3 = Image.open("pacman_assets/pacman_closed_up.png").resize((CELL_SIZE, CELL_SIZE))
pacman_close_4 = Image.open("pacman_assets/pacman_closed_down.png").resize((CELL_SIZE, CELL_SIZE))

pacman_closed_right = ImageTk.PhotoImage(pacman_close_1)
pacman_closed_left = ImageTk.PhotoImage(pacman_close_2)
pacman_closed_up = ImageTk.PhotoImage(pacman_close_3)
pacman_closed_down = ImageTk.PhotoImage(pacman_close_4)
pacman_right = ImageTk.PhotoImage(pacman_right_image)
pacman_left = ImageTk.PhotoImage(pacman_left_image)
pacman_up = ImageTk.PhotoImage(pacman_up_image)
pacman_down = ImageTk.PhotoImage(pacman_down_image)

pacman_x = CELL_SIZE * 1 + CELL_SIZE // 2
pacman_y = CELL_SIZE * 1 + CELL_SIZE // 2
pacman = canvas.create_image(pacman_x, pacman_y, image=pacman_right)

# Load the new first ghost image
ghost1_eyes_up_image = Image.open("pacman_assets/ghost1_right.png").resize((CELL_SIZE, CELL_SIZE))
ghost1_eyes_down_image = Image.open("pacman_assets/ghost1_left.png").resize((CELL_SIZE, CELL_SIZE))
ghost_eyes_open = ImageTk.PhotoImage(ghost1_eyes_up_image)
ghost_eyes_closed = ImageTk.PhotoImage(ghost1_eyes_down_image)

ghost = canvas.create_image(420, 300, image=ghost_eyes_closed)

# Load the second pink ghost
ghost2 = Image.open("pacman_assets/pink.png").resize((CELL_SIZE, CELL_SIZE))
ghost2_left_eyes = Image.open("pacman_assets/secondpink.png").resize((CELL_SIZE, CELL_SIZE))
ghost2_eyes_right = ImageTk.PhotoImage(ghost2)
ghost2_eyes_left = ImageTk.PhotoImage(ghost2_left_eyes)

ghost2_pink = canvas.create_image(450, 300, image=ghost2_eyes_left)

# Load the third blue ghost
ghost3 = Image.open("pacman_assets/blue.png").resize((CELL_SIZE, CELL_SIZE))
ghost3_left_eyes = Image.open("pacman_assets/seblue.png").resize((CELL_SIZE, CELL_SIZE))
ghost3_eyes_right = ImageTk.PhotoImage(ghost3)
ghost3_eyes_left = ImageTk.PhotoImage(ghost3_left_eyes)

ghost3_blue = canvas.create_image(490, 300, image=ghost3_eyes_left)

canvas_width = maze_width * CELL_SIZE
canvas_height = maze_height * CELL_SIZE

canvas.bind_all('<Key>', move_pacman)
canvas.focus_set()

frame = 0  # Frame counter for mouth animation



def move_ghost(ghost_id):
    ghost_coords = canvas.coords(ghost_id)
    pacman_coords = canvas.coords(pacman)
    ghost_x = ghost_coords[0]
    ghost_y = ghost_coords[1]
    pacman_x = pacman_coords[0]
    pacman_y = pacman_coords[1]

    dx = pacman_x - ghost_x
    dy = pacman_y - ghost_y

    if dx != 0:
        dx //= abs(dx)
    if dy != 0:
        dy //= abs(dy)

    new_x = ghost_x + dx * CELL_SIZE
    new_y = ghost_y + dy * CELL_SIZE

    if 0 <= new_x < canvas_width and 0 <= new_y < canvas_height:
        if maze[int(new_y / CELL_SIZE)][int(new_x / CELL_SIZE)] != '*':
            canvas.move(ghost_id, dx * CELL_SIZE, dy * CELL_SIZE)

def animate_mouth():
    global frame
    frame += 1

    pacman_direction = canvas.itemcget(pacman, "image")  # Get the current Pac-Man image

    if frame % 2 == 0:
        if pacman_direction == str(pacman_right):
            canvas.itemconfig(pacman, image=pacman_right)
        elif pacman_direction == str(pacman_left):
            canvas.itemconfig(pacman, image=pacman_left)
        elif pacman_direction == str(pacman_up):
            canvas.itemconfig(pacman, image=pacman_up)
        elif pacman_direction == str(pacman_down):
            canvas.itemconfig(pacman, image=pacman_down)
    else:
        if pacman_direction == str(pacman_right):
            canvas.itemconfig(pacman, image=pacman_closed_right)
        elif pacman_direction == str(pacman_left):
            canvas.itemconfig(pacman, image=pacman_closed_left)
        elif pacman_direction == str(pacman_up):
            canvas.itemconfig(pacman, image=pacman_closed_up)
        elif pacman_direction == str(pacman_down):
            canvas.itemconfig(pacman, image=pacman_closed_down)

    root.after(100, animate_mouth)

animate_mouth()

# For animation of first red ghost
def animate_red_ghost():
    global frame
    frame += 1

    # Alternate between open and closed mouth based on frame count
    if frame % 2 == 0:
        canvas.itemconfig(ghost, image=ghost_eyes_open)
    else:
        canvas.itemconfig(ghost, image=ghost_eyes_closed)

    # Move the ghost towards pacman
    move_ghost(ghost)

    # Schedule the next animation frame
    root.after(300, animate_red_ghost)

animate_red_ghost()

# For animation of second pink ghost
def animate_pink_ghost():
    global frame
    frame += 1

    # Alternate between open and closed mouth based on frame count
    if frame % 2 == 0:
        canvas.itemconfig(ghost2_pink, image=ghost2_eyes_right)
    else:
        canvas.itemconfig(ghost2_pink, image=ghost2_eyes_left)

    # Move the ghost towards pacman
    move_ghost(ghost2_pink)

    # Schedule the next animation frame
    root.after(300, animate_pink_ghost)

animate_pink_ghost()

# For animation of third blue ghost
def animate_blue_ghost():
    global frame
    frame += 1

    # Alternate between open and closed mouth based on frame count
    if frame % 2 == 0:
        canvas.itemconfig(ghost3_blue, image=ghost3_eyes_right)
    else:
        canvas.itemconfig(ghost3_blue, image=ghost3_eyes_left)

    # Move the ghost towards pacman
    move_ghost(ghost3_blue)

    # Schedule the next animation frame
    root.after(300, animate_blue_ghost)

animate_blue_ghost()

root.mainloop()