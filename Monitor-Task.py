import Monitoring.Health_Monitor as Health_Monitor
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import shutil

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
plots_move = str(plotpath+"0"+month+"."+day)
if os.path.exists(plots_move) == True:
    plots_movepath = str(plots_move + "-01")
else:
    plots_movepath = plots_move
    
os.makedirs(plots_movepath)
shutil.move(str(plotpath+"Humidity.png"), str(plots_movepath+"Humidity.png"))
shutil.move(str(plotpath+"Temperature.png"), str(plots_movepath+"Temperature.png"))

print("Monitoring code shutdown.")