from dotenv import dotenv_values
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes

config = {**dotenv_values(".env")}

app = Flask(__name__)
app.config.update(config)

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

[api.add_resource(*route) for route in routes]


if __name__ == "__main__":
    app.run()
