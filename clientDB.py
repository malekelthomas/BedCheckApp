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
	cur.execute("DELETE FROM clientsList WHERE caresID=?", caresID)
	conn.commit()
	conn.close()

def update(db_name, roomNum):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("UPDATE clientList SET name=?  AND caresID=? AND bed AND signature AND photo WHERE roomNum =?", roomNum)
	conn.commit()
	conn.close()
	
def searchByName(db_name, name):
	
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("SELECT * FROM clientList WHERE name =?", name)
	rows = cur.fetchall()
	conn.close()
	return rows

	
def searchByCaresID(db_name, caresID):
	
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("SELECT * FROM clientList WHERE caresID =?", caresID)
	rows = cur.fetchall()
	conn.close()
	return rows
	

