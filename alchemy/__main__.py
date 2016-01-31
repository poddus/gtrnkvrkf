from __future__ import print_function, division
from tabulate import tabulate

from initialize_db import Product, Order, StockTake    # not importing "Detail" classes, necessary?
from add_products import write_products

def what_do():
	print("Was moechten Sie machen? Bitte eine der folgenden Nummern eingeben:\n")
	print("0	Abbrechen")
	print("1	Verkauf")
	print("2	Neue Lieferung / Inventar Pruefen")
	print("3	Sortiment bearbeiten")
	print("4	Hilfe")

	choice = None
	while choice == None:
		try:
			choice = int(raw_input("> "))
		except ValueError:
			print("Bitte nur Nummern eingeben!")

	if choice == 0:
		return 0
	elif choice == 1:
		# link sale.py
		print("not implemented")
	elif choice == 2:
		# link stock_take.py
		print("not implemented")
	elif choice == 3:
		write_products()
	elif choice == 4:
		# link help.py
		print("not implemented")
	else:
		print("not implemented")

what_do()