from Shared.Database import db
from Shared.helpers import data_to_json
from Shared.Room import Room
import datetime
class AccessRequest:
    @staticmethod
    def getUserAccessRequests(UserId):
        db_results = db.query("SELECT r.RoomName, ar.DateRequested, ar.IsApproved FROM access_request ar "
        "JOIN rooms r on ar.RoomId = r.Id where ar.UserId = {}".format(UserId))
        if db_results == None or len(db_results) <= 0:
            return {}
        return db_results

    @staticmethod
    def checkIfAlreadyRequested(roomID, userID):
        currentTime = datetime.datetime.now()
        db_results = db.query("SELECT * from access_request where userID = {} and roomID = {}".format(userID, roomID))
        #have not created a request to this room
        if db_results == None or len(db_results) <= 0:
            return 0
        result = db_results[0]
        status = result['IsApproved']
        if status is not None:
            if status == 1:
                return 1
            if status == 0:
                approvalDelay = result['DateRequested'] + datetime.timedelta(minutes = 10)
                if currentTime < approvalDelay:
                    return 2
                return 3
        else:
            return 4

    @staticmethod
    def requestNewAccess(roomID, userID):
        currentTime = datetime.datetime.now()
        id = db.insert("insert into access_request(userid, roomid, DateRequested) values ({}, {},'{}')"
        .format(userID, roomID, currentTime))
        return id

    @staticmethod
    def getAllPendingRequests():
        db_results = db.query("SELECT ar.Id, ud.Username, r.RoomName, ar.DateRequested, ar.IsApproved FROM access_request ar " +
        "JOIN rooms r on ar.RoomId = r.Id " +
        "JOIN users ud on ar.UserId = ud.Id where ar.IsApproved is null")
        if db_results == None or len(db_results) <= 0:
            return {}
        return db_results

    @staticmethod
    def getCompletedRequests():
        db_results = db.query("SELECT ud.Username, r.RoomName, ar.DateRequested, ar.IsApproved FROM access_request ar " +
        "JOIN rooms r on ar.RoomId = r.Id " +
        "JOIN users ud on ar.UserId = ud.Id where ar.IsApproved is not null")
        if db_results == None or len(db_results) <= 0:
            return {}
        return db_results

    @staticmethod
    def updateRequestApprovalStatus(requestID, approval):
        if (requestID != None and approval != None):
            result = db.update("update access_request set IsApproved =  {} where Id = {}".format(approval, requestID))
            if result is True and approval == '1':
                requestObject = db.query("SELECT roomID, UserId from access_request where id = {}".format(requestID))
                result = requestObject[0]
                id = db.insert("insert into access_rights(RoomId, UserId) values({}, {})".format(result['roomID'], result['UserId']))
            return result
        else:
            return False
