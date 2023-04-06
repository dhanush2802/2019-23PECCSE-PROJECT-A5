from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from . import forms
from . import models
import numpy as np
import joblib

model = joblib.load('C:/Users/SPIRO15/Desktop/co2 new/Deploy/latest/new/RFC.pkl')

# Create your views here.
def home_view(request):
    if request.method == "POST":
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)
        name = request.POST['user']
        if name == "user":
            user = authenticate(request, username=username, password=password)
            #print(user)
            if user is not None:
                auth_login(request, user)
                return render(request, 'new/index.html')
            else:
                msg = 'Invalid Credentials'
                form = AuthenticationForm(request.POST)
                return render(request, 'new/user_login.html', {'form': form, 'msg': msg})
        else:
            user = authenticate(request, username=username, password=password)
            #print(user)
            if user is not None:
                auth_login(request, user)
                model = models.UserPredictDataModel.objects.latest('id')
                form = forms.FeedForm(request.POST)
                #print(model)
                return render(request, 'new/last.html', {'model':model,'form':form})
            else:
                msg = 'Invalid Credentials'
                form = AuthenticationForm(request.POST)
                return render(request, 'new/user_login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
    return render(request, 'new/user_login.html', {'form': form})


def login(request):
    form = AuthenticationForm()
    return render(request, 'new/login.html', {'form': form})

def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #print('saving')
            form.save()
            return render(request, 'new/user_signup.html', {'msg':"Registered Successfully",'form':form})
    else:
        form = UserCreationForm()
    return render(request, 'new/user_signup.html',{'form':form})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #print('saving')
            form.save()
            return render(request, 'new/user_signup.html', {'msg':"Registered Successfully",'form':form})
    else:
        form = UserCreationForm()
    return render(request, 'new/signup.html',{'form':form})




def predict_view(request):
    if request.method == 'POST':
        print('IF')
        fieldss = ['Engine_Size','Cylinders','Transmission','Fuel_Type','FC_City','FC_Hwy','FC_Comb_km','FC_Comb_mpg']
        form = forms.UserPredictDataForm(request.POST)
        features = []
        for i in fieldss:
            info = request.POST[i]
            features.append(info)
        final_features = [np.array(features)]
        #print(final_features)
        prediction = model.predict(final_features)
        #print(prediction)
        output = prediction[0]
        if output == 0:
            output='THE CO2 EMMISIONS ARE VERY LOW RATE CONTENTS IN AIR '
            a = 'PREVENTIONS : No Need Preventions'
        elif output == 1:
            output='THE CO2 EMMISIONS ARE LOW RATE CONTENTS IN AIR'
            a = 'PREVENTIONS : No Need Preventions'
        elif output == 2:
            output='THE CO2 EMMISIONS ARE MEDIUM OR MODERATE RATE CONTENTS IN AIR'
            a = 'PREVENTIONS : There are both nature-based and technology-based approaches to CDR. The two main strategies for removing carbon from the atmosphere are tree planting and forest restoration or conservation efforts, and direct air capture (DAC), according to a World Resources Institute report released.'
        elif output == 3:
            output='THE CO2 EMMISIONS ARE HIGH RATE CONTENTS IN AIR'
            a = 'PREVENTIONS : Avoiding the use of single occupancy vehicles through carpooling, riding transit, biking or walking to work and errands is one way to reduce emissions from transportation.'
        elif output == 4:
            output='THE CO2 EMMISIONS ARE VERY HIGH RATE CONTENTS IN AIR'
            a = 'PREVENTIONS : Switch it Off. Turn off the lights when natural light is sufficient and when you leave the room, Climate Control, Wasteful Windows, Minimize Plug Load, Phantom Power, Give it a Rest, Take the Stairs, Loaded Laundry.'
        print(features)
        print(output)
        if form.is_valid():
            print('saving')
            form.save()
        ob = models.UserPredictDataModel.objects.latest('id')
        ob.CO2_Emission_Rating = output
        ob.save()
        return render(request, 'new/index.html', {'prediction_text1':output,'prediction_text2':a, 'form':form})
    else:
        print('ELSE')
        form = forms.UserPredictDataForm(request.POST)
    return render(request, 'new/index.html', {'form':form})



def view_all(request):
    model = models.UserPredictDataModel.objects.all()
    #print(model)
    return render(request, 'new/all.html', {'model':model})



def view_last(request):
    if request.method == "POST":
        form = forms.FeedForm(request.POST)
        #print('form',form)
        if form.is_valid():
            form.save()
            model = models.UserPredictDataModel.objects.latest('id')
            #print(model)
            return render(request, 'new/last.html', {'model':model,'msg':'Feedback sent'})
        else:
            model = models.UserPredictDataModel.objects.latest('id')
            return render(request, 'new/last.html', {'model':model,'msg':'Feedback Error'})
    else:
        form = forms.FeedForm()
        model = models.UserPredictDataModel.objects.latest('id')
    return render(request, 'new/last.html', {'model':model,'form':form})
        


def feedback(request):
    model = models.FeedModel.objects.latest('id')
    return render(request, 'new/feedback.html', {'model':model})

def apredict(request):
    return render(request, 'new/index.html')

def logout_view(request):
    logout(request)
    return redirect('home_view')

