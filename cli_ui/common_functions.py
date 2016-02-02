from initialize_db import Product

def check_exists(input):
	for instance in session.query(Product.artNum):
		if instance.artNum == input:
			return True
	return False

def yes_no(question, yes="", no=""):
	while True:
		screen.addstr(question + " j/n:")
		choice = screen.getkey()
		if choice == "j":
			if yes != "":
				screen.addstr("\n" + yes)
			return True
		elif choice == "n":
			if no != "":
				screen.addstr("\n" + no)
			return False
		else:
			screen.addstr("\n" + "Bitte entweder 'j' oder 'n' eingeben\n")
			continue