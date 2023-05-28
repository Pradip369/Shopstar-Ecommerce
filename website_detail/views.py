from django.shortcuts import render
from .models import TermandCondition

def PrivacyPolicy(request):
    pp = TermandCondition.objects.all().order_by('-id')[0:1]
    return render(request,'site_doc/privacy policy.html',{'pp':pp})


def Termandcondition(request):
    tc = TermandCondition.objects.all().order_by('-id')[0:1]
    return render(request,'site_doc/term and condition.html',{"tc":tc})

def Disclaimer(request):
    dc = TermandCondition.objects.all().order_by('-id')[0:1]
    return render(request,'site_doc/disclaimer.html',{"dc":dc})