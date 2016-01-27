# https://pysqlite.readthedocs.org/en/latest/sqlite3.html

from __future__ import division, print_function
from tabulate import tabulate

'''preisliste------------------------------------------------------------------------------------'''

class drink:
	"""
	Common base class for all drinks.
	A 'unit' is the smallest deliverable unit.
	'cost' is what we pay.
	'price' is what the customer pays.
	"""
	
	def __init__(
		self,
		name,
		artNum,
		bottlesPerUnit,
		cratesPerUnit,
		unitCost, # pro Liefereinheit, also praktisch pro Kasten
		bottlePfand
	):
		
		self.name = name
		self.artNum = artNum
		self.bottlesPerUnit = bottlesPerUnit
		self.cratesPerUnit = cratesPerUnit
		self.unitCost = unitCost
		self.bottlePfand = bottlePfand
	
	
	def get_cost_MwSt(self):
		return self.unitCost*1.19
	
	def get_bottle_price(self):
		return round(((self.get_cost_MwSt() / self.bottlesPerUnit) + 0.1), 2)
		
# 	def get_crate_price(self):
# 		return round((self.get_bottle_price() * self.bottlesPerUnit), 1)
		
a1072 = drink(
	"Augustiner Hell",
	1072,
	20,
	1,
	10.972,
	0.08)

a1602 = drink(
	"Karamalz",
	1602,
	20,
	1,
	8.506,
	0.08)

a1802 = drink(
	"Tegernseer Hell",
	1802,
	20,
	1,
	11.395,
	0.08)
	

inventory = { # amounts in unit of bottles
	a1072:20,
	a1602:40,
	a1802:60}

# for users to make a selection, we need a dict to translate what they input into the object:
selectionDict = {}
for k in inventory:
	selectionDict[k.artNum] = k # the key is an integer!

'''-----------------------------------------------------------------------------------/preisliste'''
# from preisliste import *


def update_inventory(order):
	for k in order:
		inventory[k] -= order[k]

def get_order():
	order = {}
	
	# print inventory as tabulate table
	table = []
	for k in sorted(inventory):
		table.append([k.artNum, k.name, k.get_bottle_price(), inventory[k]])
	print(tabulate(table, headers=["Artikel#","Name", "Preis Flasche", "Bestand"]))
	
	selection = ""
	while True:
		print("\nGeben Sie eine Artikelnummer ein, oder schreiben Sie 'f' wie 'fertig':")
		# this exits the loop for any non-number input, not just for 'f'
		try:
			selection = int(raw_input("> "))
		except ValueError:
			print("")
			break
		
# 		if selection == "f" or selection == "fertig":
# 			print("")
# 			break
# 		selection = int(selection)
		
		try:
			# translate selection into object.
			selection = selectionDict[selection]
		except KeyError:
			print("ungueltige Auswahl!")
			continue
		
		amount = 0
		if inventory.get(selection) != 0:
			
			print("Artikel:	", selection.name)
			print("Preis:		", selection.get_bottle_price())
			print("Bestand:	", inventory.get(selection))
			print("\nWie viele Flaschen?:")
			
			while True:
				try:
					amount = int(raw_input("> "))
					break
				except ValueError:
					print("ungueltige Auswahl!")
			
			if amount == 0:
				print("Anzahl Null, Vorgang abgebrochen")
			elif amount > 0 and amount <= inventory[selection]:
				print("Menge zu diesem Artikel wurde gespeichert.")
				# previous value is overwritten if this runs again
				order[selection] = amount
			else:
				print("Mehr als Bestand im Inventar! Vorgang abgebrochen")
		
		else: print(selection, "haben wir leider nicht")
	
	# prune orders with value 0
# 	for k in order.keys():
# 		if order[k] == 0:
# 			del order[k]
# 		else:
# 			pass
	
	update_inventory(order)
	return order


def verkauf():
	
	order = get_order()
	
	if order == {}:
		print("Leere Bestellung, Vorgang abgebrochen")
	else:
		total = 0
		for k in sorted(order):
			print("Artikel:	", k.name)
			print("Preis:		", k.get_bottle_price())
			print("Bestellt:	", order[k], "\n")
			total += k.get_bottle_price() * order[k]
	
		print("Endsumme:	", total)
		
		while True:
			try:
				paid = float(raw_input("Bezahlt:	 "))
				if paid >= total:
					print("Rueckgeld:	", paid - total)
					break
				else:
					print("zu wenig...")
			except ValueError:
				print("ungueltige Auswahl!")
				continue

verkauf()