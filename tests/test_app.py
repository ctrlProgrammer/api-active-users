from json import dumps
from flask import testing
from json import loads


def test_app_request(client: testing.FlaskClient):
    # Validate application response
    # it must include response code, message and data
    response = loads(client.get("/get-users").data.decode("utf-8"))
    assert "code" in response and "message" in response and "data" in response


def test_get_users(client: testing.FlaskClient):
    # Validate the get users request without adding any user
    # the initial users dataset must be empty
    response = loads(client.get("/get-users").data.decode("utf-8"))

    assert "data" in response and type(
        response["data"]) is list and len(response["data"]) == 0


def test_user_join(client: testing.FlaskClient):
    # Validate if the user join requests works fine
    # The response should be a normal request with code, message and data
    # In this case the code is 200 and the rest are null or None

    response = client.post("/user-join", json={
        "wallet": "0x1"
    })

    assert "code" in response and "message" in response and "data" in response and response[
        "code"] == 200


# def test_user_join_negative(client: testing.FlaskClient):
#     # Validate if the user join requests works fine when an user send invalid data in the request
#     # Error request, invalid request args

#     response = loads(client.post("/user-join", data={
#         "user": "0x1"
#     }).data.decode("utf-8"))

#     assert "code" in response and "message" in response and "data" in response and response[
#         "code"] == 400


# def test_user_join_data(client: testing.FlaskClient):
#     # Validate if the app store a new users when they call user join
#     # The response of get users must have a new user on the response
#     # Also the new users should has the same wallet

#     response = loads(client.get("/get-users").data.decode("utf-8"))

#     print(response)
