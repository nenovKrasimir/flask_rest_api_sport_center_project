import threading
import time
from concurrent.futures import ThreadPoolExecutor

import schedule

import config
from db import db
from managers.admin_access_managers.delivery_manager import DeliveryGuyManger


def run_schedule():
    with ThreadPoolExecutor(max_workers=1) as executor:
        while True:
            schedule.run_pending()
            time.sleep(1)
            executor.submit(DeliveryGuyManger.move_delivered_packages)


if __name__ == "__main__":
    app = config.create_app(config.DevelopmentConfig)
    with app.app_context():
        db.init_app(app)

    schedule.every(5).minutes.do(DeliveryGuyManger.move_delivered_packages)

    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

    app.run()
