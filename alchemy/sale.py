from config import *
from initialize_db import Product, Order, OrderDetail, StockTake, crate, bottle008, bottle015
from sqlalchemy import select

from time import time
import pdb


def get_current_inventory(lastStockTake):
	inventory = {}
	
	if lastStockTake is not None:
		if lastStockTake.stocktakedetail is not None:
			for product in lastStockTake.stocktakedetail:
				inventory[product.artNum] = [
					product.product.name,
					product.quantity,
					None,    # placeholder for unit quantity
					product.product.bottlesPerUnit,    # placeholder for bottle quantity
					product.get_unit_price(),
					product.get_bottle_price()
				]

		if lastStockTake.order is not None:
			for order in lastStockTake.order:
				for detail in order.orderdetail:
					inventory[detail.artNum][1] -= detail.quantity
		else:
			print "no orders since last stock take"
			raw_input()
	
	table = []
	for product in inventory:
		# insert unit & bottle quantities into placeholders in inventory
		inventory[product][2] = inventory[product][1] // inventory[product][3]
		inventory[product][3] = inventory[product][1] % inventory[product][3]
		
		# convert to tabulate-able table
		table.append(
			[
				product,
				inventory[product][0],
				inventory[product][2],
				inventory[product][3],
				inventory[product][4],
				inventory[product][5]
			]
		)
	
	print tabulate(table, headers=["Artikel#", "Name", "Einheiten", "+Flaschen", "Preis/E", "Preis/Fl"])
	print
	return inventory

def check_availability(artNum, inventory):
	try:
		if inventory[artNum][1] > 0:
			return True
		else:
			return False
	except:
		print "Artikel existiert nicht!"
		raw_input()
		return False

def select_quantity(currentProduct, inventory):
	totalQuantity = 0    # in bottles
	
	while True:
		try:
			unitQuantity = int(raw_input("Anzahl der Liefereinheiten:	"))
			if unitQuantity * currentProduct.bottlesPerUnit > inventory[currentProduct.artNum][1]:
				print "Nicht genug vorhanden!"
				continue
			else:
				totalQuantity += unitQuantity * currentProduct.bottlesPerUnit
				pfandCrates = unitQuantity * currentProduct.cratesPerUnit
				break
		except:
			print "bitte nur ganze Zahlen eingeben"
	
	while True:
		try:
			bottleQuantity = int(raw_input("Anzahl der Flaschen:	"))
			if totalQuantity + bottleQuantity > inventory[currentProduct.artNum][1]:
				print "Nicht genug vorhanden!"
				continue
			else:
				totalQuantity += bottleQuantity
				break
		except:
			print "bitte nur ganze Zahlen eingeben"
	
	return totalQuantity, totalQuantity, pfandCrates

def determine_pfand(currentProduct):
	if currentProduct.bottlePfand == 0.08:
		return bottle008.artNum
	elif currentProduct.bottlePfand == 0.15:
		return bottle015.artNum

def sale():
	order = Order()
	order.timestamp = time()
	print "Notiz zu diesem Vorgang:"
	order.note = raw_input("> ")
	
	session.add(order)
	
	lastStockTake = session.query(StockTake).order_by(StockTake.stockTakeID.desc()).first()
	totalCost = 0
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
		
		if check_availability(currentProduct.artNum, inventory) is False:
			print "Produkt nicht vorhanden."
			raw_input()
			clear_screen()
			break
		else:
			pass
		
		productDetail = OrderDetail()
		bottlePfandDetail = OrderDetail()
		cratePfandDetail = OrderDetail()
		
		productDetail.orderID = order.orderID
		productDetail.artNum = currentProduct.artNum
		
		bottlePfandDetail.artNum = determine_pfand(currentProduct)
		
		productDetail.quantity, bottlePfandDetail.quantity, cratePfandDetail.quantity = select_quantity(currentProduct, inventory)
		
		session.add(productDetail)
		session.add(bottlePfandDetail)
		session.add(cratePfandDetail)
		
		totalCost += inventory[currentProduct.artNum][5] * productDetail.quantity
		
		# add Pfand cost (bottles and crates) to totalCost
		totalCost += bottlePfandDetail.quantity * currentProduct.bottlePfand
		totalCost += cratePfandDetail.quantity * currentProduct.cratesPerUnit * 1.5
		
		table = []
		table.append(
			[
				inventory[currentProduct.artNum][0],
				productDetail.quantity // currentProduct.bottlesPerUnit,
				productDetail.quantity % currentProduct.bottlesPerUnit,
				inventory[currentProduct.artNum][1] * inventory[currentProduct.artNum][5],
			]
		)
		
		print tabulate(table, headers=["Name", "Einheiten", "Flaschen", "Zwischensumme"])
		print
		print "Summe: ", totalCost