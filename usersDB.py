import sqlite3
# connect to db
# create cursor obj
# 3 write an sql query
# 4 commit changes
# 5 close connection


def create_table(db_name):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, password TEXT, user_type TEXT)")
	conn.commit()
	conn.close()


def insert(db_name, name, email, password, user_type):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("INSERT INTO users VALUES (?,?,?,?)",(name, email, password, user_type))
	conn.commit()
	conn.close()


def view(db_name):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("SELECT * FROM users")
	rows = cur.fetchall()
	conn.close()
	return rows

def delete(db_name, email, password):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("DELETE FROM users WHERE email =? ", (email,))
	conn.commit()
	conn.close()

def updatePassword(db_name, email, oldPassword, newPassword):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("UPDATE users SET password=? WHERE email=? AND password =?", (newPassword, email, oldPassword))
	conn.commit()
	conn.close()
	
def searchByEmail(db_name, email):
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	cur.execute("SELECT * FROM users WHERE email=?", (email,))
	rows = cur.fetchall()
	conn.close()
	return rows

