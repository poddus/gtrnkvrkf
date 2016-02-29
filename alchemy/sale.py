from config import *
from initialize_db import Product, Order, StockTake
from sqlalchemy import select

from time import time

def get_current_inventory(lastStockTake):
	inventory = {}
	
	if lastStockTake is not None:
		if lastStockTake.stocktakedetail is not None:
			for instance in lastStockTake.stocktakedetail:
				inventory[instance.artNum] = [
					instance.product.name,
					instance.quantity,
					None,    # placeholder for unit quantity
					instance.product.bottlesPerUnit,    # placeholder for bottle quantity
					instance.get_unit_price(),
					instance.get_bottle_price()
				]
	
		if lastStockTake.order is not None:
			for instance in lastStockTake.order:
				inventory[instance.artNum][1] -= instance.quantity
	
	table = []
	for key in inventory:
		# insert amounts into placeholders in inventory
		inventory[key][2] = inventory[key][1] // inventory[key][3]
		inventory[key][3] = inventory[key][1] % inventory[key][3]
		
		# convert to tabulate-able table
		table.append(
			[
				key,
				inventory[key][0],
				inventory[key][2],
				inventory[key][3],
				inventory[key][4],
				inventory[key][5]
			]
		)
	
	print tabulate(table, headers=["Artikel#", "Name", "Einheiten", "+Flaschen", "Preis/E", "Preis/Fl"])
	print
	return inventory

def check_available(inputArtNum, inventory):
	try:
		if inventory[inputArtNum][1] > 0:
			return True
		else:
			print "Produkt nicht vorhanden!"
			raw_input()
			return False
	except:
		print "Artikel existiert nicht!"
		raw_input()
		return False

def input_products(writeBuffer, total):
	lastStockTake = session.query(StockTake).order_by(StockTake.stockTakeID.desc()).first()
	
	while yes_no("Neues Product eingeben?") is True:
		clear_screen()
		inventory = get_current_inventory(lastStockTake)
		
		print "Waehlen Sie ein Produkt\n"
		while True:
			try:
				inputArtNum = int(raw_input("Artikelnummer:		"))
				currentProduct = session.query(Product).filter(Product.artNum == inputArtNum).first()
				break
			except:
				print "Bitte nur Ziffern eingeben!"
		
		# TODO: if article exists in writeBuffer, edit existing entry
		
		if check_available(inputArtNum, inventory) is False:
			clear_screen()
			continue
		else:
			pass
		
		# select quantities of product
		# TODO: Pfand!
		totalQuantity = 0
		while True:
			try:
				unitQuantity = int(raw_input("Anzahl der Liefereinheiten:	"))
				if unitQuantity * currentProduct.bottlesPerUnit > inventory[inputArtNum][1]:
					print "Nicht genug vorhanden!"
					continue
				else:
					totalQuantity += unitQuantity * currentProduct.bottlesPerUnit
					break
			except:
				print "Bitte nur ganze Zahlen eingeben!"
		
		while True:
			try:
				bottleQuantity = int(raw_input("Anzahl der Flaschen:	"))
				totalQuantity += bottleQuantity
				break
			except:
				print "Bitte nur ganze Zahlen eingeben!"
		
		
		writeBuffer[inputArtNum] = [unitQuantity, bottleQuantity, totalQuantity * inventory[inputArtNum][5]]
		
		# total price, bottles * bottle_price
		for i in writeBuffer:
			total += writeBuffer[i][2]
		
		# convert dict to tabulate-able table and print
		table = []
		for key in writeBuffer:
			table.append([key, writeBuffer[key][0], writeBuffer[key][1], writeBuffer[key][2]])
		
		clear_screen()
		print "Vorgang:"
		print
		print tabulate(table, headers=["Artikel#", "Einheiten", "+Flaschen", "Zwischensumme"])
		
		print
		print "Insgesamt: ", total
		raw_input()
		
	return writeBuffer, total

def sale():
	
	order = Order()
	order.timestamp = time()
	print "Notiz zu dieser Bestellung:"
	order.note = raw_input("> ")
	
	session.add(order)
	
	writeBuffer, total = input_products(writeBuffer = {}, total = 0)
	
	# once user no longer wishes to input Products, ask to finalize order
	if yes_no("Bestellung vollstaendig?") is False:
		print "Vorgang abgebrochen!"
		raw_input()
		pass
	else:
		# calculate change, and write writeBuffer to database
		print "Bargeld gegeben:"
		moneyGiven = None
		while moneyGiven == None:
			try:
				moneyGiven = float(raw_input("> "))
			except ValueError:
				print "Bitte nur Zahlen eingeben!"
		
		print "Rueckgeld:"
		print moneyGiven - total
		
		for product in writeBuffer:
			session.add(
				order.orderdetail(
					orderID = order.orderID,
					artNum = product,
					# TODO, placeholders:
					quantity = 0,
					pfandCrates = 0,
					pfandBottles = 0,
				)
			)

# show preisliste
#	query database for last StockTake where quantity > 0
#	print nice table of results (tabulate?)
#
# ask to add a new product to order
# select article using artNum
# 	? print info about article
# 
# select amount
#	print subtotal
#	? also total
#
# write selection to session
# session.add(Order...)
# 
# repeat until order is complete
# 
# Pfand zurueck?
# 	Anzahl der Kasten (float, because half-crates!)
# 	Anzahl der 0.08 Flaschen
# 	Anzahl der 0.15 Flaschen
# Pfand mitnehmen? (Flaschen sind schon verrechnet, hier NUR KASTEN)
# 
# write net Pfand to order
# 
# print order, give choice:
# 	acknowledge, continue to check out
# 	request change, return to point 3, but retain order information
# 		if changes are made, overwrite previous choice, else keep choices
# 
# check out
# calculate change
# 
# write transaction to database, update inventory
# return to beginning