from flask import Flask, request, jsonify, json
from core.routing import createResponse
from core.user import User
from core.users import Users
from core.controller import Controller
from dotenv import load_dotenv

load_dotenv()

controller = Controller()
app = Flask(__name__)
users = Users(controller)

# API to create runtime users dataset validating if the users are active on the game or not
# The program must validate if the user has actions every 15 minutes,
# if not, remove it automatically from the dataset


@app.route('/user-join', methods=["POST"])
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


@app.route('/get-users', methods=["GET"])
def getUsers():
    # returns a set of active users
    return createResponse(200, users.getActiveUsersJSON(), None)


@app.route('/user-exit', methods=["POST"])
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


@app.route('/daily-logs', methods=["GET"])
def dailyLogs():
    return createResponse(200, users.getTimeLogs(), None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
