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

# this same function is defined in add_products
def yes_no(question, yes="", no=""):
	while True:
		print("")
		print(question + " j/n:")
		choice = raw_input(">")
		if choice == "j":
			if yes != "":
				print(yes)
			return True
		elif choice == "n":
			if no != "":
				print(no)
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
	currentProduct = session.query(Product).filter(Product.artNum == inputArtNum).one()
	
	# add most recent StockTakeID foreign key
	writeBuffer.append(session.query(StockTake).order_by(StockTake.StockTakeID.desc()).first())
	writeBuffer.append(inputArtNum)
	
	while True:
		try:
			quantity = int(raw_input("Anzahl der Liefereinheiten:	")))
		except TypeError:
			print("Bitte nur ganze Zahlen eingeben!")
	
	# convert unit quantity to bottle quantity
	quantity *= currentProduct.bottlesPerUnit
	
	pfandcrates = quantity * currentProduct.cratesPerUnit
	
	while True:
		try:
			quantity += int(raw_input("Zusaetzliche volle Flaschen:	")))
		except TypeError:
			print("Bitte nur ganze Zahlen eingeben!")
		
		if currentProduct.bottlePfand != 0:
			pfandbottles = quantity
		
			writeBuffer.append(quantity)
	
	while True:
		try:
			writeBuffer.append(float(raw_input("Preis pro Liefereinheit:	")))
		except TypeError:
			print("Bitte nur Dezimalzahlen eingeben!")
	
	while True:
		try:
			writeBuffer.append(float(raw_input("Aufschlag pro Flasche:		")))
		except TypeError:
			print("Bitte nur Dezimalzahlen eingeben!")
		
	return writeBuffer, pfandcrates, pfandbottles

def new_stocktake_detail():
	while True:
		try:
			inputArtNum = int(raw_input("Artikelnummer:		"))
		except TypeError:
			print("Bitte nur Ziffern eingeben!")
	
	writeBuffer, pfandcrates, pfandbottles = edit_write_buffer(inputArtNum)
	if yes_no(
		"Bitte ueberpruefen Sie ihre Angaben. Bestaetigen?",
		"Angaben akzeptiert, werden am Schluss in der Datenbank gespeichert.",
		"Angaben verworfen!\n\n"
		) is True:
		session.add(
			StockTakeDetail(
				StockTakeID = writeBuffer.pop(0),
				artNum = writeBuffer.pop(0),
				quantity = writeBuffer.pop(0),
				unitCost = writeBuffer.pop(0),
				bottleSurcharge = writeBuffer.pop(0),
				pfandCrates = pfandcrates,
				pfandbottles = pfandbottles
			)
		)
	else:
		pass

def extra_pfand():
	if yes_no("Ist zusaetzliches Leergut auch vorhanden?") is True:
		# TODO
		# Anzahl der Kasten (float, because half-crates!)
		# Anzahl der 0.08 Flaschen
		# Anzahl der 0.15 Flaschen
	print("Wie viele Kasten?")
	while True:
		try:
			pfandcrates = int(raw_input("> "))
		except TypeError:
			print("Bitte nur Ziffern eingeben!")
	
	while True:
		# TODO: fudge nugget, I've coded myself into a pickle.
		# see issue #12 on github
		
		# I am creating entries with emtpy values. how will I deal with this? pandas?
		session.add(
			StockTakeDetail(
				pfandCrates = pfandcrates,
				pfandBottles = pfandbottles
			)
		)
		pass

def new_stocktake(inputArtNum):
	stocktake = StockTake()
	stocktake.timestamp = time()
	print("Notiz zu dieser Bestandaufnahme:")
	stocktake.note = raw_input("> ")
	
	session.add(stocktake)
	
	while yes_no("Möchten Sie den warenbestand eines Produktes eingeben?") is True:
		new_stocktake_detail()
	
	extra_pfand()
	
	session.commit()

def take_stock():
	while yes_no("Neue Bestandaufnahme eingeben?") is True:
		inputArtNum = int(raw_input("Artikelnummer:		"))
		if check_exists(inputArtNum) is True:
			new_stocktake(inputArtNum)
		elif yes_no("Artikel existiert noch nicht in der Datenbank! Moechten Sie ein neues Produkt anlegen?") is True:
			write_products()    # from import add_products
		else:
			continue