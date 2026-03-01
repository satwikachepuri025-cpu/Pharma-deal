import schedule
import time
from app.main import run_pipeline


def start_scheduler():
    print("📅 Scheduler started. Waiting for scheduled runs...")
    schedule.every().day.at("09:00").do(run_pipeline)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    start_scheduler()