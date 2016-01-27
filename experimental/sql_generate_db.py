from __future__ import print_function, division

import sqlite3 as lite

con = lite.connect('database.db')

with con:
	cur = con.cursor()
	cur.execute("CREATE TABLE tblProducts(artNum INT PRIMARY KEY, Name TEXT, bottlesPerUnit INT, cratesPerUnit INT, bottlePfand FLOAT, unitCost FLOAT, bottleSurcharge FLOAT)")
	
	cur.execute("CREATE TABLE tblOrder(OrderID INT PRIMARY KEY, timestamp TEXT)")
	cur.execute("CREATE TABLE tblOrderDetail(OrderDetailID INT PRIMARY KEY, OrderID INT, artNum INT, quantity INT, pfandCrates FLOAT, pfandBottles INT, FOREIGN KEY(OrderID) REFERENCES tblOrder(OrderID), FOREIGN KEY(artNum) REFERENCES tblProducts(artNum))")
	
	cur.execute("CREATE TABLE tblStockTake(StockTakeID INT, timestamp TEXT, note TEXT)")
	cur.execute("CREATE TABLE tblStockTakeDetail(StockTakeDetailID INT PRIMARY KEY, StockTakeID INT, artNum INT, quantity INT, pfandCrates FLOAT, pfandBottles INT, FOREIGN KEY(StockTakeID) REFERENCES tblStockTake(StockTakeID), FOREIGN KEY(artNum) REFERENCES tblProducts(artNum))")
	
	cur.execute("CREATE TABLE tblShipment(ShipmentID INT PRIMARY KEY, timestamp TEXT, note TEXT)")
	cur.execute("CREATE TABLE tblShipmentDetail(ShipmentDetailID INT PRIMARY KEY, ShipmentID INT, artNum INT, quantity INT, pfandCrates FLOAT, pfandBottles INT, FOREIGN KEY(ShipmentID) REFERENCES tblShipment(ShipmentID), FOREIGN KEY(artNum) REFERENCES tblProducts(artNum))")
	
	# for testing, populate with data
	cur.execute("INSERT INTO tblProducts VALUES(1072, 'Augustiner Hell', 20, 1, 0.08, 10.972, 0.10)")