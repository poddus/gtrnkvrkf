from config import *
from initialize_db import Product, Order, StockTake
from sqlalchemy import select

def get_current_inventory(lastStockTake):
	inventory = {}
	dict = {}
	
	if lastStockTake is not None:
		if lastStockTake.stocktakedetail is not None:
			for instance in lastStockTake.stocktakedetail:
				inventory[instance.artNum] = [instance.quantity, instance.get_bottle_price()]
				dict[instance.artNum] = [
					instance.product.name,
					None,    # placeholder for unit quantity
					instance.product.bottlesPerUnit,    # placeholder for bottle quantity
					instance.get_unit_price(),
					instance.get_bottle_price()
				]
	
		if lastStockTake.order is not None:
			for instance in lastStockTake.order:
				inventory[instance.artNum] -= instance.quantity
	
	table = []
	for key in dict:
		# insert amounts into placeholders in dict
		dict[key][1] = inventory[key][0] // dict[key][2]
		dict[key][2] = inventory[key][0] % dict[key][2]
		
		# convert to tabulate-able table
		table.append(
			[
				key,
				dict[key][0],
				dict[key][1],
				dict[key][2],
				dict[key][3],
				dict[key][4]
			]
		)
	
	print tabulate(table, headers=["Artikel#", "Name", "Einheiten", "+Flaschen", "Preis/E", "Preis/Fl"])
	print
	return inventory

def check_available(inputArtNum, inventory):
	try:
		if inventory[inputArtNum] > 0:
			return True
		else:
			return False
	except KeyError:
		"Artikel existiert nicht!"
		return False

def sale():
	lastStockTake = session.query(StockTake).order_by(StockTake.stockTakeID.desc()).first()
	
	order = []
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
		
		if check_available(inputArtNum, inventory) is False:
			print "Produkt nicht vorhanden!"
			raw_input()
			clear_screen()
			continue
		else:
			pass
		
		totalQuantity = 0
		while True:
			try:
				unitQuantity = int(raw_input("Anzahl der Liefereinheiten:	"))
				if unitQuantity * currentProduct.bottlesPerUnit > inventory[inputArtNum]:
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
		
		
		order.append([inputArtNum, unitQuantity, bottleQuantity, totalQuantity * inventory[inputArtNum][1]])
		
		clear_screen()
		print "Vorgang:"
		print
		print tabulate(order, headers=["Artikel#", "Einheiten", "+Flaschen", "Zwischensumme"])
		
		total = 0
		for i in order:
			total += i[3]
		
		print
		print "Insgesamt: ", total
		raw_input()

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