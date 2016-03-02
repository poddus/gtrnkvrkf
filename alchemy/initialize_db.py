from config import *

from sqlalchemy import Table, Column, Integer, Float, String, DateTime, MetaData, ForeignKey, select
from sqlalchemy.orm import relationship

class Product(Base):
	"""
	Common base class for all products.
	A 'unit' is the smallest deliverable unit.
	"""

	__tablename__ = "tblProducts"

	artNum = Column(Integer, primary_key=True, autoincrement=False)
	name = Column(String(32))
	bottlesPerUnit = Column(Integer)
	cratesPerUnit = Column(Integer)
	bottlePfand = Column(Float)
	
	stocktakedetail = relationship("StockTakeDetail", back_populates="product")
	orderdetail = relationship("OrderDetail")

	def __repr__(self):
		table = []
		table.append(["Artikel#", self.artNum])
		table.append(["Name", self.name])
		table.append(["Fl pro E", self.bottlesPerUnit])
		table.append(["Ka pro E", self.cratesPerUnit])
		table.append(["Pfand pro Fl", self.bottlePfand])
		return (tabulate(table, numalign="left"))

# unit cost no longer stored in Product class/tbl. define function anyway (db-query StockTake) for convenience?
# 	def get_cost_MwSt(self):
# 		return self.unitCost*1.19
# 
# 	def get_bottle_price(self):
# 		return round(((self.get_cost_MwSt() / self.bottlesPerUnit) + 0.1), 2)

"""----------------------------------------------------------------------------------------------"""

class Order(Base):

	__tablename__ = "tblOrder"

	orderID = Column(Integer, primary_key=True)
	stockTakeID = Column(Integer, ForeignKey("tblStockTake.stockTakeID"))
	timestamp = Column(Integer)    # how does this one work?
	note = Column(String)
	
	# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-relationship
	stocktake = relationship("StockTake", back_populates="order")
	orderdetail = relationship("OrderDetail")
	
	def get_total(self):
		# TODO: add up subtotals from OrderDetail.get_subtotals(), return a nice table
		pass

class OrderDetail(Base):
	
	__tablename__ = "tblOrderDetail"
	
	orderDetailID = Column(Integer, primary_key=True)
	orderID = Column(Integer, ForeignKey("tblOrder.orderID"))
	artNum = Column(Integer, ForeignKey("tblProducts.artNum"))
	quantity = Column(Integer)
# 	pfandCrates = Column(Float)
# 	pfandBottles = Column(Integer)
	
	product = relationship("Product", back_populates="orderdetail")
	
	def get_subtotals(self, orderID):
		# TODO:
		# query tblOrderDetail for all entries with given orderID
		# query
		pass

"""----------------------------------------------------------------------------------------------"""

class StockTake(Base):
	
	__tablename__ = "tblStockTake"
	stockTakeID = Column(Integer, primary_key=True)
	timestamp = Column(Integer)    # how does this one work?
	note = Column(String)
	
	stocktakedetail = relationship("StockTakeDetail")
	order = relationship("Order", back_populates="stocktake")
	
	def get_initial_inventory_value(self, StockTake):
		# TODO: should value be what we payed for it or what we get when selling?
		total = 0
		details = self.stocktakedetail
		
		for instances in details:
			total += details.get_unit_price()
		
		# TODO: also take Pfand into account
		
		return total

class StockTakeDetail(Base):
	"""
	'cost' is what we pay.
	'price' is what the customer pays.
	"""
	
	__tablename__ = "tblStockTakeDetail"
	
	stockTakeDetailID = Column(Integer, primary_key=True)
	stockTakeID = Column(Integer, ForeignKey("tblStockTake.stockTakeID"))
	artNum = Column(Integer, ForeignKey("tblProducts.artNum"))
	quantity = Column(Integer)
	unitCost = Column(Float)    # pro Liefereinheit, also praktisch pro Kasten
	bottleSurcharge = Column(Float)
	pfandCrates = Column(Float)
	pfandBottles = Column(Integer)
	
	product = relationship("Product", back_populates="stocktakedetail")
	
	def get_unit_price(self):
		return (self.unitCost*1.19 + (self.bottleSurcharge * self.product.bottlesPerUnit))
	
	def get_bottle_price(self):
		return round(self.get_unit_price() / self.product.bottlesPerUnit, 2)

Base.metadata.create_all(engine)

"""----------------------------------------------------------------------------------------------"""
# if doesn't exist, create Products for Pfand bottles to database
# 
# This is necessary in order to track additional Pfand Bottles without having to
# worry about what's on the label

# I need this but can't get it from config due to circular dependencies
def init_check_exists(input):
	for instance in session.query(Product.artNum):
		if instance.artNum == input:
			return True
	return False

crate = Product(
	artNum = 10000,
	name = "Pfandkasten",
	bottlesPerUnit = 0,
	cratesPerUnit = 0,
	bottlePfand = 0,
)

bottle008 = Product(
	artNum = 10001,
	name = "0.08 Pfandflasche",
	bottlesPerUnit = 0,
	cratesPerUnit = 0,
	bottlePfand = 0.08,
)

bottle015 = Product(
	artNum = 10002,
	name = "0.15 Pfandflasche",
	bottlesPerUnit = 0,
	cratesPerUnit = 0,
	bottlePfand = 0.15,
)

if init_check_exists(crate.artNum) is False:
	session.add(crate)
	session.commit()

if init_check_exists(bottle008.artNum) is False:
	session.add(bottle008)
	session.commit()

if init_check_exists(bottle015.artNum) is False:
	session.add(bottle015)
	session.commit()