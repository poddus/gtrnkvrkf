from initialize_db import Product, StockTake, StockTakeDetail
from add_products import write_products
from config import *

from time import time

def edit_write_buffer(stocktake, currentProduct):
	writeBuffer = []
	
	writeBuffer.append(stocktake.stockTakeID)
	writeBuffer.append(currentProduct.artNum)
	
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
	
	# TODO: if possible, default value to last entry
	# 
	# lastStockTakeEntry = query for last entry of currentProduct in StockTakeDetail
	# lastStockTakeEntry.unitCost
	# lastStockTakeEntry.bottleSurcharge
	# if input is "", use previous values
	while True:
		try:
			writeBuffer.append(float(raw_input("Kosten pro Liefereinheit:	")))
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

def new_stocktake_detail(stocktake):
	while True:
		try:
			inputArtNum = int(raw_input("Artikelnummer:			"))
			break
		except:
			print "Bitte nur Ziffern eingeben!"
	
	if check_exists(inputArtNum) is True:
		currentProduct = session.query(Product).filter(Product.artNum == inputArtNum).first()
		writeBuffer, pfandcrates, pfandbottles = edit_write_buffer(stocktake, currentProduct)
		
		clear_screen()
		
		einheiten = writeBuffer[2] // currentProduct.bottlesPerUnit
		zusFlaschen = writeBuffer[2] % currentProduct.bottlesPerUnit
		
		table = []
		table.append(["Artikelnummer", writeBuffer[1]])
		table.append(["Anzahl Einheiten", einheiten])
		table.append(["Zusaetzlich Fl", zusFlaschen])
		table.append(["Preis pro Einheit", writeBuffer[3]])
		table.append(["Aufschlag pro Fl", writeBuffer[4]])
		
		print tabulate(table, numalign="left")
		if yes_no(
			"\nBitte ueberpruefen Sie ihre Angaben. Bestaetigen?",
			"Angaben akzeptiert, werden am Schluss in der Datenbank gespeichert.",
			"Angaben verworfen!"
			) is True:
			
			
			
			clear_screen()
			
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
		print "Bitte legen Sie Artikel immer zuerst an. Sie werden weitergeleitet"
		raw_input()
		clear_screen()
		
		write_products()    # imported from add_products
		clear_screen()
		print "Eingegebene Artikel sind gespeichert. Fahren Sie nun mit der Bestandsaufnahme weiter."
		pass

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
		new_stocktake_detail(stocktake)
	
	if yes_no("Ist zusaetzliches Leergut auch vorhanden?") is True:
		add_pfand(stocktake)

def take_stock():
	if yes_no("Neue Bestandsaufnahme eingeben?"):
		clear_screen()
		new_stocktake()
		session.commit()
		print "Bestandsaufnahme wurde in die Datenbank eingetragen"
		raw_input()