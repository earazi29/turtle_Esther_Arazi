# Turtle Village — Lite (Student Scaffold)
# Focus: loops, decisions, try/except, and small functions.
# Run this file locally (IDLE/Thonny/PyCharm).

# ===>>>  REMOVE PASS IN ALL METHODS TO CODE

# NOTE about Turtle coordinate axis.
# turtle centers the origin (x == 0, y == 0 ) in the center of the canvas
# so if our default screen size is : CANVAS_W, CANVAS_H = 800, 600
#  the corners of your screen are :
# Top-left: (-CANVAS_W/2, CANVAS_H/2) → (-400, 300)
# Top-right: ( CANVAS_W/2, CANVAS_H/2) → ( 400, 300)
# Bottom-left: (-CANVAS_W/2, -CANVAS_H/2) → (-400, -300)
# Bottom-right: ( CANVAS_W/2, -CANVAS_H/2) → ( 400, -300)

import turtle as T
import random

# ---------- constants ----------
CANVAS_W, CANVAS_H = 800, 600
TOP_MARGIN, BOTTOM_MARGIN = 40, 40

# size of houses
SIZES = {
    "s": (120, 80),
    "m": (150, 100),
    "l": (180, 120),
}

'''
How to use Themes : 
# Use a theme like this:
colors = THEMES[theme_key]          # where theme_key is either "pastel" or "primary"
body_c  = colors["body"]            # we then can access the colors for the body of the house
roof_c  = colors["roof"]            # color of the roof of the house 
door_c  = colors["door"]            # door 
win_c   = colors["window"]          # window -- feel free to add or change the colors 
                                    # there is are beautiful pallette choices at coolors.co

# how to apply :
fill_rect_center(cx, cy, w, h, body_c)  # house body
'''
THEMES = {
    "pastel": dict(body="#ffd1dc", roof="#c1e1c1", door="#b5d3e7", window="#fff7ae"),
    "primary": dict(body="red", roof="blue", door="gold", window="#aee3ff"),
}


# ---------- tiny turtle helpers (provided) ----------
def move_to(x, y):
    '''
    x - position on x coordinate axis
    y - position on y coordinate axis
    '''
    T.penup()
    T.goto(x, y)
    T.pendown()


def draw_line(x1, y1, x2, y2):
    '''
       we draw a line from x1,y1
       to x2, y2
    '''
    move_to(x1, y1)
    T.pendown()
    T.goto(x2, y2)
    T.penup()


def fill_rect_center(cx, cy, w, h, color):
    '''
    cx - center of rectangle x coordinate
    cy - center of rectangle y coordinate
    w - width of rectangle
    h - height of rectangle
    color - color of rectangle
    '''
    T.fillcolor(color)
    T.pencolor("black")
    move_to(cx - w / 2, cy + h / 2)
    T.begin_fill()
    for _ in range(2):
        T.forward(w)
        T.right(90)
        T.forward(h)
        T.right(90)
    T.end_fill()


def fill_triangle(p1, p2, p3, color):
    """
    Draw a filled triangle defined by three points.
    """
    T.fillcolor(color)
    T.pencolor("black")
    move_to(*p1)
    T.begin_fill()
    T.goto(*p2)
    T.goto(*p3)
    T.goto(*p1)
    T.end_fill()


def fill_circle_center(cx, cy, r, color):
    '''
    a circle is defined by
    cx - the center of your circle, x coordinate
    cy - center of your circle, y coordinate
    r - radius
    color - color of circle
    '''
    T.fillcolor(color)
    T.pencolor("black")
    move_to(cx, cy - r)  # turtle draws circles from the bottom
    T.begin_fill()
    T.circle(r)
    T.end_fill()


# ---------- input helpers ----------
def ask_choice_int(prompt, allowed):
    """Ask for an integer in the allowed set; reprompt on error."""
    allowed_set = set(allowed)
    prompt = prompt + str(allowed_set) + ": "
    while True:
        try:
            user_input = int(input(prompt))
            if user_input not in allowed_set:
                raise ValueError("Invalid Input")
            return user_input
        except ValueError:
            print("Invalid Input — please try again.")


def ask_choice_str(prompt, allowed):
    """Ask for a string in the allowed list (case-insensitive); reprompt on error."""
    allowed_lower = [a.lower() for a in allowed]
    prompt = prompt + str(allowed_lower) + ": "
    while True:
        try:
            user_input = input(prompt).lower().strip()
            if user_input not in allowed_lower:
                raise ValueError("Invalid Input")
            return user_input
        except ValueError:
            print("Invalid Input — please try again.")


# ---------- draw_roads ----------
def draw_roads(cols, rows, cell_w, cell_h):
    """Draw straight separator lines between rows and columns (simple roads)."""
    top_y = CANVAS_H / 2 - TOP_MARGIN
    bot_y = -CANVAS_H / 2 + BOTTOM_MARGIN
    left_x = -CANVAS_W / 2
    right_x = CANVAS_W / 2

    T.pencolor("black")
    T.pensize(2)

    # Horizontal lines
    for r in range(1, rows):
        y = top_y - r * cell_h
        draw_line(left_x, y, right_x, y)

    # Vertical lines
    for c in range(1, cols):
        x = left_x + c * cell_w
        draw_line(x, top_y, x, bot_y)


# ---------- draw_house_centered ----------
def draw_house_centered(cx, cy, size_key, theme_key, roof_style):
    """Draw a simple house centered at (cx, cy)."""
    w, h = SIZES[size_key]
    colors = THEMES[theme_key]

    # Body
    fill_rect_center(cx, cy, w, h, colors["body"])

    # Roof
    yT = cy + h / 2
    if roof_style == "triangle":
        p1 = (cx - w / 2, yT)
        p2 = (cx + w / 2, yT)
        p3 = (cx, yT + 0.5 * h)
        fill_triangle(p1, p2, p3, colors["roof"])
    else:
        fill_rect_center(cx, yT + h * 0.1, w, h * 0.2, colors["roof"])

    # Door
    door_w, door_h = w * 0.25, h * 0.52
    fill_rect_center(cx, cy - h * 0.22, door_w, door_h, colors["door"])

    # Window
    win_w, win_h = w * 0.2, h * 0.2
    fill_rect_center(cx - w * 0.25, cy + h * 0.1, win_w, win_h, colors["window"])


# ---------- draw_tree_near ----------
def draw_tree_near(cx, cy, size_key):
    """Draw a small tree near the house (left or right)."""
    w, h = SIZES[size_key]
    tw, th = w * 0.10, h * 0.40
    side = random.choice([-1, 1])
    tx = cx + side * (w * 0.45)
    ty = cy - h * 0.5 + th / 2
    fill_rect_center(tx, ty, tw, th, "#8B4513")  # trunk
    fill_circle_center(tx, ty + th / 2 + h * 0.15, w * 0.18, "#5DAE4D")  # leaves


# ---------- draw_village ----------
def draw_village(cols, rows, size_key, theme_key, sun_flag, roof_style):
    """Compute cell sizes, draw roads, and loop over grid to place houses/trees."""
    cell_w = CANVAS_W / cols
    cell_h = (CANVAS_H - TOP_MARGIN - BOTTOM_MARGIN) / rows

    draw_roads(cols, rows, cell_w, cell_h)

    top_y = CANVAS_H / 2 - TOP_MARGIN
    left_x = -CANVAS_W / 2

    for r in range(rows):
        for c in range(cols):
            cx = left_x + (c + 0.5) * cell_w
            cy = top_y - (r + 0.5) * cell_h
            draw_house_centered(cx, cy, size_key, theme_key, roof_style)
            draw_tree_near(cx, cy, size_key)

    # Optional sun
    if sun_flag == 'y':
        r = 35
        cx = CANVAS_W / 2 - r - 12
        cy = CANVAS_H / 2 - r - 12
        fill_circle_center(cx, cy, r, "yellow")


# ---------- main ----------
def main():
    print("Welcome to Turtle Village — Lite!")
    cols = ask_choice_int("How many houses per row?", [2, 3])
    rows = ask_choice_int("How many rows?", [2])
    size_key = ask_choice_str("House size", ["S", "M", "L"]).lower()
    theme_key = ask_choice_str("Color theme", ["pastel", "primary"])
    roof_style = ask_choice_str("Roof type", ["triangle", "flat"]).lower()
    sun_flag = ask_choice_str("Draw a sun?", ["y", "n"]).lower()

    # Setup window
    T.setup(CANVAS_W, CANVAS_H)
    T.speed(0)
    T.tracer(False)

    # Draw the village
    draw_village(cols, rows, size_key, theme_key, sun_flag, roof_style)

    T.tracer(True)
    T.hideturtle()
    T.done()

if __name__ == "__main__":
    main()
