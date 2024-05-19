import random
import curses

def initialize_board():
    board = [[0]*4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_tiles = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = 2 if random.random() < 0.9 else 4

def slide_row_left(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (4 - len(new_row))
    for i in range(3):
        if new_row[i] == new_row[i+1] and new_row[i] != 0:
            new_row[i] *= 2
            new_row[i+1] = 0
    new_row = [i for i in new_row if i != 0]
    new_row += [0] * (4 - len(new_row))
    return new_row

def move_left(board):
    return [slide_row_left(row) for row in board]

def rotate_board(board):
    return [list(row) for row in zip(*board[::-1])]

def move_right(board):
    rotated_board = rotate_board(rotate_board(board))
    moved_board = move_left(rotated_board)
    return rotate_board(rotate_board(moved_board))

def move_up(board):
    rotated_board = rotate_board(rotate_board(rotate_board(board)))
    moved_board = move_left(rotated_board)
    return rotate_board(moved_board)

def move_down(board):
    rotated_board = rotate_board(board)
    moved_board = move_left(rotated_board)
    return rotate_board(rotate_board(rotate_board(moved_board)))

def can_move(board):
    for row in board:
        if 0 in row:
            return True
    for row in board + rotate_board(board):
        for i in range(3):
            if row[i] == row[i+1]:
                return True
    return False

def draw_board(stdscr, board, score):
    stdscr.clear()
    stdscr.addstr("Score: " + str(score) + "\n")
    for row in board:
        stdscr.addstr("+----" * 4 + "+\n")
        stdscr.addstr("".join(f"|{str(num).center(4) if num != 0 else '    '}" for num in row) + "|\n")
    stdscr.addstr("+----" * 4 + "+\n")
    stdscr.refresh()

def game_loop(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    board = initialize_board()
    score = 0

    while True:
        draw_board(stdscr, board, score)
        move = stdscr.getch()
        if move == curses.KEY_LEFT:
            new_board = move_left(board)
        elif move == curses.KEY_RIGHT:
            new_board = move_right(board)
        elif move == curses.KEY_UP:
            new_board = move_up(board)
        elif move == curses.KEY_DOWN:
            new_board = move_down(board)
        else:
            continue

        if new_board != board:
            board = new_board
            add_new_tile(board)
            score += sum(sum(row) for row in board)

        if not can_move(board):
            draw_board(stdscr, board, score)
            stdscr.addstr("Game Over!\n")
            stdscr.refresh()
            stdscr.getch()
            break

if __name__ == "__main__":
    curses.wrapper(game_loop)
