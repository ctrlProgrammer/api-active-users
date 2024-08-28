from flask import jsonify


def createResponse(code, data, message):
    return jsonify({
        'code': code,
        "data": data,
        "message": message,
    })
