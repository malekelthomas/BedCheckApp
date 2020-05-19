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

def checkClientDirExists(ID):
	
	path = os.getcwd()
	clientDir = path+"/clients/{}".format(ID)
	
	if os.path.exists(clientDir):
		print("Client dir already Exists")
		return False
	else:
		print("Created Client dir")
		os.mkdir(clientDir)
		return clientDir
	

def createSignatureOrPhotoDir(clientsDB, name, *args):
	client = clientDB.searchByName(clientsDB, name)
	
	if client == []:
		clientInfo = input("Enter Cares ID, Room Number, and Bed: ").split(",")
		signature = "signature"
		DirName = clientInfo[0].strip()
		path = os.getcwd()+"/clients/"
		photoLocation = path+DirName+"/photos"
		signatureLocation = path+DirName+"/signatures"
		if "photo" in args:
			if checkClientDirExists(clientInfo[0].strip()):
				os.mkdir(photoLocation)
				print("Created Client photo dir:",photoLocation)
				clientDB.updatePhotoLoc(clientsDB, DirName, photoLocation)
				return photoLocation
			else:
				if not checkClientDirExists(client[0].strip()):
					return client[5]
		elif "signature" in args:
			if checkClientDirExists(clientInfo[0].strip()):
				os.mkdir(signatureLocation)
				print("Created Client signature dir:", signatureLocation)
				clientDB.updateSignatureLoc(clientsDB, DirName, signatureLocation)
				return signatureLocation
			else:
				if not checkClientDirExists(clientInfo[0].strip()):
					return client[4]
			
def changeRoom(clientsDB, caresID, room, bed):

	client = clientDB.searchByCaresID(clientsDB, caresID)
	
	if client != None:
		clientDB.updateRoom(clientsDB, caresID, room, bed)
		signature = "signature"
		
		





roomsList = populateRoomNumbers(11,4,2)	

roomsAvailable = populateRoomsOpen(roomsList)

db = "clientList.db"
clientDB.create_table(db)



clientDB.insert(db, "Marc Edwards", 7873637, 501,"B", "jfndkd", createPhotoDir(db, "Marc Edwards"))

showClients(db)
print(isRoomOpen(roomsAvailable,501))

#createPhotoDir(db, "Marc Edwards")