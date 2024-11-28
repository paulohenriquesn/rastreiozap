from src.crons.update_tracks import update_tracks
import schedule
import time

schedule.every(10).seconds.do(update_tracks)

while True:
    schedule.run_pending()
    time.sleep(1)
