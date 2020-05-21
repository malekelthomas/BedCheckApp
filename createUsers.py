import usersDB


def checkUserExists(db, email):
	user = usersDB.searchByEmail(db, email)
	if user == []:
		return False
	else:
		print("User already exists")
		return True

def createUser(db, name,email, password, user_type):
	userExists = checkUserExists(db, email)
	if not userExists:
		usersDB.insert(db, name,email, password, user_type)
		return True
	else:
		return False

def viewUsers(db):
	users = usersDB.view(db)
	
	for i in users:
		print(i)
		print("\n")


database = "users.db"
usersDB.create_table(database)

createUser(database,"Maleke Thomas","malekelthomas97@gmail.com", "12341", "SSO")


viewUsers(database)