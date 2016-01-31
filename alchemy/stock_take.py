from sqlalchemy import create_engine
engine = create_engine('sqlite:///alchemy.db', echo=False)    # echo=True to show SQL statements

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from initialize_db import Product, Order, StockTake, StockTakeDetail
from add_products import write_products

from time import time

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


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
# Leergut zusätzlich noch da?
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

def choose_to_new_stocktake():
	while True:
		print("")
		print("Neues Bestandaufnahme eingeben? j/n:")
		choice = raw_input(">")
		if choice == "j":
			return True
		elif choice == "n":
			return False
		else:
			print("Bitte entweder 'j' oder 'n' eingeben")
			continue

def choose_to_new_detail():
	while True:
		print("")
		print("Warenbestand eingeben? j/n:")
		choice = raw_input(">")
		if choice == "j":
			return True
		elif choice == "n":
			return False
		else:
			print("Bitte entweder 'j' oder 'n' eingeben")
			continue

def check_exists(input):
	for instance in session.query(Product.artNum):
		if instance.artNum == input:
			return True
	return False

def edit_write_buffer(inputArtNum):
	writeBuffer = []
	# TODO: how to add most recent StockTakeID? foreign key
	writeBuffer.append(inputArtNum)
	try:
		quantity = int(raw_input("Anzahl der Liefereinheiten:	")))
		# TODO: convert to bottles
		try:
			quantity += int(raw_input("Zusaetzliche volle Flaschen:	")))
		except TypeError:
			print("Bitte nur ganze Zahlen eingeben!")
		
		writeBuffer.append(quantity)
	except TypeError:
		print("Bitte nur ganze Zahlen eingeben!")
	
	try:
		writeBuffer.append(float(raw_input("Preis pro Liefereinheit:	")))
	except TypeError:
		print("Bitte nur Dezimalzahlen eingeben!")
	
	try:
		writeBuffer.append(float(raw_input("Aufschlag pro Flasche:		")))
	except TypeError:
		print("Bitte nur Dezimalzahlen eingeben!")
	
	# TODO: fucking Pfand, man
	
	return writeBuffer

def choose_to_accept():
	while True:
		print("Bitte ueberpruefen Sie ihre Angaben. Bestaetigen? j/n")
		choice = raw_input(">")
		if choice == "j":
			print("Angaben akzeptiert, werden am Schluss in der Datenbank gespeichert.")
			return True
		elif choice == "n":
			print("Angaben verworfen!\n\n")
			return False
		else:
			print("Bitte entweder 'j' oder 'n' eingeben")
			continue

def new_stocktake_detail():
	writeBuffer = edit_write_buffer(inputArtNum)
	if choose_to_accept() is True:
		session.add(
			StockTakeDetail(
				StockTakeID = writeBuffer.pop(0),
				artNum = writeBuffer.pop(0),
				quantity = writeBuffer.pop(0),
				unitCost = writeBuffer.pop(0),
				bottleSurcharge = writeBuffer.pop(0),
				pfandCrates = writeBuffer.pop(0),
				pfandBottles = writeBuffer.pop(0)
			)
		)
	else:
		pass

def new_stocktake(inputArtNum):
	stocktake = StockTake()
	stocktake.timestamp = time()
	print("Notiz zu dieser Bestandaufnahme:")
	stocktake.note = raw_input("> ")
	
	session.add(stocktake)
	
	while choose_to_new_detail() is True:
		new_stocktake_detail()
	
	session.commit()

def choose_to_create():
	while True:
		print("Artikel existiert noch nicht in der Datenbank! Moechten Sie ein neues Produkt anlegen? j/n")
		choice = raw_input(">")
		if choice == "j":
			return True
		elif choice == "n":
			return False
		else:
			print("Bitte entweder 'j' oder 'n' eingeben")
			continue

def take_stock():
	while choose_to_new_stocktake() is True:
		inputArtNum = int(raw_input("Artikelnummer:		"))
		if check_exists(inputArtNum) is True:
			new_stocktake(inputArtNum)
		elif choose_to_create() is True:
			write_products()    # from import add_products
		else:
			continue