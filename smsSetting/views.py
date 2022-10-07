from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import SmsModle
from .serializer import SmsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from theme.models import Member
from django.contrib import messages
from threading import Thread
from theme.gym_scheduler.smsGymScheduler import sendMessageToUser,sendMessageToAll
# Create your views here.
def smshistory(request):
    if request.method=="POST":
        if request.POST.get('add-sms'):
            SmsModle.objects.create(smsFor=request.POST.get('sms-for'),smsModule=request.POST.get('sms-module'),smsText=request.POST.get('sms-text')).save()
            return HttpResponseRedirect(reverse('smshistory'))
        if request.POST.get('sms-delete'):
            SmsModle.objects.filter(id=request.POST.get('sms-id')).delete()
            return HttpResponseRedirect(reverse('smshistory'))
        if request.POST.get('send-message'):
            name=Member.objects.filter(id=request.POST.get('model-member-id')).first().member_name
            number=Member.objects.filter(id=request.POST.get('model-member-id')).first().member_contact
            message=request.POST.get('model-smstext')
            try:
                if sendMessageToUser(name,number,message)==200:
                    messages.success(request, 'Message sent successfully')
                    return HttpResponseRedirect(reverse('addMember'))
                else:
                    messages.error(request, 'Message not sent')
                    return HttpResponseRedirect(reverse('addMember'))
            except:
                messages.error(request, 'Message not sent')
                return HttpResponseRedirect(reverse('addMember'))
        if request.POST.get("send-message-toall"):
            message=request.POST.get('model-smstext-all')
            status=request.POST.get('model-status')
            print(message,status)
            try:
                Thread(target=sendMessageToAll, args=(message,status)).start()
                messages.success(request, 'Message sent successfully')
                return HttpResponseRedirect(reverse('addMember'))
            except Exception as e:
                print(e)
                messages.error(request, f'Message not sent{e}')
                return HttpResponseRedirect(reverse('addMember'))
    else:
        return render(request, 'smshistory.html',
        {'sms_list':SmsModle.objects.all()})
        

@api_view(['GET'])
def smsForsearch(request):
    if request.method == 'GET':
        try:
            module=request.GET.get('module')
            sms_list = SmsModle.objects.filter(smsModule=module)
            serializer = SmsSerializer(sms_list, many=True)
            return Response(serializer.data)
        except SmsModle.DoesNotExist:
            return Response("No sms module data found")
    else:
        return Response("Invalid request method")
    
@api_view(['GET'])
def searchMessage(request):
    if request.method == 'GET':
        try:
            module=request.GET.get('module')
            sms_for=request.GET.get('sms')
            sms_list = SmsModle.objects.filter(smsModule=module).filter(smsFor=sms_for)
            print("hellow",sms_list)
            return Response(SmsSerializer(sms_list,many=True).data)
        except Exception as e:
            print(e)
            return Response("No sms module data found")
    else:
        return Response("Invalid request method")