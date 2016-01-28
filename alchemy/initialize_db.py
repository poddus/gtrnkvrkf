from sqlalchemy import create_engine
engine = create_engine('sqlite:///alchemy.db', echo=False)    # echo=True to show SQL statements

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, Float, String, DateTime
class Drink(Base):
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
	unitCost = Column(Float)    # pro Liefereinheit, also praktisch pro Kasten
	bottleSurcharge = Column(Float)

	def __repr__(self):
		# print drinks as tabulate table
		table = []
		for k in sorted(inventory):    # inventory variable needs to be changed to a database query
			table.append([self.artNum, self.name, self.get_bottle_price()])
		return (tabulate(table, headers=["Artikel#", "Name", "Preis Flasche"]))

	def get_cost_MwSt(self):
		return self.unitCost*1.19

	def get_bottle_price(self):
		return round(((self.get_cost_MwSt() / self.bottlesPerUnit) + 0.1), 2)

class Order(Base):

	__tablename__ = "tblOrder"

	OrderID = Column(Integer, primary_key=True)
	timestamp = Column(DateTime)    # how does this one work?
	note = Column(String)


Base.metadata.create_all(engine)
