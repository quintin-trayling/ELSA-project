import os
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from discord_webhooks import DiscordWebhooks
import numpy as np
import matplotlib.pyplot as plt

sender_email = "elsa.notification@gmail.com"

Webhook_URL = "https://discordapp.com/api/webhooks/676912729662947341/Zwc1g74r1Z05zPw3b6Joul08h2m8io4Fvz2cMxBSUZcpk5lVS_6VNdIpkDP2dKKteAe7"

webhook = DiscordWebhooks(Webhook_URL)

emails = ["15qjt@queensu.ca","15anjh@queensu.ca","15yd29@queensu.ca","15fh23@queensu.ca"]

Server = "smtp.gmail.com"
Port = 465  # For SSL

def Email_Sender(password,image1,image2,issuecode):

    temp_data = open(image1, 'rb').read()
    humid_data = open(image2, 'rb').read()
        
    msg = MIMEMultipart()
    msg['Subject'] = 'ELSA Monitoring Software Alert'
    msg['From'] = sender_email
    
    if issuecode == 0:
        reason = "Temperature"
    elif issuecode == 1:
        reason = "Humidity"
    elif issuecode == 2:
        reason = "Temperature and Humidity"
    
    text = MIMEText("The automatic monitoring software for the Temperature and Humidity of the ELSA apparatus detected a significant change in the "
                   + reason + " of the apparatus. The Temperature and Humidity plots are attached for manual review.")
    msg.attach(text)
    img_temp = MIMEImage(temp_data, name=os.path.basename(image1))
    msg.attach(img_temp)
    img_humid = MIMEImage(humid_data, name=os.path.basename(image2))
    msg.attach(img_humid)

    text = msg.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(Server, Port, context=context) as server:
        server.login(sender_email, password)
        msg['To'] = emails[0]
        receiver_email = emails[0]
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    discord_msg = ("@everyone The ELSA Automatic monitoring script has detected a significant change in temperature or humidity at " 
                   + str(dt_string) + ". Check email for further details.")
    
    webhook.set_content(content=discord_msg)
    webhook.send()
    return 1

def Write_Datetime(filename,datetime):
    with open(filename, 'r+') as f:
        text = f.read()
        text = str(datetime)
        f.seek(0)
        f.write(text)
        f.truncate()

def Apparatus_Monitor(sensordata,plotpath,lasttime,temp_bounds=[-18,-12],humid_thresh = 0.05):
    c_dt = datetime.now()
    datetime_int = c_dt.second + c_dt.minute*60 + c_dt.hour*60*60 + c_dt.day*60*60*24
    lastrun = float(np.loadtxt(lasttime))
    
    if datetime_int > lastrun+60:
        can_alert = True
    else:
        can_alert = False
    
    humid_data,temp_data = np.loadtxt(sensordata,delimiter=',',skiprows=2,unpack=True)
    t0 = 28800
    time_data = np.arange(0,5*len(humid_data)+1,5)
    password = "10Icicles"
    
    temppath = str(plotpath+"Temperature.png")
    humidpath = str(plotpath+"Humidity.png")
    
    plt.plot(time_data,temp_data,'r-',label="Temperature")
    plt.xlabel("Runtime (s)")
    plt.ylabel("Temperature (C)")
    plt.legend()
    plt.savefig(temppath)
    
    plt.close()
    
    plt.plot(time_data,humid_data,'b-',label="Humidity")
    plt.xlabel("Runtime (s)")
    plt.ylabel("Humidity")
    plt.legend()
    plt.savefig(humidpath)
    
    plt.close()
    
    temp_alert = 0
    humid_alert = 0
    
    if temp_data[-1] < temp_bounds[0] or temp_data[-1] > temp_bounds[1]:
        temp_alert = 1
    else:
        temp_alert = 0
    
    humid_mean = np.mean(humid_data)
    if humid_data[-1] < (1-humid_thresh)*humid_mean or humid_data[-1] > (1+humid_thresh)*humid_mean:
        humid_alert = 1
    else:
        humid_alert = 0
    
    if can_alert == True:
        if temp_alert == 1 and humid_alert == 1:
            Email_Sender(password,temppath,humidpath,2)
            Write_Datetime(lasttime,datetime_int)
        elif temp_alert == 1 and humid_alert == 0:
            Email_Sender(password,temppath,humidpath,0)
            Write_Datetime(lasttime,datetime_int)
        elif temp_alert == 0 and humid_alert == 1:
            Email_Sender(password,temppath,humidpath,1)
            Write_Datetime(lasttime,datetime_int)
        else:
            print("No issues found")
    
    return 1