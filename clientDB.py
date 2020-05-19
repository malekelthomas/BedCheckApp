import sqlite3
# connect to db
# create cursor obj
# 3 write an sql query
# 4 commit changes
# 5 close connection


def create_table(db_name):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS clientsList (name TEXT, caresID TEXT, roomNum TEXT, bed TEXT, signature TEXT, photoLocation TEXT)")
	conn.commit()
	conn.close()

def insert(db_name, name, caresID, roomNum, bed, signature, photoLocation):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("INSERT INTO clientsList VALUES (?,?,?,?,?,?)",(name, caresID, roomNum, bed, signature, photoLocation))
	conn.commit()
	conn.close()




def view(db_name):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("SELECT * FROM clientsList")
	rows = cur.fetchall()
	conn.close()
	return rows

def delete(db_name, caresID):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("DELETE FROM clientsList WHERE caresID=?", (caresID))
	conn.commit()
	conn.close()

def updateRoom(db_name, caresID, roomNum, bed):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("UPDATE clientsList SET roomNum =? AND bed =? WHERE caresID =?", (roomNum, bed, caresID))
	conn.commit()
	conn.close()

def updatePhotoLoc(db_name, caresID, photoLoc):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("UPDATE clientsList SET photoLocation=? WHERE caresID =?", (photoLoc, caresID))
	conn.commit()
	conn.close()
	
def searchByName(db_name, name):
	
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("SELECT * FROM clientsList WHERE name =?", (name,)) #for one var, place in tuple with comma afterwards or it will treat var as input sequence
	rows = cur.fetchall()
	conn.close()
	return rows

	
def searchByCaresID(db_name, caresID):
	
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("SELECT * FROM clientsList WHERE caresID =?",(caresID,))
	rows = cur.fetchall()
	conn.close()
	return rows
	
def searchByPhoto(db_name, photoloc):
	
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("SELECT * FROM clientsList WHERE photoloc =?",(photoloc,))
	rows = cur.fetchall()
	conn.close()
	return rows

