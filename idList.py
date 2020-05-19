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

def getPhoto(photoLocation):
	im = Image.open(photoLocation+".jpg")
	return im
	
def isRoomOpen(openRooms, room):
	if openRooms[room]["A"] == "Open":
		return "A"
	elif openRooms[room]["B"] == "Open":
		return "B"
	else:
		return "Full"
		
def checkClientDirExists(clientsDB, name):
	client = clientsDB.searchByName(clientDB, name)
	
	
	path = os.getcwd()
	clientDir = path+"/clients/{}".format(client[1])
	
	if os.path.exists(clientDir):
		return True
	else:
		return False
	

def createPhotoDir(clientsDB, name):
	client = clientDB.searchByName(clientsDB, name)
	
	if client is None:
		clientInfo = input("Enter Cares ID, Room Number, and Bed: ").split()
		signature = "signature"
		photoDirName = clientInfo[0].strip()
		path = os.getcwd()+"/clients/"
		photoLocation = path+photoDirName+"/photos"
		os.mkdir(photoLocation)
		print("Created dir:", photoLocation)
		clientDB.insert(clientsDB, name, clientInfo[0], clientInfo[1], clientInfo[2], signature, photoLocation)
		return photoLocation
	else:
		if checkClientDirExists(clientsDB,client[1]):
			print("Directory already exists:", client[5])
			return client[5]
			
def createClientDir(clientsDB, name):
	client = clientDB.searchByName(clientsDB, name)
	
	path = os.getcwd()+"/clients/"
	clientDir = path+client[0]
	if client is None:
		if not os.path.exists(clientDir):
			os.mkdir(clientDir)
			print("Directory created:", clientDir)
			return clientDir
		
			
			
		
		
			
		
		
def changeRoom(clientsDB, caresID, room, bed):

	client = clientDB.searchByCaresID(clientsDB, caresID)
	
	if client != None:
		clientDB.updateRoom(clientsDB, caresID, room, bed)
		signature = "signature"
		
		





roomsList = populateRoomNumbers(11,4,2)	

roomsAvailable = populateRoomsOpen(roomsList)

db = "clientList.db"
clientDB.create_table(db)



clientDB.insert(db, "Marc Edwards", 7873637, 501,"B", "jfndkd", createPhotoDir(clientDB, "Marc Edwards"))

showClients(db)
print(isRoomOpen(roomsAvailable,501))

createPhotoDir(db, "Marc Edwards")