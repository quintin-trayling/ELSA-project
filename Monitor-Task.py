import Monitoring.Health_Monitor as Health-Monitor
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

sched = BackgroundScheduler()

month = datetime.now.month
day = datetime.now.day

filename = str(month+"-"+day+".log")

datapath = str("/Hum_Temp/"+filename)

@sched.scheduled_job('interval', seconds=5)
def timed_job():
    Health-Monitor.ApparatusMonitor(sensordata=datapath,plotpath="/Plots/",lasttime="lastrun.txt")
	
sched.start()
input("Press Enter to shutdown Monitoring ")
sched.shutdown()
print("Monitoring code shutdown.")