import os
import platform
import clientDB
from PIL import Image

def populateRoomNumbers(numRoomsPerFloor, numFloors, floorStart):
	
	start = floorStart*100+1
	end = 100*(floorStart+(numFloors-floorStart)+1)+11
	rooms = [i for i in range(start,end+1) if i % 100 <= numRoomsPerFloor]
	
	return rooms
	
def populateRoomsOpen(rooms):
	roomsOpen = {}
	for i in rooms:
		roomsOpen[i] = {"A": "Open", "B": "Open"}
	return roomsOpen
	

def showClients(clients):
	allClients = clientDB.view(clients)
	
	for i in allClients:
		print(i)
		print("\n")
	
def getPhotoLoc(clientsdb, name):
	client = clientDB.searchByName(clientsdb, name)
	for i in client:
		return i[-1]

def openPhoto(photoLocation):
	im = Image.open(photoLocation+".jpg")
	im.show()
	
def isRoomOpen(openRooms, room):
	if openRooms[room]["A"] == "Open":
		return (True, "A is Open")
	elif openRooms[room]["B"] == "Open":
		return (True, "B is Open")
	else:
		return (False, "Full")

def createPhotoDir(clientsDB, name):
	client = clientDB.searchByName(clientsDB, name)
	
	if client is None:
		clientInfo = input("Enter Cares ID, Room Number, and Bed: ").split()
		signature = "signature"
		photoDirName = clientInfo+x[:].join("")
		path = os.getcwd()+"/client_Photos/"
		photoLocation = path+photoDirName
		print("Created dir:", photoLocation)
		clientDB.insert(clientsDB, name, x[0], x[1], x[2], signature, photoLocation)
	else:
		for info in client:
			caresID = input("Enter Cares ID: ")
			if caresID in info:
				roomChange = input("Room Number: ")
				clientDB.updateRoom(clientsDB, caresID, roomChange)
				signature = "signature"
				photoDirName = info[:-2]
				path = os.getcwd()+"/client_Photos/"
				photoLocation = path+photoDirName
				print("Updated to dir:", photoLocation)
				clientDB.updatePhotoLoc(caresID, photoLocation)





roomsList = populateRoomNumbers(11,4,2)	

roomsAvailable = populateRoomsOpen(roomsList)

db = "clientList.db"
clientDB.create_table(db)



#clientDB.insert(db, "Marc Edwards", 7873637, 501,"B", "jfndkd", z)

showClients(db)
x = openPhoto(getPhotoLoc(db, "Marc Edwards"))
print(os.name)
print(platform.system())
print(isRoomOpen(roomsAvailable,501))