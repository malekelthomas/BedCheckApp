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
		return clientDir
	else:
		print("Created Client dir")
		os.mkdir(clientDir)
		return clientDir

def checkPhotoDirExists(ID):
	path = os.getcwd()
	photoDir = path+"/clients/{}/photos".format(ID)
	
	if os.path.exists(photoDir):
		print("Photo dir already exists")
		return photoDir
	else:
		print("Created photo dir for {}".format(ID))
		os.mkdir(photoDir)
		return photoDir

def createSignatureOrPhotoDir(clientsDB, caresID, *args):
	client = clientDB.searchByCaresID(clientsDB, ID)
	
	if client == []:
		path = os.getcwd()+"/clients/"
		photoLocation = path+str(caresID)+"/photos"
		signatureLocation = path+str(caresID)+"/signatures"
		if checkClientDirExists(ID):
			if "photo" in args:
				os.mkdir(photoLocation)
				print("Created Client photo dir:",photoLocation)
				clientDB.updatePhotoLoc(clientsDB, ID, photoLocation)
				return photoLocation
			elif "signature" in args:
				os.mkdir(signatureLocation)
				print("Created Client signature dir:", signatureLocation)
				clientDB.updateSignatureLoc(clientsDB, ID, signatureLocation)
				return signatureLocation
	else:
		if "photo" in args:
			print(client[0][5])
			return client[0][5]
		elif "signature" in args:
			print(client[0][4])
			return client[0][4]
			
			
def changeRoom(clientsDB, caresID, room, bed):

	client = clientDB.searchByCaresID(clientsDB, caresID)
	
	if client != None:
		clientDB.updateRoom(clientsDB, caresID, room, bed)
		signature = "signature"
		
		
		





roomsList = populateRoomNumbers(11,4,2)	

roomsAvailable = populateRoomsOpen(roomsList)

db = "clientList.db"
clientDB.create_table(db)


ID = 12345
clientDB.insert(db, "Marc Edwards", ID, 501,"B", createSignatureOrPhotoDir(db, ID, "signature"), createSignatureOrPhotoDir(db, ID, "photo"))

showClients(db)
#print(isRoomOpen(roomsAvailable,501))
