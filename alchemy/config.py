from __future__ import division
from tabulate import tabulate
import os

from sqlalchemy import create_engine
engine = create_engine('sqlite:///alchemy.db', echo=False)    # echo=True to show SQL statements

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


"""----------------------------------------------------------------------------------------------"""
# common functions

from initialize_db import Product

def check_exists(input):
	for instance in session.query(Product.artNum):
		if instance.artNum == input:
			return True
	return False

def yes_no(question, yes="", no=""):
	while True:
		print question + " j/n:"
		choice = raw_input("> ")
		if choice == "j":
			if yes != "":
				print yes
			return True
		elif choice == "n":
			if no != "":
				print no
			return False
		else:
			print "Bitte entweder 'j' oder 'n' eingeben"
			continue

def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')