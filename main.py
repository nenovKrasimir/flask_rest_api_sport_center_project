from flask_apscheduler import APScheduler

import config
from db import db
from managers.admin_access_managers.delivery_manager import DeliveryGuyManger

scheduler = APScheduler()

if __name__ == "__main__":
    app = config.create_app(config.DevelopmentConfig)

    with app.app_context():
        db.init_app(app)
        scheduler.init_app(app)
        scheduler.add_job(id="delete", func=lambda: (app.app_context().push(), DeliveryGuyManger.move_delivered_packages()), trigger='interval', minutes=1)

        scheduler.start()
        app.run()
