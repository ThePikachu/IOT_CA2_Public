from flask import Flask, render_template, jsonify, request, redirect, url_for,session,send_from_directory
from Shared.User import User
from Shared.Room import Room
from Shared.AccessRight import AccessRight
from Shared.AccessLog import AccessLog
from Shared.AccessRequest import AccessRequest
from Shared.EnviroInfo import EnviroInfo
from Shared.MotionEvent import MotionEvent
from Shared.Configs import Config
import signal
import socket
from datetime import datetime
from SigV4Utils import SigV4Utils
from urllib.parse import quote_plus
import os
from twilio.twiml.messaging_response import Message, MessagingResponse
from Bots.whatsappbot import WhatsAppBot
app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.secret_key = b'\xe1\xa5\x0f\xe7\x12KQ\xb0\xd3e\xbf\xb5\xfb\xdf]\xbf'

def IsAuthenticated():
	if 'UserId' not in session:
		return False
	return True

def IsAuthorised():
	if not IsAuthenticated() or not session['IsAdmin']:
		return False
	return True

def redirectIfNotLoginAndRender(templateName, **kwargs):
	if IsAuthenticated() == False:
		return redirect(url_for('.loginPage'))
	return render_template(templateName,Username = session['Username'],IsAdmin = session['IsAdmin'],**kwargs)

@app.route("/")
def loginPage():
	if IsAuthenticated() == True:
		return redirect(url_for('.dashboardPage')) if session['IsAdmin'] else redirect(url_for('.publicDashBoardPage'))
	errorMsg = ""
	errorCode = request.args.get('error')
	if errorCode != None:
		if int(errorCode) == 1:
			errorMsg = "Wrong username or password"

	return render_template('login.html',error=errorMsg)

@app.route("/register")
def registerPage():
	errorMsg = ""
	errorCode = request.args.get('error')
	if errorCode != None:
		if int(errorCode) == 1:
			errorMsg = "Username or password cannot be blank"
		if int(errorCode) == 2:
			errorMsg = "Passwords do not match"
	return render_template('register.html',error=errorMsg)

@app.route("/dashboard")
def dashboardPage():
	if IsAuthenticated() == True:
		return redirectIfNotLoginAndRender('dashboard.html',rooms = Room.GetAllRooms()) if session['IsAdmin'] else redirect(url_for('.publicDashBoardPage'))
	return redirect(url_for('.loginPage'))

@app.route("/publicdashboard")
def publicDashBoardPage():
	return redirectIfNotLoginAndRender('publicDashboard.html', user = User.TryGetUserById(session['UserId']), rooms = Room.GetAllRooms()) if not session['IsAdmin'] else redirect(url_for('.dashboardPage'))

@app.route("/ManageRooms")
def manageRoomsPage():
	return redirectIfNotLoginAndRender('manage_rooms.html')

@app.route("/RoomAccessRights")
def roomAccessRightsPage():
	return redirectIfNotLoginAndRender('room_access_rights.html',users = User.GetUsers(), rooms = Room.GetAllRooms())

@app.route("/ManageApprovals")
def manageApprovalsPage():
	return redirectIfNotLoginAndRender('manage_approvals.html',users = User.GetUsers(), rooms = Room.GetAllRooms())

#----------------------------------------------------------------------------------------------

@app.route("/api/login",methods = ['POST'])
def loginAPI():
	user = User.ParseFromForm(request.form)
	if not user.IsValid():
		return redirect(url_for('.loginPage', error=1))
	elif not user.TryLogin():
		return redirect(url_for('.loginPage', error=1))
	session['UserId'] = user.Id
	session['Username'] = user.Username
	session['IsAdmin'] = user.IsAdmin()
	return redirect(url_for('.dashboardPage')) if user.IsAdmin() else redirect(url_for('.publicDashBoardPage'))

@app.route("/api/register",methods = ['POST'])
def registerAPI():
	user = User.ParseRegistrationForm(request.form)
	if user.registerUser() == "1":
		return redirect(url_for('.registerPage', error=1))
	if user.registerUser() == "2":
		return redirect(url_for('.registerPage', error=2))
	return redirect(url_for('.loginPage'))

@app.route("/api/logout")
def logoutAPI():
	session.pop('UserId', None)
	session.pop('Username', None)
	return redirect(url_for('.loginPage'))

#----------------------------------------------------------------------------------------------

@app.route("/api/getRooms")
def getRoomsAPI():
	if not IsAuthorised():
		return "Not authorised", 401
	return jsonify(Room.GetAllRoomsJSON())

@app.route("/api/updateRoom",methods = ['POST'])
def updateRoomAPI():
	if not IsAuthorised():
		return "Not authorised", 401
	room = Room.ParseFromForm(request.form)
	if not room.IsValidForUpdate():
		return "Missing Data", 400
	if room.TryUpdateDb() == False:
		return "Failed to update Database", 401
	return "Updated"

@app.route("/api/addRoom",methods = ['POST'])
def addRoomAPI():
	if not IsAuthorised():
		return "Not authorised", 401
	room = Room.ParseFromForm(request.form)
	if not room.IsValidForAdd():
		return "Missing Data", 400
	if room.TryAdd() == False:
		return "Failed to add into Database", 401
	return "added"

@app.route("/api/removeRoom",methods = ['POST'])
def removeRoomAPI():
	if not IsAuthorised():
		return "Not authorised", 401
	Id = request.form['IotId']
	if Id == None:
		return "Missing Data", 400
	room = Room(Id = Id)
	if not room.TryRemove():
		return "Failed to remove from Database", 401
	return "removed"

@app.route("/protected/<path:filename>")
def protected(filename):
	print(filename)
	print(app.instance_path)
	if not IsAuthorised():
		return "Not authorised", 401
	return send_from_directory(
        os.path.join(app.instance_path, 'protected'),
        filename
    )

#----------------------------------------------------------------------------------------------

@app.route("/api/getAccessRights")
def getAccessRightsAPI():
	if not IsAuthorised():
		return "Not authorised", 401
	return jsonify(AccessRight.GetAllAccessRights())

@app.route("/api/updateAccessRight",methods = ['POST'])
def updateAccessRightAPI():
	if not IsAuthorised():
		return "Not authorised", 401
	access_right = AccessRight.ParseFromForm(request.form)
	if not access_right.IsValidForUpdate():
		return "Missing Data", 400
	elif not access_right.TryUpdateDb():
		return "Failed to update Database", 401
	return "Updated"

@app.route("/api/addAccessRight",methods = ['POST'])
def addAccessRightAPI():
	if not IsAuthorised():
		return "Not authorised", 401
	access_right = AccessRight.ParseFromForm(request.form)
	if not access_right.IsValidForAdd():
		return "Missing Data", 400
	elif not access_right.TryAdd():
		return "Data already exist", 400
	return "added"

@app.route("/api/removeAccessRight",methods = ['POST'])
def removeAccessRightAPI():
	if not IsAuthorised():
		return "Not authorised", 401
	access_right = AccessRight.ParseFromForm(request.form)
	if not access_right.IsValidForRemove():
		return "Missing Data", 400
	elif not access_right.TryRemove():
		return "Failed to remove from Database", 401
	return "removed"


#----------------------------------------------------------------------------------------------

@app.route("/api/getAvgRoomTemps/<int:roomId>")
def getAvgRoomTempsAPI(roomId):
	if not IsAuthorised():
		return "Not authorised", 401
	room = Room.TryGetRoomById(roomId)
	if room == None:
		return "Error",400
	result = {
		"RoomName":room.RoomName,
		"data":EnviroInfo.GetAvgEnviroInfoByDay(room.Id)
	}
	return jsonify(result)

#----------------------------------------------------------------------------------------------

@app.route("/api/getValidAccessLog/<int:roomId>")
def getValidAccessLogAPI(roomId):
	if not IsAuthorised():
		return "Not authorised", 401
	result = AccessLog.GetValidExitedAccessLogForRoom(roomId)
	return jsonify(result)

@app.route("/api/getInvalidAccessLog/<int:roomId>")
def getInvalidAccessLogAPI(roomId):
	if not IsAuthorised():
		return "Not authorised", 401
	result = AccessLog.GetInvalidExitedAccessLogForRoom(roomId)
	return jsonify(result)

#----------------------------------------------------------------------------------------------

@app.route("/api/setLightStatus",methods = ['POST'])
def setLightStatusAPI():
	if not IsAuthorised():
		return "Not authorised", 401
	RoomId = request.form.get("RoomId")
	Status = request.form.get("Status")
	room = Room.TryGetRoom(socket.gethostname())
	if room == None or room.Id != int(RoomId):
		return "Error, not current room",401
	return "success"

#----------------------------------------------------------------------------------------------

@app.route("/api/getMotionEvents/<path:roomId>")
def getMotionEventsAPI(roomId):
	if not IsAuthorised():
		return "Not authorised", 401
	return jsonify(MotionEvent.GetMotionEvents(roomId))

#----------------------------------------------------------------------------------------------

@app.route("/api/getAwsIotWSS")
def getAwsIotWSS():
	if not IsAuthorised():
		return "Not authorised", 401
	time = datetime.utcnow()
	date_stamp = time.strftime('%Y%m%d')
	amzdate = date_stamp + 'T' + time.strftime('%H%M%S') + 'Z'
	service = 'iotdevicegateway'
	canonicalUri = '/mqtt'
	algorithm = 'AWS4-HMAC-SHA256'
	credentialScope = date_stamp + '/' + Config.aws_region + '/' + service + '/' + 'aws4_request'

	canonicalQuerystring = 'X-Amz-Algorithm=' + algorithm
	canonicalQuerystring += '&X-Amz-Credential=' + quote_plus(Config.aws_access_key + '/' + credentialScope)
	canonicalQuerystring += '&X-Amz-Date=' + amzdate
	canonicalQuerystring += '&X-Amz-SignedHeaders=host'

	canonicalHeaders = 'host:' + Config.aws_endpoint + '\n'
	payloadHash = SigV4Utils.sha256('')
	canonicalRequest = 'GET' + '\n' + canonicalUri + '\n' + canonicalQuerystring + '\n' + canonicalHeaders + '\nhost\n' + payloadHash
	stringToSign = algorithm + '\n' +  amzdate + '\n' +  credentialScope + '\n' +  SigV4Utils.sha256(canonicalRequest)
	signingKey = SigV4Utils.getSignatureKey(Config.aws_secret_key,date_stamp,Config.aws_region,service)
	signature = SigV4Utils.sign(signingKey, stringToSign)

	canonicalQuerystring += '&X-Amz-Signature=' + signature
	return ('wss://' + Config.aws_endpoint + canonicalUri + '?' + canonicalQuerystring),200

#----------------------------------------------------------------------------------------------
#PUBLIC DASHBOARD API CALLS
@app.route("/api/setCardID", methods = ['POST'])
def setUserCardID():
	if not IsAuthenticated():
		return "Not authorised", 401
	cardID = request.form.get("cardID")
	userID = session['UserId']
	if cardID == "" or cardID == None:
		return "Error, A card ID cannot be blank", 400
	result = User.addCardId(cardID, userID)
	if result == False:
		return "Error, A card with this ID already exists",400
	return "success"

@app.route("/api/getUserAccessRequests")
def getUserAccessRequestsWithoutUserID():
	if not IsAuthenticated():
		return "Not authorised", 401
	UserId = session['UserId']
	result = AccessRequest.getUserAccessRequests(UserId)
	return jsonify(result)

@app.route("/api/requestNewAccess", methods = ['POST'])
def requestNewAccess():
	if not IsAuthenticated():
		return "Not authorised", 401
	roomID = request.form.get("roomID")
	userID = session['UserId']
	status = AccessRequest.checkIfAlreadyRequested(roomID, userID)
	if status == 0 or status == 3:
		result = AccessRequest.requestNewAccess(roomID, userID)
		if result is False:
			return "Error, something went wrong when inserting value", 400
	elif status == 1:
		return "Error, Your request for this room is already approved", 400
	elif status == 2:
		return "Error, Your last request has not passed 10 minutes", 400
	elif status == 4:
		return "Error, Your request is pending", 400
	return "Successfully requested for access for Room"

@app.route("/api/getUserAccessRights")
def getUserAccessRightsWithoutUserID():
	if not IsAuthenticated():
		return "Not authorised", 401
	UserId = session['UserId']
	result = AccessRight.getUserAccessRights(UserId)
	return jsonify(result)

@app.route("/api/LatestEnviroInfo/<int:roomID>")
def GetRoomLatestEnviroInfo(roomID):
	if not IsAuthenticated():
		return "Not authorised", 401
	result = EnviroInfo.GetLatestEnviroInfo(roomID)
	return jsonify(result)

#----------------------------------------------------------------------------------------------
# ADMIN ACCESS RIGHTS APPROVAL REQUESTS APIs

@app.route("/api/getPendingRequests")
def getPendingAccessRequests():
	if not IsAuthorised():
		return "Not authorised", 401
	result = AccessRequest.getAllPendingRequests()
	return jsonify(result)

@app.route("/api/getCompletedRequests")
def getCompletedRequests():
	if not IsAuthorised():
		return "Not authorised", 401
	result = AccessRequest.getCompletedRequests()
	return jsonify(result)

@app.route("/api/approveAccessRequest/<int:requestID>", methods = ['POST'])
def updateRequestApprovalStatus(requestID):
	if not IsAuthenticated():
		return "Not authorised", 401
	approval = request.form.get("approval")
	print(approval)
	result = AccessRequest.updateRequestApprovalStatus(requestID, approval)
	return jsonify(result)

#----------------------------------------------------------------------------------------------
# WhatsAPP Receive and handle incoming messages

@app.route("/api/whatsapp",methods = ['POST'])
def handleWhatsApp():
    number = request.form['From']
    message_body = request.form['Body']
    WhatsAppBot.createMessage(message_body,number)
    return "successfully sent message"

#----------------------------------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
