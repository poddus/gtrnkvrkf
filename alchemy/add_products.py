from sqlalchemy import create_engine
engine = create_engine('sqlite:///alchemy.db', echo=False)    # echo=True to show SQL statements

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from initialize_db import Product

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

def choose_to_input():
	while True:
		print("")
		print("Neues Product eingeben? j/n:")
		choice = raw_input(">")
		if choice == "j":
			return True
		elif choice == "n":
			return False
		else:
			print("Bitte entweder 'j' oder 'n' eingeben")
			continue

def check_uniqueness(input):
	for instance in session.query(Product.artNum):
		if instance.artNum == input:
			return False
	return True

def choose_to_accept():
	while True:
		# print confirmation before adding to database
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

def choose_to_edit_existing():
	while True:
		print("Artikel existiert schon in der Datenbank! Moechten Sie die Daten aendern? j/n")
		choice = raw_input(">")
		if choice == "j":
			return True
		elif choice == "n":
			return False
		else:
			print("Bitte entweder 'j' oder 'n' eingeben")
			continue

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
	writeBuffer = []
	writeBuffer = edit_write_buffer(inputArtNum)
	if choose_to_accept() is True:
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
	print("Achtung: Alle Eingaben muessen neu ausgefuellt werden\n")
	writeBuffer = edit_write_buffer(inputArtNum)
	del writeBuffer[0]    # remove artNum, we don't want to CHANGE that ever, right?
	
	if choose_to_accept() is True:
		existingProduct.name = writeBuffer.pop(0)
		existingProduct.bottlesPerUnit = writeBuffer.pop(0)
		existingProduct.cratesPerUnit = writeBuffer.pop(0)
		existingProduct.bottlePfand = writeBuffer.pop(0)
	else:
		pass

def add_products():
	while choose_to_input() is True:
		
		inputArtNum = int(raw_input("Artikelnummer:		"))
		if check_uniqueness(inputArtNum) is True:
			create_new_product(inputArtNum)
		elif choose_to_edit_existing() is True:
			edit_existing(inputArtNum)
		else:
			continue

def write_products():
	add_products()
	session.commit()
