from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import logging
import datetime
from .models import parkingFee

def index(request):
    return render(request,'index.html')

def calculate(request):
    timeIn = request.POST.get("datetime1", None).replace('T', ' ')
    timeOut = request.POST.get("datetime2", None).replace('T', ' ')
    strmode = str(request.POST.get("usedVehicle", None))
    rndr = {}
    strDuration = ""
    fee = 0
    if timeIn and timeOut:
        try:
            dateTime_in = datetime.datetime.strptime(timeIn, '%Y-%m-%d %H:%M:%S')
        except:
            dateTime_in = datetime.datetime.strptime(timeIn, '%Y-%m-%d %H:%M')
        try:
            dateTime_out = datetime.datetime.strptime(timeOut, '%Y-%m-%d %H:%M:%S')
        except:
            dateTime_out = datetime.datetime.strptime(timeOut, '%Y-%m-%d %H:%M')
        if strmode == "Motorcycle" or strmode == "empMotor":
            duration = (dateTime_out.day - dateTime_in.day)+1
            fee = duration * parkingFee.objects.get(mode=strmode).fee
            if strmode == "empMotor":
                fee = fee - (fee*.2)
            strDuration = str(duration) + " Day(s)"
        else:
            duration = dateTime_out - dateTime_in
            succedingFee = parkingFee.objects.get(mode = strmode).succeedingFee
            fee = parkingFee.objects.get(mode = strmode).fee
            totalHours = ((duration.total_seconds()/60)/60)
            if totalHours >= 0:
                totalHours = totalHours-2
                if totalHours > 0:
                    fee = round((succedingFee*totalHours),2)
                strDuration = str(duration)
            else:
                fee = 0
    if fee <= 0:
        rndr["fee"] = "INVALID INPUT"
    else:
        rndr["fee"] = "PHP " + str(fee)
        rndr["duration"] = strDuration
    return render(request,'index.html',rndr)

# Create your views here.
