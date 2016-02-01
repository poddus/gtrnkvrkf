from __future__ import print_function, division
from tabulate import tabulate

from sqlalchemy import create_engine
engine = create_engine('sqlite:///alchemy.db', echo=False)    # echo=True to show SQL statements

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

from common_functions import *
from initialize_db import *

from add_products import write_products
from stock_take import take_stock

def what_do():
	while True:
		print("Was moechten Sie machen? Bitte eine der folgenden Nummern eingeben:")
		print("0	Programm schließen")
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
			take_stock()
		elif choice == 3:
			write_products()
		elif choice == 4:
			# link help.py
			print("not implemented")
		else:
			print("not implemented")

what_do()