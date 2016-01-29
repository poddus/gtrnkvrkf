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
		print("Neues Product eingeben? j/n:")
		choice = raw_input(">")
		if choice == "n":
			return False
		elif choice == "j":
			return True
		else:
			print("Bitte entweder 'j' oder 'n' eingeben")
			continue

def check_uniqueness(input):
	for instance in session.query(Product.artNum):
		if instance.artNum == input:
			# implement editing of entries!
			print("Artikel existiert schon in der Datenbank! Bitte versuchen Sie es erneut.\n\n")
			return False
	return True

def choose_to_accept():
	while True:
		# print confirmation before adding to database
		print("Bitte ueberpruefen Sie ihre Angaben. Bestaetigen? j/n")
		choice = raw_input(">")
		if choice == "n":
			print("Angaben verworfen!\n\n")
			return False
		elif choice == "j":
			print("Angaben akzeptiert, werden am Schluss in der Datenbank gespeichert.")
			return True
		else:
			print("Bitte entweder 'j' oder 'n' eingeben")
			continue

def add_products():
	while choose_to_input() is True:
		writeBuffer = []
		# check for uniqueness of Article Number:
		# query database for input
		# if row exists, error
		# else continue
		inputArtNum = int(raw_input("Artikelnummer:		"))
		if check_uniqueness(inputArtNum) is True:
			writeBuffer.append(inputArtNum)
		else:
			continue

		writeBuffer.append(raw_input("Artikel Name:		"))
		writeBuffer.append(int(raw_input("Flaschen pro Einheit:	")))
		writeBuffer.append(int(raw_input("Kasten pro Einheit:	")))
		writeBuffer.append(float(raw_input("Flaschenpfand:		")))

		if choose_to_accept() is True:
			if writeBuffer == []:
				print("Keine Angaben gefunden. Es wurde nichts gemacht")
			else:
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
			continue

def write_products():
	add_products()
	session.commit()
