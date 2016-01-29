from sqlalchemy import create_engine
engine = create_engine('sqlite:///alchemy.db', echo=False)    # echo=True to show SQL statements

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Table, Column, Integer, Float, String, DateTime, MetaData, join, ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):
	"""
	Common base class for all products.
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
#	the following have been moved to StockTake
# 	unitCost = Column(Float)    # pro Liefereinheit, also praktisch pro Kasten
# 	bottleSurcharge = Column(Float)

	def __repr__(self):
		# print products as tabulate table
		table = []
		for k in sorted(inventory):    # inventory variable needs to be changed to a database query
			table.append([self.artNum, self.name, self.get_bottle_price()])
		return (tabulate(table, headers=["Artikel#", "Name", "Preis Flasche"]))

	def get_cost_MwSt(self):
		return self.unitCost*1.19

	def get_bottle_price(self):
		return round(((self.get_cost_MwSt() / self.bottlesPerUnit) + 0.1), 2)

"""----------------------------------------------------------------------------------------------"""

class Order(Base):

	__tablename__ = "tblOrder"

	OrderID = Column(Integer, primary_key=True)
	timestamp = Column(DateTime)    # how does this one work?
	note = Column(String)
	
	def get_total(self):
		# add up subtotals from OrderDetail.get_subtotals(), return a nice table
		pass
	
	# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-relationship
	orderdetail = relationship("OrderDetail")

class OrderDetail(Base):
	
	__tablename__ = "tblOrderDetail"
	
	OrderDetailID = Column(Integer, primary_key=True)
	OrderID = Column(Integer, ForeignKey('tblOrder.OrderID'))
	artNum = Column(Integer, ForeignKey('tblProducts.artNum'))
	quantity = Column(Integer)
	pfandCrates = Column(Float)
	pfandBottles = Column(Integer)
	
	def get_subtotals(self, OrderID):
		# query tblOrderDetail for all entries with given OrderID
		# query
		pass

"""----------------------------------------------------------------------------------------------"""

class StockTake(Base):
	
	__tablename__ = "tblStockTake"
	StockTakeID = Column(Integer, primary_key=True)
	timestamp = Column(DateTime)    # how does this one work?
	note = Column(String)
	
	stocktakedetail = relationship("StockTakeDetail")
	
	def get_inventory_value(self, StockTake):
		# query tblOrderDetail for all entries with given OrderID
		# query
		pass

class StockTakeDetail(Base):
	
	__tablename__ = "tblStockTakeDetail"
	
	StockTakeDetailID = Column(Integer, primary_key=True)
	StockTakeID = Column(Integer, ForeignKey('tblStockTake.StockTakeID'))
	artNum = Column(Integer, ForeignKey('tblProducts.artNum'))
	quantity = Column(Integer)
	unitCost = Column(Float)    # pro Liefereinheit, also praktisch pro Kasten
	bottleSurcharge = Column(Float)
	pfandCrates = Column(Float)
	pfandBottles = Column(Integer)

Base.metadata.create_all(engine)
