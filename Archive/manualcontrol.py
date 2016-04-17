import curses
from motor import moveBot, motorStop
from Servo import Servo

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0, 10, "Hit 'q' to quit")
stdscr.refresh()

# Set amount of time waiting for input
stdscr.timeout(100)

key = ''
while key != ord('q'):
    key = stdscr.getch()
    print key
    stdscr.addch(20, 25, key)
    stdscr.refresh()

    if key == -1:
        stdscr.addstr(2, 20, "Stop")
        motorStop()

    elif key == curses.KEY_UP:
        stdscr.addstr(2, 20, "Up")
        moveBot('forward', continuous_mode=True)

    elif key == curses.KEY_DOWN:
        stdscr.addstr(2, 20, "Down")
        moveBot('backward', continuous_mode=True)

    elif key == curses.KEY_LEFT:
        stdscr.addstr(2, 20, "Left")
        moveBot('turnleft', continuous_mode=True)

    elif key == curses.KEY_RIGHT:
        stdscr.addstr(2, 20, "Right")
        moveBot('turnright', continuous_mode=True)

    # elif key == ord('w'):
    #     stdscr.addstr(2, 20, "Camera_Up")
    #     moveCam('up')

    # elif key == ord('s'):
    #     stdscr.addstr(2, 20, "Camera_Down")
    #     moveCam('down')

    # elif key == ord('a'):
    #     stdscr.addstr(2, 20, "Camera_Left")
    #     moveCam('right')

    # elif key == ord('d'):
    #     stdscr.addstr(2, 20, "Camera_Right")
    #     moveCam('left')

curses.endwin()
