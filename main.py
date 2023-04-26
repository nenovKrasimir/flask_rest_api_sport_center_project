from flask_apscheduler import APScheduler

import config
from managers.admin_access_managers.delivery_manager import DeliveryGuyManger

scheduler = APScheduler()
app = config.create_app()

if __name__ == "__main__":
    with app.app_context():
        scheduler.init_app(app)
        scheduler.add_job(id="delete",
                          func=lambda: (app.app_context().push(), DeliveryGuyManger.move_delivered_packages()),
                          trigger='interval', minutes=1)

        scheduler.start()
        app.run()
