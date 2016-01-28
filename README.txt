The main program currently resides in the "alchemy" folder.

Dependencies:
tabulate
sqlite3
sqlalchemy

Pseudo Code Verkauf:

1 start program
	open database
	start database session
2 show preisliste
	artikelnummer
	name
	preis pro flasche
	preis pro kasten
	bestand

3 select article
	print info about article

4 select amount
5 print acknowledgement
6 write selection to order

7 repeat 3 to 6 until order is complete

8 Pfand zurück?
	Anzahl der Kasten (float, because half-crates!)
	Anzahl 0.08 Flaschen
	Anzahl 0.15 Flaschen
9 Pfand mitnehmen? (Flaschen sind schon verrechnet, hier NUR KASTEN)

10 write net Pfand to order

11 print order, give choice:
	acknowledge, continue to check out
	request change, return to point 3, but retain order information
		if changes are made, overwrite previous choice, else keep choices

12 check out
13 calculate change

14 write transaction to database, update inventory
15 return to 2