import Monitoring.Health_Monitor as Health_Monitor
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

sched = BackgroundScheduler()

month = str(datetime.now().month)
day = str(datetime.now().day)

filename = str("0"+month+"."+day+".log")

datapath = str("./Hum_Temp/"+filename)

@sched.scheduled_job('interval', seconds=5)
def timed_job():
    Health_Monitor.Apparatus_Monitor(sensordata=datapath,plotpath="./Plots/",lasttime="./Monitoring/lastrun.txt")
	
sched.start()
input("Press Enter to shutdown Monitoring ")
sched.shutdown()
print("Monitoring code shutdown.")