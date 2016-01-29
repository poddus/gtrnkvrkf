from sqlalchemy import create_engine
engine = create_engine('sqlite:///alchemy.db', echo=False)    # echo=True to show SQL statements

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from initialize_db import Product, Order, StockTake

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


# show preisliste
#	query database for last StockTake where quantity > 0
#	print nice table of results (tabulate?)
#
# ask to add a new product to order
# select article using artNum
# 	? print info about article
# 
# select amount
#	print subtotal
#	? also total
#
# write selection to session
# session.add(Order...)
# 
# repeat until order is complete
# 
# Pfand zurück?
# 	Anzahl der Kasten (float, because half-crates!)
# 	Anzahl der 0.08 Flaschen
# 	Anzahl der 0.15 Flaschen
# Pfand mitnehmen? (Flaschen sind schon verrechnet, hier NUR KASTEN)
# 
# write net Pfand to order
# 
# print order, give choice:
# 	acknowledge, continue to check out
# 	request change, return to point 3, but retain order information
# 		if changes are made, overwrite previous choice, else keep choices
# 
# check out
# calculate change
# 
# write transaction to database, update inventory
# return to beginning
