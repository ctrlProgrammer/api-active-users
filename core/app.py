from flask import Flask
from core.routes import main


# API to create runtime users dataset validating if the users are active on the game or not
# The program must validate if the user has actions every 15 minutes,
# if not, remove it automatically from the dataset


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=getenv("APP_PORT"))
