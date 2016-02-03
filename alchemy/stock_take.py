from initialize_db import Product, StockTake, StockTakeDetail
from add_products import write_products
from config import *

from time import time


# ask to input product to the stock take
# select article using artNum
# if product exists in tblProducts:
# 	print info about article
#	ask if info (example cost) has changed
#	if yes, edit_products (not yet implemented)
# else:
# 	ask to add product to database
# 	add_products.py
#
# select quantity (has to either be directly in bottles, or calculated
# from shipment units into bottles
#
# write selection to session
# session.add(StockTake...)
# 
# repeat until stock take is complete
# 
# Leergut zusaetzlich noch da?
# 	Anzahl der Kasten (float, because half-crates!)
# 	Anzahl der 0.08 Flaschen
# 	Anzahl der 0.15 Flaschen
# 
# write net Pfand to session
# 
# print articles and quantities, give choice:
# 	acknowledge, write transaction to database
# 	request change, return to input products, but retain order information
# 		if changes are made, overwrite previous choice, else keep choices

def edit_write_buffer(inputArtNum):
	writeBuffer = []
	currentProduct = session.query(Product).filter(Product.artNum == inputArtNum).one()
	
	# add most recent StockTakeID foreign key
	writeBuffer.append(session.query(StockTake).order_by(StockTake.stockTakeID.desc()).first())
	writeBuffer.append(inputArtNum)
	
	while True:
		try:
			quantity = int(raw_input("Anzahl der Liefereinheiten:	"))
			break
		except:
			print "Bitte nur ganze Zahlen eingeben!"
	
	# convert unit quantity to bottle quantity
	quantity *= currentProduct.bottlesPerUnit
	
	pfandcrates = quantity * currentProduct.cratesPerUnit
	
	while True:
		try:
			quantity += int(raw_input("Zusaetzliche volle Flaschen:	"))
			break
		except:
			print "Bitte nur ganze Zahlen eingeben!"
		
	if currentProduct.bottlePfand != 0:
		pfandbottles = quantity
	
	writeBuffer.append(quantity)
	
	while True:
		try:
			writeBuffer.append(float(raw_input("Preis pro Liefereinheit:	")))
			break
		except:
			print "Bitte nur Dezimalzahlen eingeben!"
	
	while True:
		try:
			writeBuffer.append(float(raw_input("Aufschlag pro Flasche:		")))
			break
		except:
			print "Bitte nur Dezimalzahlen eingeben!"
		
	return writeBuffer, pfandcrates, pfandbottles

def new_stocktake_detail():
	while True:
		try:
			inputArtNum = int(raw_input("Artikelnummer:			"))
			break
		except:
			print "Bitte nur Ziffern eingeben!"
	
	if check_exists(inputArtNum) is True:
		writeBuffer, pfandcrates, pfandbottles = edit_write_buffer(inputArtNum)
		
		clear_screen()
		
		currentProduct = session.query(Product).filter(Product.artNum == inputArtNum).first()
		einheiten = writeBuffer[2] // currentProduct.bottlesPerUnit
		zusFlaschen = writeBuffer[2] % currentProduct.bottlesPerUnit
		
		table = []
		table.append(["Artikelnummer", writeBuffer[1]])
		table.append(["Anzahl Einheiten", einheiten])
		table.append(["Zusaetzlich Fl", zusFlaschen])
		table.append(["Preis pro Einheit", writeBuffer[3]])
		table.append(["Aufschlag pro Fl", writeBuffer[4]])
		
		print tabulate(table, numalign="center")
		if yes_no(
			"\nBitte ueberpruefen Sie ihre Angaben. Bestaetigen?",
			"Angaben akzeptiert, werden am Schluss in der Datenbank gespeichert.",
			"Angaben verworfen!"
			) is True:
			
			raw_input()
			clear_screen()
			
			# TODO: Pfand tracking is not figured out yet
			session.add(
				StockTakeDetail(
					stockTakeID = writeBuffer.pop(0),
					artNum = writeBuffer.pop(0),
					quantity = writeBuffer.pop(0),
					unitCost = writeBuffer.pop(0),
					bottleSurcharge = writeBuffer.pop(0),
					pfandCrates = pfandcrates,
					pfandBottles = pfandbottles
				)
			)
	else:
		print "Artikel existiert noch nicht in der Datenbank!"
		raw_input()
		clear_screen()
		
		write_products()    # imported from add_products
		pass

def extra_pfand():
	if yes_no("Ist zusaetzliches Leergut auch vorhanden?") is True:
		# TODO: I'm creating entries with NULL values, how will I deal with that later on?
		while True:
			try:
				pfandcrates = float(raw_input("Wie viele Kasten?		"))
				session.add(
					StockTakeDetail(
						stockTakeID = session.query(StockTake).order_by(StockTake.stockTakeID.desc()).first(),
						artNum = 10000,
						pfandCrates = pfandcrates
					)
				)
				break
			except:
				print "Bitte nur Ziffern eingeben!"
		
		while True:
			try:
				bottles008 = int(raw_input("Wie viele 0.08 Flaschen:	"))
				session.add(
					StockTakeDetail(
						stockTakeID = session.query(StockTake).order_by(StockTake.stockTakeID.desc()).first(),
						artNum = 10001,
						pfandBottles008 = bottles008
					)
				)
				break
			except:
				print "Bitte nur Ziffern eingeben!"
		
		while True:
			try:
				bottles015 = int(raw_input("Wie viele 0.15 Flaschen:	"))
				session.add(
					StockTakeDetail(
						stockTakeID = session.query(StockTake).order_by(StockTake.stockTakeID.desc()).first(),
						artNum = 10002,
						pfandBottles015 = bottles015
					)
				)
				break
			except:
				print "Bitte nur Ziffern eingeben!"

def new_stocktake():
	stocktake = StockTake()
	stocktake.timestamp = time()
	print "Neue Bestandsaufnahme"
	print "Notiz zu dieser Bestandaufnahme:"
	stocktake.note = raw_input("> ")
	
	session.add(stocktake)
	
	clear_screen()
	print "Geben Sie den Bestand jedes Produktes nacheinander ein."
	while yes_no("Moechten Sie den Warenbestand eines Produktes eingeben?") is True:
		new_stocktake_detail()
	
	extra_pfand()

def take_stock():
	if yes_no("Neue Bestandsaufnahme eingeben?"):
		clear_screen()
		new_stocktake()
		session.commit()