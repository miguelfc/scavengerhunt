from micropython import const
import badger2040
from badger2040 import UPDATE_NORMAL, UPDATE_MEDIUM, UPDATE_FAST, UPDATE_TURBO, BUTTON_A, BUTTON_B, BUTTON_C, BUTTON_DOWN, BUTTON_UP, WIDTH, HEIGHT
from time import sleep
import random
import gc

# **SCREEN IS USED IN PORTRAIT**

C = const

HALF_W = C(int(WIDTH/2))
HALF_H = C(int(HEIGHT/2))

CELL_SIDE = C(23)    # Num of px tall and wide
CELL_SPACING = C(3)  # Vert. and horiz. spacing between cell borders in the grid
# Top left of the grid
GRID_ORIGIN_X = C(int(HALF_W - (CELL_SIDE*3 + CELL_SPACING*2.5)))
GRID_ORIGIN_Y = C(int(HALF_H - (CELL_SIDE*2.5 + CELL_SPACING*2)))

CELL_FONT = C("serif")
CELL_FONT_SCALE = C(0.8)
HEADER_FONT = C("sans")

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
LETTERS = C(ALPHABET)

LETTERS_SIZE = len(ALPHABET)
# Grid data
grid = [[""]*5] * 6

display = badger2040.Badger2040()

### Functions ###

def _43CA490():
    return 0b00000000
def _404CA39():
    return 0b00000001
def _034CA49():
    return 0b00000010
def _0434CA9():
    return 0b00000011
def _4493CA0():
    return 0b00000100
def _9404CA3():
    return 0b00000101
def _0443CA9():
    return 0b00000110
def _94CA430():
    return 0b00000111
def _9CA4034():
    return 0b00001000
def _4430CA9():
    return 0b00001001
def _94CA340():
    return 0b00001010
def _44CA903():
    return 0b00001011
def _49CA340():
    return 0b00001100
def _CA39404():
    return 0b00001101
def _4CA0493():
    return 0b00001110
def _39CA044():
    return 0b00001111
def _40CA493():
    return 0b00010000
def _CA44903():
    return 0b00010001
def _934CA04():
    return 0b00010010
def _9CA4430():
    return 0b00010011
def _0944CA3():
    return 0b00010100
def _3CA9404():
    return 0b00010101
def _CA34409():
    return 0b00010110
def _9CA3404():
    return 0b00010111
def _0CA4349():
    return 0b00011000
def _CA43940():
    return 0b00011001
def _CA49043():
    return 0b00011010
def _0449CA3():
    return 0b00011011
def _940CA34():
    return 0b00011100
def _CA30494():
    return 0b00011101
def _0CA3449():
    return 0b00011110
def _39440CA():
    return 0b00011111
def _4490CA3():
    return 0b00100000
def _94CA043():
    return 0b00100001
def _40943CA():
    return 0b00100010
def _04934CA():
    return 0b00100011
def _4CA4903():
    return 0b00100100
def _9430CA4():
    return 0b00100101
def _0CA4394():
    return 0b00100110
def _3904CA4():
    return 0b00100111
def _CA94043():
    return 0b00101000
def _3490CA4():
    return 0b00101001
def _CA34904():
    return 0b00101010
def _34094CA():
    return 0b00101011
def _CA40349():
    return 0b00101100
def _CA90443():
    return 0b00101101
def _4CA0349():
    return 0b00101110
def _CA09434():
    return 0b00101111
def _0CA4943():
    return 0b00110000
def _04493CA():
    return 0b00110001
def _9034CA4():
    return 0b00110010
def _30CA449():
    return 0b00110011
def _39CA404():
    return 0b00110100
def _43CA904():
    return 0b00110101
def _4CA3049():
    return 0b00110110
def _30CA494():
    return 0b00110111
def _494CA30():
    return 0b00111000
def _940CA43():
    return 0b00111001
def _CA94430():
    return 0b00111010
def _9CA4304():
    return 0b00111011
def _30494CA():
    return 0b00111100
def _3CA4409():
    return 0b00111101
def _4304CA9():
    return 0b00111110
def _CA40493():
    return 0b00111111
def _CA40934():
    return 0b01000000
def _904CA34():
    return 0b01000001
def _4CA0943():
    return 0b01000010
def _3CA0449():
    return 0b01000011
def _04CA943():
    return 0b01000100
def _CA03944():
    return 0b01000101
def _90443CA():
    return 0b01000110
def _430CA49():
    return 0b01000111
def _49403CA():
    return 0b01001000
def _449CA30():
    return 0b01001001
def _04439CA():
    return 0b01001010
def _43CA094():
    return 0b01001011
def _CA94340():
    return 0b01001100
def _430CA94():
    return 0b01001101
def _CA04934():
    return 0b01001110
def _049CA34():
    return 0b01001111
def _4CA9340():
    return 0b01010000
def _93404CA():
    return 0b01010001
def _34CA409():
    return 0b01010010
def _0349CA4():
    return 0b01010011
def _443CA90():
    return 0b01010100
def _34CA940():
    return 0b01010101

def select_word(idx):
    # There are 2,309 winner words
    f = open("/examples/winners.txt", "r")
    f.seek(idx * 0b101)
    winner_word = f.read(0b101)
    f.close()
    gc.collect()
    return winner_word.upper()

def valid_word(word):
    if len(word) != 0b101:
        return False
    return True

def conv_grid_coords(x, y):
    """Converts portrait grid coords into landscape grid coords"""
    return 5-y, x

def draw_cell(x, y, outline, fill, text, char):
    x, y = conv_grid_coords(x, y)
    # Top left of this cell
    org_x = GRID_ORIGIN_X + CELL_SIDE*x + CELL_SPACING*x
    org_y = GRID_ORIGIN_Y + CELL_SIDE*y + CELL_SPACING*y
    # Fill block
    display.set_pen(fill)
    display.rectangle(org_x, org_y, CELL_SIDE+1, CELL_SIDE+1) # +1 because rectangle width/height isn't inclusive
    # Draw outline if needed
    if outline != fill:
        display.set_pen(outline)
        side = CELL_SIDE + 1 # Used a lot below, since line() doesn't go to the final point
        display.line(org_x, org_y, org_x+side, org_y) # Top
        display.line(org_x, org_y+side-1, org_x+side, org_y+side-1) # Bottom
        display.line(org_x, org_y, org_x, org_y+side) # Left
        display.line(org_x+side-1, org_y, org_x+side-1, org_y+side) # Right
    # Draw letter if needed
    if char:
        display.set_font(CELL_FONT)
        display.set_pen(text)
        display.text(
            char,
            org_x+int(CELL_SIDE/2)-1,
            org_y+int((CELL_SIDE-display.measure_text(char, CELL_FONT_SCALE))/2),
            scale=CELL_FONT_SCALE,
            angle=90,
        )

# Cell Style:
#     Empty cell: black outline, white fill
#     Correct cell: black outline, white fill, black letter
#     Yellow cell: black outline (?), grey fill, white letter
#     Wrong cell: black outline, black fill, white letter
#     Unsubmitted cell: black outline, white fill, black letter

def draw_grid():
    for y in range(6):
        for x in range(5):
            char = grid[y][x]
            if char == "":
                # Empty
                draw_cell(x, y, 0, 15, 0, char)
            elif char == WORD[x]:
                # Correct
                draw_cell(x, y, 0, 15, 0, char)
            elif char in WORD:
                # In word but wrong place
                draw_cell(x, y, 0, 9, 0, char)
            elif char not in WORD:
                draw_cell(x, y, 0, 0, 15, char)


### Main code ###
# You need to provide the appropriate value to the
# select_word function in order to solve the puzzle.
# (there are some functions available for your convenience).
WORD = select_word(_PLACEHOLDER_)

# Initial screen
display.set_update_speed(UPDATE_NORMAL)
display.set_pen(15)
display.clear()
display.set_pen(0)
display.set_font(HEADER_FONT)
display.text("CSE", WIDTH-20, HALF_H-31, scale=1.0, angle=90)
display.text("Wordle", WIDTH-50, HALF_H-51, scale=1.0, angle=90)
draw_grid()
display.update()

### Letter selection ###

# Position on grid
pos_x = 0
pos_y = 0

# Letters to be submitted
# Ex: ["C", "R", "A", "", ""]
row = [""] * 5
row_char_idx = [-1] * 5 # Index in LETTERS

display.set_update_speed(UPDATE_TURBO)

while True:
    if display.pressed(BUTTON_B):
        # Next letter
        row_char_idx[pos_x] = (row_char_idx[pos_x]+1) % LETTERS_SIZE
        row[pos_x] = LETTERS[row_char_idx[pos_x]]
    elif display.pressed(BUTTON_C):
        # Prev letter
        if row_char_idx[pos_x] == -1:
            # First time in the cell, set to Z
            # Otherwise (-1-1)%26 will set it to Y
            row_char_idx[pos_x] = LETTERS_SIZE - 1
        else:
            row_char_idx[pos_x] = (row_char_idx[pos_x]-1) % LETTERS_SIZE
        row[pos_x] = LETTERS[row_char_idx[pos_x]]
    elif display.pressed(BUTTON_A):
        # Submit row
        
        if row[pos_x] == "":
            # Row isn't finished
            sleep(0.2) # Debounce
            continue
        
        if not valid_word("".join(row)):
            sleep(0.2) # Debounce
            continue
        
        # Submit to grid
        grid[pos_y] = row
        # Move to new row
        pos_y += 1
        pos_x = 0
        # Reset data for row
        row = [""] * 5
        row_char_idx = [-1] * 5
        # Draw grid
        display.set_update_speed(UPDATE_FAST)
        draw_grid()
        
        # Is the game over?
        if pos_y == 6 or "".join(grid[pos_y-1]) == WORD:
            pos_y -= 1 # Allow usage of pos_y in end game code
            break    
    elif display.pressed(BUTTON_UP):
        # Delete letter
        # Erase current letter
        draw_cell(pos_x, pos_y, 0, 15, 0, "")
        # Reset data for current letter
        row[pos_x] = ""
        row_char_idx[pos_x] = -1
        # Update position
        pos_x = max(0, pos_x-1)
        display.set_update_speed(UPDATE_FAST) # Better update
    elif display.pressed(BUTTON_DOWN) and row[pos_x] != "":
        # Next letter
        pos_x = min(pos_x+1, 4)
        display.set_update_speed(UPDATE_FAST) # Better update
    else:
        # No button pressed, so check buttons again without updating screen
        continue
    
    # A button was pressed, so draw
    draw_cell(pos_x, pos_y, 0, 15, 0, row[pos_x])
    display.update()
    display.set_update_speed(UPDATE_TURBO) # Reset update speed in case it was changed


# End game screen

display.set_pen(0)
display.set_font(HEADER_FONT)

if "".join(grid[pos_y]) == WORD:
    # Won
    display.text("You won!", 30, HALF_H-55, angle=90, scale=0.8)
    sleep(3)
else:
    # Lost
    display.text(WORD, 30, int(HALF_H-display.measure_text(WORD)/2), angle=90)

display.update()

