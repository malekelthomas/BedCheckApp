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

def createPhotoLoc(clientsDB, client):
	pass

roomsList = populateRoomNumbers(11,4,2)	

roomsAvailable = populateRoomsOpen(roomsList)

db = "clientList.db"
clientDB.create_table(db)

z=os.getcwd()+"/client_Photos/Marc_Edwards_7873637"

#clientDB.insert(db, "Marc Edwards", 7873637, 501,"B", "jfndkd", z)

showClients(db)
openPhoto(getPhotoLoc(db, "Marc Edwards"))
print(os.name)
print(platform.system())
print(isRoomOpen(roomsAvailable,501))