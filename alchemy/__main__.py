from config import *

from add_products import write_products
from stock_take import take_stock
from sale import sale

def what_do():	
	table = []
	table.append([0, "Programm schliessen"])
	table.append([1, "Verkauf"],)
	table.append([2, "Neue Lieferung / Inventar Pruefen"],)
	table.append([3, "Sortiment bearbeiten"],)
	table.append([4, "Hilfe"])
	
	while True:
		clear_screen()
		print "Was moechten Sie machen? Bitte eine der folgenden Nummern eingeben:"
		print tabulate(table)

		choice = None
		while choice == None:
			try:
				choice = int(raw_input("> "))
			except ValueError:
				print "Bitte nur Nummern eingeben!"

		if choice == 0:
			clear_screen()
			return 0
		elif choice == 1:
			clear_screen()
			sale()
		elif choice == 2:
			clear_screen()
			take_stock()
		elif choice == 3:
			clear_screen()
			write_products()
		elif choice == 4:
			# link help.py
			print "not implemented"
		else:
			print "not implemented"

what_do()