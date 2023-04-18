import threading
import time

import schedule
from dotenv import dotenv_values
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from managers.admin_access_managers.delivery_manager import DeliveryGuyManger
from resources.routes import routes

config = {**dotenv_values(".env")}

app = Flask(__name__)
app.config.update(config)

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

[api.add_resource(*route) for route in routes]

schedule.every(5).seconds.do(DeliveryGuyManger.move_delivered_packages)


def run_schedule():
    with app.app_context():
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
    app.run()
