from __future__ import print_function, division
from tabulate import tabulate

from sqlalchemy import create_engine
engine = create_engine('sqlite:///alchemy.db', echo=False) # echo=True to show SQL statements

# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, Float, String, DateTime
class drink(Base):
	"""
	Common base class for all drinks.
	A 'unit' is the smallest deliverable unit.
	'cost' is what we pay.
	'price' is what the customer pays.
	"""
	
	__tablename__ = "tblProducts"
	
	artNum = Column(Integer, primary_key=True)
	name = Column(String(32))
	bottlesPerUnit = Column(Integer)
	cratesPerUnit = Column(Integer)
	bottlePfand = Column(Float)
	unitCost = Column(Float) # pro Liefereinheit, also praktisch pro Kasten
	bottleSurcharge = Column(Float)
	
	def __repr__(self):
		# print drinks as tabulate table
		table = []
		for k in sorted(inventory):
			table.append([self.artNum, self.name, self.get_bottle_price()])
		return (tabulate(table, headers=["Artikel#","Name", "Preis Flasche"]))
 	
 	
	def get_cost_MwSt(self):
		return self.unitCost*1.19
	
	def get_bottle_price(self):
		return round(((self.get_cost_MwSt() / self.bottlesPerUnit) + 0.1), 2)

class order(Base):
	
	__tablename__ = "tblOrder"
	
	OrderID = Column(Integer, primary_key=True)
	timestamp = Column(DateTime) # how does this one work?
	note = Column(String)
	

Base.metadata.create_all(engine)

"""----------------------------------------------------------------------------------------------"""
"""populate table"""

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
	for instance in session.query(drink.artNum):
		if input == instance.artNum:
			print("Artikel existiert schon in der Datenbank! Bitte versuchen Sie es erneut.\n\n")
			return False
		else:
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

while choose_to_input() == True:
	writeBuffer = []
	# check for uniqueness of Article Number:
	# query database for input
	# if row exists, error
	# else continue
	inputArtNum = int(raw_input("Artikelnummer:		"))
	if check_uniqueness(inputArtNum) == True:
		writeBuffer.append(inputArtNum)
	else: continue
	
	writeBuffer.append(raw_input("Artikel Name:		"))
	writeBuffer.append(int(raw_input("Flaschen pro Einheit:	")))
	writeBuffer.append(int(raw_input("Kasten pro Einheit:	")))
	writeBuffer.append(float(raw_input("Flaschenpfand:		")))
	writeBuffer.append(float(raw_input("Einkaufspreis:		")))
	writeBuffer.append(float(raw_input("Aufschlag pro Flasche:	")))
	
	if choose_to_accept() == False:
		pass
	else: continue

	if writeBuffer == []:
		print("Keine Angaben gefunden. Es wurde nichts gemacht")
	else:
		session.add(
			drink(
				artNum = writeBuffer.pop(0),
				name = writeBuffer.pop(0),
				bottlesPerUnit = writeBuffer.pop(0),
				cratesPerUnit = writeBuffer.pop(0),
				bottlePfand = writeBuffer.pop(0),
				unitCost = writeBuffer.pop(0),
				bottleSurcharge = writeBuffer.pop(0))
		)

def add_Products():
	while choose_to_input() == True:
		writeBuffer = []
		# check for uniqueness of Article Number:
		# query database for input
		# if row exists, error
		# else continue
		inputArtNum = int(raw_input("Artikelnummer:		"))
		if check_uniqueness(inputArtNum) == True: # this isn't working! wtf
			writeBuffer.append(inputArtNum)
		else: continue
	
		writeBuffer.append(raw_input("Artikel Name:		"))
		writeBuffer.append(int(raw_input("Flaschen pro Einheit:	")))
		writeBuffer.append(int(raw_input("Kasten pro Einheit:	")))
		writeBuffer.append(float(raw_input("Flaschenpfand:		")))
		writeBuffer.append(float(raw_input("Einkaufspreis:		")))
		writeBuffer.append(float(raw_input("Aufschlag pro Flasche:	")))
	
		if choose_to_accept() == False:
			pass
		else: continue

		if writeBuffer == []:
			print("Keine Angaben gefunden. Es wurde nichts gemacht")
		else:
			session.add(
				drink(
					artNum = writeBuffer.pop(0),
					name = writeBuffer.pop(0),
					bottlesPerUnit = writeBuffer.pop(0),
					cratesPerUnit = writeBuffer.pop(0),
					bottlePfand = writeBuffer.pop(0),
					unitCost = writeBuffer.pop(0),
					bottleSurcharge = writeBuffer.pop(0))
			)

add_Products()
session.commit()