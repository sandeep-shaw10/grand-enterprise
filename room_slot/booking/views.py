from django.shortcuts import render,redirect
from .models import Contact
from .models import Rooms,Booking,Apartment,BookingApartment
from login.models import Customer
from django.contrib import messages
from django.http import HttpResponse
from datetime import date

def index(request):
    return render(request,'booking/index.html',{})

def contact(request):
    if request.method=="GET":
     return render(request,"contact/contact.html",{})
    else:
     username=request.POST['name']
     email=request.POST['email']
     message=request.POST['message']
     data=Contact(name=username,email=email,message=message)
     data.save()
     return render(request,"contact/contact.html",{'message':'Thank you for contacting us.'})

def book(request):
    if request.method=="POST":
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']
        category = request.POST['category']
        print(start_date,end_date,category)
        if(start_date > end_date):
            return redirect('index')
        else:
            request.session['start_date']=start_date
            request.session['end_date']=end_date
            checkin = date(int(start_date[:4]),int(start_date[5:7]),int(start_date[8:]))
            checkout = date(int(end_date[:4]),int(end_date[5:7]),int(end_date[8:]))
            no_of_days=(checkout-checkin).days + 1
            if(category=="Rooms"):
                data=Rooms.objects.filter(is_available=True,no_of_days_advance__gte=no_of_days,start_date__lte=start_date)
                request.session['no_of_days']=no_of_days
                return render(request,'booking/book.html',{'data':data})
            else:
                data1=Apartment.objects.filter(is_available=True,no_of_days_advance__gte=no_of_days,start_date__lte=start_date)
                request.session['no_of_days']=no_of_days
                return render(request,'booking/book.html',{'data1':data1})
    else:
        return redirect('index')

def book_now(request,category,id):
    if request.session.get("username",None) and request.session.get("type",None)=='customer':
        if request.session.get("no_of_days",1):
            no_of_days=request.session['no_of_days']
            start_date=request.session['start_date']
            end_date=request.session['end_date']
            if(category=="room"):
                request.session['room_no']=id
                data=Rooms.objects.get(room_no=id)
            else:
                request.session['apartment_no']=id
                data=Apartment.objects.get(apartment_no=id)                
            bill=data.price*int(no_of_days)
            request.session['bill']=bill
            roomManager=data.manager.username
            return render(request,"booking/book-now.html",{"no_of_days":no_of_days,"room_no":id,"data":data,"bill":bill,"roomManager":roomManager,"start":start_date,"end":end_date,"category":category})
        else:
            return redirect("index")
    else:
        next="book-now/"+id
        return redirect('user_login')

def book_confirm(request):
    room_no=request.session['room_no']
    start_date=request.session['start_date']
    end_date=request.session['end_date']
    username=request.session['username']
    user_id=Customer.objects.get(username=username)
    room=Rooms.objects.get(room_no=room_no)
    amount=request.session['bill']
    data=Booking(room_no=room,start_day=start_date,end_day=end_date,amount=amount,user_id=user_id)
    data.save()
    room.is_available=False
    room.save()
    del request.session['start_date']
    del request.session['end_date']
    del request.session['bill']
    del request.session['room_no']
    messages.info(request,"Room has been successfully booked")
    return redirect('user_dashboard')

def book_confirm1(request):
    apartment_no=request.session['apartment_no']
    start_date=request.session['start_date']
    end_date=request.session['end_date']
    username=request.session['username']
    user_id=Customer.objects.get(username=username)
    room=Apartment.objects.get(apartment_no=apartment_no)
    amount=request.session['bill']
    data=BookingApartment(apartment_no=room,start_day=start_date,end_day=end_date,amount=amount,user_id=user_id)
    data.save()
    room.is_available=False
    room.save()
    del request.session['start_date']
    del request.session['end_date']
    del request.session['bill']
    del request.session['apartment_no']
    messages.info(request,"Apartment has been successfully booked")
    return redirect('user_dashboard')

def cancel_room(request,id):
    data=Booking.objects.get(id=id)
    room=data.room_no
    room.is_available=True
    room.save()
    data.delete()
    return HttpResponse("Booking Cancelled Successfully")

def delete_room(request,id):
    data=Rooms.objects.get(id=id)
    manager=data.manager.username
    if manager==request.session['username']:
        data.delete()
        return HttpResponse("You have deleted the room successfully")
    else:
        return HttpResponse("Invalid Request")


            



    
