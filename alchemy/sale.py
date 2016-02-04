from config import *
from initialize_db import Product, Order, StockTake

def get_current_inventory():
	# TODO: from lastStockTake, subtract from quantity all associated Orders, return
	pass

def tbl_of_products(lastStockTake, inventory):
	# TODO: inventory not yet implemented
	table = []
	for entry in lastStockTake.stocktakedetail:
		# TODO: only add if available quantity in current inventory > 0
		inventoryEntry = session.query(inventory).filter(artNum == entry.artNum).first()
		
		table.append(
			[
				entry.artNum,
				entry.product.name,
				inventoryEntry.quantity // entry.product.bottlesPerUnit,
				inventoryEntry.quantity % entry.product.bottlesPerUnit
				entry.get_unit_price()
				entry.get_bottle_price()
			]
		)
	
	return tabulate(table, headers="Artikel#", "Name", "Einheiten", "+Flaschen", "Preis/E", "Preis/Fl")

def sale():
	lastStockTake = session.query(StockTake).order_by(StockTake.stockTakeID.desc()).first()
	inventory = get_current_inventory()
	
	print tbl_of_products(lastStockTake, inventory)




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