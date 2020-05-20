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
	
def isBedOpen(room, bed, openRooms):
	isBedOcc = isRoomOpen(openRooms, room)

	if isBedOcc == bed or isBedOcc == bed.lower() or isBedOcc == "Empty":
		return True
	else:
		print("Bed occupied")
		return False


def isRoomOpen(openRooms, room):
	if openRooms[room]["A"] == "Open" and openRooms[room]["B"] == "Open":
		return "Empty"
	elif openRooms[room]["A"] == "Open" and openRooms[room]["B"] != "Open":
		return "A"
	elif openRooms[room]["B"] == "Open" and openRooms[room]["A"] != "Open":
		return "B"
	else:
		return "Full"

def occupyBed(openRooms, room, bed):
	if isBedOpen(room, bed, openRooms):
		openRooms[room][bed.upper()] = "Occupied"
		return True
	else:
		return False

def checkClientDirExists(caresID):
	
	path = os.getcwd()
	clientDir = path+"/clients/{}".format(caresID)
	
	if os.path.exists(clientDir):
		#print("Client dir already Exists")
		return clientDir
	else:
		#print("Created Client dir")
		os.mkdir(clientDir)
		return clientDir

def checkPhotoDirExists(caresID):
	path = os.getcwd()
	photoDir = path+"/clients/{}/photos".format(caresID)
	
	if os.path.exists(photoDir):
		#print("Photo dir already exists")
		return (True, photoDir)
	else:
		#print("Created photo dir for {}".format(ID))
		return (False, photoDir)
def checkSignatureDirExists(caresID):
	path = os.getcwd()
	sigDir = path+"/clients/{}/signatures".format(caresID)
	
	if os.path.exists(sigDir):
		#print("Photo dir already exists")
		return (True, sigDir)
	else:
		#print("Created photo dir for {}".format(ID))
		return (False, sigDir)

def createSignatureOrPhotoDir(clientsDB, caresID, *args):
	client = clientDB.searchByCaresID(clientsDB, caresID)
	if client == []:
		#path = os.getcwd()+"/clients/"
		#photoLocation = path+str(caresID)+"/photos"
		#signatureLocation = path+str(caresID)+"/signatures"
		if checkClientDirExists(caresID):
			if "photo" in args:
				if not checkPhotoDirExists(caresID)[0]:
					photoLocation = checkPhotoDirExists(caresID)[1]
					os.mkdir(photoLocation)
					#print("Created Client photo dir:",photoLocation)
					clientDB.updatePhotoLoc(clientsDB, caresID, photoLocation)
					return photoLocation
				else:
					return checkPhotoDirExists(caresID)[1]
			elif "signature" in args:
				if not checkPhotoDirExists(caresID)[0]:
					signatureLocation = checkSignatureDirExists(caresID)[1]
					os.mkdir(signatureLocation)
					#print("Created Client photo dir:",photoLocation)
					clientDB.updateSignatureLoc(clientsDB, caresID, signatureLocation)
					return signatureLocation
				else:
					return checkSignatureDirExists(caresID)[1]
	else:
		if "photo" in args:
			#print(client[0][5])
			return client[0][5]
		elif "signature" in args:
			#print(client[0][4])
			return client[0][4]
			
			
def changeRoom(clientsDB, caresID, room, bed):

	client = clientDB.searchByCaresID(clientsDB, caresID)
	
	if client != None:
		clientDB.updateRoom(clientsDB, caresID, room, bed)
		signature = "signature"
		
def removeClient(clientsDB, caresID):
	print("Client removed")
	return clientDB.delete(clientsDB, caresID)

def addClient(clientsDB, name, caresID, roomNum, bed, openRooms):
	if clientDB.searchByCaresID(clientsDB, caresID) == []:
		if isRoomOpen(openRooms, roomNum) != "Full":
			if isBedOpen(roomNum, bed, openRooms):
				occupyBed(openRooms, roomNum, bed)
				return clientDB.insert(clientsDB, name, caresID, roomNum, bed, createSignatureOrPhotoDir(clientsDB, caresID, "signature"), createSignatureOrPhotoDir(clientsDB, caresID,"photo"))
			else:
				return False
		else:
			print("Room is full, pick a room with an empty bed")
			return False
	else:
		print("Client already added")
		return False







roomsList = populateRoomNumbers(11,4,2)	

roomsAvailable = populateRoomsOpen(roomsList)

db = "clientList.db"
clientDB.create_table(db)

ID = 12345
ID2 = 54321
addClient(db, "Marc Edwards", ID, 501,"B", roomsAvailable)
addClient(db, "Mike Johnson", ID2, 501,"A", roomsAvailable)

showClients(db)

# removeClient(db, ID)

# removeClient(db, ID2)

# showClients(db)

print(roomsAvailable)
#print(isRoomOpen(roomsAvailable,501))
