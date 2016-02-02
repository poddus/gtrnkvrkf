from __main__ import session
from initialize_db import Product

def check_exists(input):
	for instance in session.query(Product.artNum):
		if instance.artNum == input:
			return True
	return False

def yes_no(question, yes="", no=""):
	while True:
		print("")
		print(question + " j/n:")
		choice = raw_input(">")
		if choice == "j":
			if yes != "":
				print(yes)
			return True
		elif choice == "n":
			if no != "":
				print(no)
			return False
		else:
			print("Bitte entweder 'j' oder 'n' eingeben")
			continue