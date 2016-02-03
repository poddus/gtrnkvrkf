from config import *

def edit_write_buffer(inputArtNum):
	writeBuffer = []
	writeBuffer.append(inputArtNum)
	writeBuffer.append(raw_input("Artikel Name:		"))
	while True:
		try:
			writeBuffer.append(int(raw_input("Flaschen pro Einheit:	")))
			break
		except:
			print "Bitte nur ganze Zahlen eingeben!\n"
	
	while True:
		try:
			writeBuffer.append(int(raw_input("Kasten pro Einheit:	")))
			break
		except:
			print "Bitte nur ganze Zahlen eingeben!\n"
	
	while True:
		try:
			writeBuffer.append(float(raw_input("Flaschenpfand:		")))
			break
		except:
			print "Bitte nur Dezimalzahlen eingeben!\n"
	
	return writeBuffer

def create_new_product(inputArtNum):
	writeBuffer = edit_write_buffer(inputArtNum)
	
	clear_screen()
	newProduct = Product(
		artNum = writeBuffer.pop(0),
		name = writeBuffer.pop(0),
		bottlesPerUnit = writeBuffer.pop(0),
		cratesPerUnit = writeBuffer.pop(0),
		bottlePfand = writeBuffer.pop(0),
	)
	
	print newProduct
	if yes_no(
		"\nBitte ueberpruefen Sie ihre Angaben. Bestaetigen?",
		"Angaben akzeptiert, werden am Schluss in der Datenbank gespeichert.",
		"Angaben verworfen!"
		) is True:
		raw_input()
		clear_screen()
		
		session.add(newProduct)
	else:
		raw_input()
		clear_screen()
		pass

def edit_existing(inputArtNum):
	existingProduct = session.query(Product).filter(Product.artNum == inputArtNum).first()
	print existingProduct
	print 
	# is there a way to retain existing values?
	print "Achtung: Alle Eingaben muessen neu ausgefuellt werden\n"
	print "Artikelnummer:		%d" % inputArtNum
	writeBuffer = edit_write_buffer(inputArtNum)
	del writeBuffer[0]    # remove artNum, we don't want to CHANGE that ever, right?
	
	if yes_no(
		"\nBitte ueberpruefen Sie ihre Angaben. Bestaetigen?",
		"Angaben akzeptiert, werden am Schluss in der Datenbank gespeichert.",
		"Angaben verworfen!"
		) is True:
		raw_input()
		clear_screen()
		
		existingProduct.name = writeBuffer.pop(0)
		existingProduct.bottlesPerUnit = writeBuffer.pop(0)
		existingProduct.cratesPerUnit = writeBuffer.pop(0)
		existingProduct.bottlePfand = writeBuffer.pop(0)
	else:
		raw_input()
		clear_screen()
		pass

def add_products():	
	while yes_no("Neues Product eingeben?") is True:
		while True:
			try:
				inputArtNum = int(raw_input("Artikelnummer:		"))
				break
			except TypeError:
				print "Bitte nur Ziffern eingeben!"
		
		if check_exists(inputArtNum) is False:    # if unique
			create_new_product(inputArtNum)
		elif yes_no("Artikel existiert schon in der Datenbank! Moechten Sie die Daten aendern?") is True:
			clear_screen()
			edit_existing(inputArtNum)
		else:
			clear_screen()
			continue

def write_products():
	add_products()
	session.commit()
