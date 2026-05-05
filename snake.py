import curses
import random
import time
 
def main(stdscr):
    # Setup
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Food
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Score
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Border
 
    sh, sw = stdscr.getmaxyx()
    if sh < 20 or sw < 40:
        stdscr.addstr(0, 0, "Terminal too small! Need at least 40x20.")
        stdscr.getch()
        return
 
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(True)
    win.timeout(100)
 
    # Initial snake
    mid_y, mid_x = sh // 2, sw // 2
    snake = [[mid_y, mid_x], [mid_y, mid_x - 1], [mid_y, mid_x - 2]]
    direction = curses.KEY_RIGHT
    score = 0
    high_score = 0
 
    def place_food():
        while True:
            y = random.randint(2, sh - 2)
            x = random.randint(2, sw - 2)
            if [y, x] not in snake:
                return [y, x]
 
    food = place_food()
 
    def draw_border():
        win.attron(curses.color_pair(4))
        win.border()
        win.attroff(curses.color_pair(4))
 
    def draw_ui():
        win.attron(curses.color_pair(3))
        win.addstr(0, 2, f" 🐍 Snake  Score: {score}  High: {high_score}  [Q]uit ")
        win.attroff(curses.color_pair(3))
 
    while True:
        win.clear()
        draw_border()
        draw_ui()
 
        # Draw food
        win.attron(curses.color_pair(2))
        win.addch(food[0], food[1], "●")
        win.attroff(curses.color_pair(2))
 
        # Draw snake
        for i, seg in enumerate(snake):
            win.attron(curses.color_pair(1))
            win.addch(seg[0], seg[1], "█" if i == 0 else "▓")
            win.attroff(curses.color_pair(1))
 
        win.refresh()
 
        key = win.getch()
        if key in (ord("q"), ord("Q")):
            break
 
        # Update direction
        opposites = {curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP,
                     curses.KEY_LEFT: curses.KEY_RIGHT, curses.KEY_RIGHT: curses.KEY_LEFT}
        key_map = {ord("w"): curses.KEY_UP, ord("s"): curses.KEY_DOWN,
                   ord("a"): curses.KEY_LEFT, ord("d"): curses.KEY_RIGHT}
        key = key_map.get(key, key)
 
        if key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
            if key != opposites.get(direction):
                direction = key
 
        # Move head
        head = snake[0].copy()
        if direction == curses.KEY_UP:    head[0] -= 1
        elif direction == curses.KEY_DOWN: head[0] += 1
        elif direction == curses.KEY_LEFT: head[1] -= 1
        elif direction == curses.KEY_RIGHT: head[1] += 1
 
        # Collision check
        if (head[0] <= 0 or head[0] >= sh - 1 or
            head[1] <= 0 or head[1] >= sw - 1 or
            head in snake):
            # Game over
            high_score = max(high_score, score)
            win.addstr(sh // 2, sw // 2 - 10, f"  GAME OVER BYE! Score: {score}  ")
            win.addstr(sh // 2 + 1, sw // 2 - 10, "  Press R to restart or Q to quit  ")
            win.refresh()
            while True:
                k = win.getch()
                if k in (ord("r"), ord("R")):
                    snake = [[mid_y, mid_x], [mid_y, mid_x - 1], [mid_y, mid_x - 2]]
                    direction = curses.KEY_RIGHT
                    food = place_food()
                    score = 0
                    break
                elif k in (ord("q"), ord("Q")):
                    return
            continue
 
        snake.insert(0, head)
        if head == food:
            score += 10
            food = place_food()
        else:
            snake.pop()
 
if __name__ == "__main__":
    print("Starting Snake Game... (Press Q to quit)")
    time.sleep(0.5)
    curses.wrapper(main)
    print("Thanks for playing!")