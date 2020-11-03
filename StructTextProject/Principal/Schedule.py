import schedule

def job():
    print("teste")

schedule.every(10).seconds.do(job)


while True:
    schedule.run_pending()