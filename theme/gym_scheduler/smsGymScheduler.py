from apscheduler.schedulers.background import BackgroundScheduler
from threading import Thread
from theme.models import Member
import requests
import datetime as dt
def smsMessage(days):
    english=f"""
Hello and Asalam o Alaikum 
Greetings from Masho Fitness
We sincerely hope that you are enjoying your fitness and health. To continue with it, all you need to do is to renew your membership to stay part of Masho's Fitness as early as possible. 
Your Membership will expire {days}. 
Thank you.
"""
    return english
def sendMessageToAll(message,status):
    try:
        if status=='All':
            for i in Member.objects.all():
                print(sendMessageToUser(i.member_name,i.member_contact, message))
        else:
            for i in Member.objects.filter(active_fee_id__status=status):
                print(sendMessageToUser(i.member_name,i.member_contact, message))
        return 200
    except Exception as e:
        print("sendMessageToAll exception",e)
        return 400

def sendMessageToUser(name,number,message):
    number=number.replace("-", "")
    try:
        return requests.get(f'https://sendpk.com/api/sms.php?api_key=923402601866-e097c210-00f1-4fdf-9318-7e012f796e4a&sender=MashoFitness&mobile={number}&message=Dear {name},{message}').status_code
    except Exception as e:
        print("sendMessageToUser exception",e)
        
def main():
    try:
        if Member.objects.all().exists():
            for i in Member.objects.all():
                print(i.member_name)
                if (i.member_membership_expiry_date-dt.date.today()).days==5:
                    sendMessageToUser(i.member_name,i.member_contact,smsMessage("in 5 days"))
                elif (i.member_membership_expiry_date-dt.date.today()).days==3:
                    sendMessageToUser(i.member_name,i.member_contact,smsMessage("in 3 days"))
                elif (i.member_membership_expiry_date-dt.date.today()).days==1:
                    sendMessageToUser(i.member_name,i.member_contact,smsMessage("in 1 day"))
                elif (i.member_membership_expiry_date-dt.date.today()).days==0:
                    sendMessageToUser(i.member_name,i.member_contact,smsMessage("today"))
    except Exception as e:
        print("checkMemberStarus exception",e)


def fun_call():
    Thread(target=main).start()
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fun_call, 'interval', minutes=1440)
    scheduler.start()