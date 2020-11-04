from Principal.Main import job
import schedule

#schedule.every(10).seconds.do(job)
schedule.every().day.at("00:00").do(job)


while True:
    schedule.run_pending()