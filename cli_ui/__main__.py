import config

from add_products import write_products

def what_do(stdscr):
	# Frame the interface area at fixed VT100 size
	global screen
	screen = stdscr.subwin(40, 100, 0, 0)
	
	while True:
		screen.refresh()

		table = []
		screen.addstr("Was moechten Sie machen? Bitte eine der folgenden Nummern eingeben:\n")
		table.append([0, "Programm schliessen"])
		table.append([1, "Verkauf"],)
		table.append([2, "Neue Lieferung / Inventar Pruefen"],)
		table.append([3, "Sortiment bearbeiten"],)
		table.append([4, "Hilfe"])
	
		screen.addstr(2,0, tabulate(table))

		screen.refresh()

		choice = int(screen.getkey(10,0))
		screen.clear()

		if choice == 0:
			return 0
		elif choice == 1:
			print("not implemented")
		elif choice == 2:
			print("not implemented")
		elif choice == 3:
			write_products()
		elif choice == 4:
			print("not implemented")
		else:
			print("not implemented")

try:
	# Initialize curses
	stdscr=curses.initscr()
	# Turn off echoing of keys, and enter cbreak mode,
	# where no buffering is performed on keyboard input
	curses.noecho()
	curses.cbreak()

	# In keypad mode, escape sequences for special keys
	# (like the cursor keys) will be interpreted and
	# a special value like curses.KEY_LEFT will be returned
	stdscr.keypad(1)
	
	what_do(stdscr)    # Enter the main loop
	
	# Set everything back to normal
	stdscr.keypad(0)
	curses.echo()
	curses.nocbreak()
	curses.endwin()    # Terminate curses
	
except:
	# In event of error, restore terminal to sane state.
	stdscr.keypad(0)
	curses.echo()
	curses.nocbreak()
	curses.endwin()
	traceback.print_exc()           # Print the exception
	