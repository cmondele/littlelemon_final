from django.http import HttpResponse
from django.shortcuts import render

from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from .forms import BookingForm , BookingDateForm

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
     message=None
     form = BookingForm()
     if request.method == 'POST':
         form = BookingForm(request.POST)
         mmd=str(form['reservation_date'].value())
         form_data={
             'reservation_date':mmd
         }
         matching_instance=Booking.objects.filter(**form_data).first()

         if form.is_valid() and matching_instance is None :
             form.save()
             message="Success We can not Wait to see you!!"
         else:
             message="Failed! Sorry but, we are reserved for this date. Please choose another date"
     context = {'form':form,"message":message}
     return render(request, 'book.html', context)

# Add code for the bookings() view



def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 
def bookings(request):
    form=BookingDateForm()
    date =request.GET.get('date',datetime.today().date())
    bookings=Booking.objects.all()
    booking_json =serializers.serialize('json',bookings)
    return render(request, 'bookings.html',{"bookings":booking_json,'form':form})