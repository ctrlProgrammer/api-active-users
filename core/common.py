from time import time
from flask import jsonify


def getTime():
    return round(time() * 1000)


def createResponse(code, data, message):
    return jsonify({
        'code': code,
        "data": data,
        "message": message,
    })
