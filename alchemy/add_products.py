from __main__ import session
from initialize_db import Product
from common_functions import *

def edit_write_buffer(inputArtNum):
	writeBuffer = []
	writeBuffer.append(inputArtNum)
	writeBuffer.append(raw_input("\nArtikel Name:		"))
	try:
		writeBuffer.append(int(raw_input("Flaschen pro Einheit:	")))
	except TypeError:
		print("Bitte nur ganze Zahlen eingeben!")
	
	try:
		writeBuffer.append(int(raw_input("Kasten pro Einheit:	")))
	except TypeError:
		print("Bitte nur ganze Zahlen eingeben!")
	
	try:
		writeBuffer.append(float(raw_input("Flaschenpfand:		")))
	except TypeError:
		print("Bitte nur Dezimalzahlen eingeben!")
	
	return writeBuffer

def create_new_product(inputArtNum):
	writeBuffer = edit_write_buffer(inputArtNum)
	if yes_no(
		"Bitte ueberpruefen Sie ihre Angaben. Bestaetigen?",
		"Angaben akzeptiert, werden am Schluss in der Datenbank gespeichert.",
		"Angaben verworfen!\n\n"
		) is True:
		session.add(
			Product(
				artNum = writeBuffer.pop(0),
				name = writeBuffer.pop(0),
				bottlesPerUnit = writeBuffer.pop(0),
				cratesPerUnit = writeBuffer.pop(0),
				bottlePfand = writeBuffer.pop(0),
			)
		)
	else:
		pass

def edit_existing(inputArtNum):
	existingProduct = session.query(Product).filter(Product.artNum == inputArtNum).first()
	print(existingProduct)
	print("")
	# is there a better way to retain existing values?
	print("Achtung: Alle Eingaben muessen neu ausgefuellt werden\n")
	writeBuffer = edit_write_buffer(inputArtNum)
	del writeBuffer[0]    # remove artNum, we don't want to CHANGE that ever, right?
	
	if yes_no(
		"Bitte ueberpruefen Sie ihre Angaben. Bestaetigen?",
		"Angaben akzeptiert, werden am Schluss in der Datenbank gespeichert.",
		"Angaben verworfen!\n\n"
		) is True:
		existingProduct.name = writeBuffer.pop(0)
		existingProduct.bottlesPerUnit = writeBuffer.pop(0)
		existingProduct.cratesPerUnit = writeBuffer.pop(0)
		existingProduct.bottlePfand = writeBuffer.pop(0)
	else:
		pass

def add_products():
	while yes_no("Neues Product eingeben?") is True:
		while True:
			try:
				inputArtNum = int(raw_input("Artikelnummer:		"))
				break
			except TypeError:
				print("Bitte nur Ziffern eingeben!")
		
		if check_exists(inputArtNum) is False:    # if unique
			create_new_product(inputArtNum)
		elif yes_no("Artikel existiert schon in der Datenbank! Moechten Sie die Daten aendern?") is True:
			edit_existing(inputArtNum)
		else:
			continue

def write_products():
	add_products()
	session.commit()
