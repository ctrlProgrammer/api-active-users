from flask import request, Blueprint
from core.common import createResponse
from core.user import User
from core.extensions import users

main = Blueprint("main", __name__)


@main.route('/user-join', methods=["POST"])
def userJoin():
    # add new user on the dataset
    # validate if the requests has the correct information and if the user is active
    response = createResponse(400, None, None)

    data = request.get_json()

    if "wallet" not in data:
        return response

    if not users.addNewUser(User(data["wallet"])):
        return createResponse(400, None, "Invalid user")

    return createResponse(200, None, None)


@main.route('/get-users', methods=["GET"])
def getUsers():
    # returns a set of active users
    return createResponse(200, users.getActiveUsersJSON(), None)


@main.route('/user-exit', methods=["POST"])
def userExit():
    # remove user from the dataset
    # it validates if the request has the correct information and validate if the user exists
    response = createResponse(400, None, None)

    data = request.get_json()

    if "wallet" not in data:
        return response

    if not users.removeUser(data["wallet"]):
        return createResponse(400, None, "Invalid user")

    return createResponse(200, None, None)


@main.route('/daily-logs', methods=["GET"])
def dailyLogs():
    return createResponse(200, users.getTimeLogs(), None)
