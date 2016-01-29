from __future__ import print_function, division
from tabulate import tabulate

from initialize_db import Product, Order, StockTake    # not importing "Detail" classes, necessary?
from add_products import write_products

def what_do():
	print("Was moechten Sie machen? Bitte eine der folgenden Nummern eingeben:\n")
	print("0	Abbrechen")
	print("1	Um neue Produkte zum Sortiment hinzuzufuegen")
	print("2	not implemented")
	print("3	not implemented")
	print("")

	choice = None
	while choice == None:
		try:
			choice = int(raw_input("> "))
		except ValueError:
			print("Bitte nur Nummern eingeben!")

	if choice == 0:
		return 0
	elif choice == 1:
		write_products()
	else:
		print("not implemented")

what_do()