from __future__ import division

class drink:
	"""
	Common base class for all drinks.
	A 'unit' is the smallest deliverable unit.
	'cost' is what we pay.
	'price' is what the customer pays.
	"""
	
	def __init__(
		self,
		name,
		artNum,
		bottlesPerUnit,
		cratesPerUnit,
		unitCost, # pro Liefereinheit, also praktisch pro Kasten
		bottlePfand
	):
		
		self.name = name
		self.artNum = artNum
		self.bottlesPerUnit = bottlesPerUnit
		self.cratesPerUnit = cratesPerUnit
		self.unitCost = unitCost
		self.bottlePfand = bottlePfand
	
	
	def get_cost_MwSt(self):
		return self.unitCost*1.19
	
	def get_bottle_price(self):
		return round(((self.get_cost_MwSt() / self.bottlesPerUnit) + 0.1), 2)
		
	def get_crate_price(self):
		return round((self.get_bottle_price() * self.bottlesPerUnit), 1)
		
a1072 = drink(
	"Augustiner Hell",
	1072,
	20,
	1,
	10.972,
	0.08)

a1602 = drink(
	"Karamalz",
	1602,
	20,
	1,
	8.506,
	0.08)

a1802 = drink(
	"Tegernseer Hell",
	1802,
	20,
	1,
	11.395,
	0.08)
	

inventory = { # amounts in unit of bottles
	a1072:20,
	a1602:40,
	a1802:60}

# for users to make a selection, we need a dict to translate what they input into the object:
selectionDict = {}
for k in inventory:
	selectionDict[k.artNum] = k # the key is an integer!