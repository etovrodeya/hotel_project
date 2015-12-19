from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,CreateView
from .models import Booking,Contract,Service_order,Room,Service
from mypage.models import Company,MpUser
from .forms import BookingForm,ServiceOrderForm
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.list import ListView
from django import forms
from django.forms.fields import ChoiceField
import datetime
from django.utils.timezone import utc


class BookingView(CreateView):
    template_name='bill/booking.html'
    model=Booking
    form_class = BookingForm
    
    def form_valid(self, form):
        if form.instance.contract is not None:
            contract=Contract.objects.get(name=form.instance.contract)
            if contract.company is not None:
                if contract.company==self.request.user.company:
                    form.instance.person = self.request.user
                    form.instance.company=self.request.user.company
                    form.instance.is_delete=True
                    return super(BookingView, self).form_valid(form)
                else:
                    return HttpResponse('Выбранный контракт не подходит для вышей компании.<p><a href="/booking/">Вернуться на страницу бронирования</a>')
        else:
            form.instance.person = self.request.user
            form.instance.is_delete=True
            return super(BookingView, self).form_valid(form)

def ConfirmtheBookingView(request,booking_id):
    args={}
    record=Booking.objects.get(pk=booking_id)
    date=record.e_date-record.s_date
    if record.company is not None:
        price=(record.room.per_night*date.days)-((record.room.per_night*date.days)*(record.contract.booking_discount/100))
    else:
        price=(record.room.per_night*date.days)
    args['price']=price
    args['message']="Цена бронирования номера"
    return render(request,'bill/confbooking.html',args)

def ValidBooking(request,booking_id):
    if request.user.is_authenticated():
        user=MpUser.objects.get(pk=request.user.id)
        record=Booking.objects.get(pk=booking_id)
        date=record.e_date-record.s_date
        nowtime= datetime.datetime.utcnow().replace(tzinfo=utc)
        if record.s_date<nowtime:
            return HttpResponse('Данную бронь активировать невозможно, т.к дата заезда уже прошла.<p><a href="/mypage/mybookings/">Вернуться на страницу просмотра броней</a>')
        if record.company is not None:
            price=(record.room.per_night*date.days)-((record.room.per_night*date.days)*(record.contract.booking_discount/100))
        else:
            price=(record.room.per_night*date.days)
        sbookings=Booking.objects.filter(s_date__range=(record.s_date,record.e_date))
        ebookings=Booking.objects.filter(e_date__range=(record.s_date,record.e_date))
        if sbookings.filter(is_delete=False).exists() or ebookings.filter(is_delete=False).exists():
            record.is_delete=True
            record.save()
            return HttpResponse('Данный номер уже имеет активную бронь в указаном промежутке дат.<p><a href="/mypage/mybookings/">Вернуться на страницу просмотра броней</a>')
        else:
            record.price=price
            user.total_money=user.total_money-record.price
            record.is_delete=False
            record.save()
            user.save()
            return HttpResponseRedirect("/mypage/mybookings/")
    else:
        return HttpResponseRedirect("/login/")

def DeleteBooking(request,booking_id):
    if request.user.is_authenticated():
        user=MpUser.objects.get(pk=request.user.id)
        nowtime= datetime.datetime.utcnow().replace(tzinfo=utc)
        record=Booking.objects.get(pk=booking_id)
        diff=record.s_date-nowtime
        if diff.days<7:
            return HttpResponse('Данное действие невозможно, т.к до даты заезда осталось 7 дней или менее.<p><a href="/mypage/mybookings/">Вернуться на страницу просмотра броней</a>')
        else:
            if not record.is_delete:
                user.total_money=user.total_money+record.price
                record.is_delete=True
                record.save()
                user.save()
            return HttpResponseRedirect("/mypage/mybookings/")
    else:
        return HttpResponseRedirect("/login/")

def FindFreeRoom(request,sdate,edate):
    booking=Booking.objects.filter(s_date__range=(sdate,edate)).filter(e_date__range=(sdate,edate),is_delete=False)
    rooms=Room.objects.all()
    args={}
    freeroom={}
    for room in rooms:
        if not booking.filter(room=room).exists():
            freeroom[room]=room
    args['freeroom']=freeroom.items()
    args['sdate']=sdate
    args['edate']=edate
    return render (request,'bill/freeroom.html',args)

def FindFreeRoomWS(request,sdate,edate,style):
    booking=Booking.objects.filter(s_date__range=(sdate,edate)).filter(e_date__range=(sdate,edate),is_delete=False)
    rooms=Room.objects.all()
    args={}
    freeroom={}
    for room in rooms:
        if not booking.filter(room=room).exists():
            if room.style==style:
                freeroom[room]=room
    args['freeroom']=freeroom.items()
    args['sdate']=sdate
    args['edate']=edate
    return render (request,'bill/freeroom.html',args)

class ServiceOrderView(CreateView):
    template_name='bill/serviceorder.html'
    model=Service_order
    form_class = ServiceOrderForm

    def form_valid(self, form):
        form.instance.person = self.request.user
        form.instance.is_delete=True
        return super(ServiceOrderView, self).form_valid(form)

def ConfirmetheServiceOrderView(request,serviceorder_id):
    args={}
    serviceorder=Service_order.objects.get(pk=serviceorder_id)
    if serviceorder.booking.contract is None:
        price=serviceorder.service.apiece
    else:
        price=serviceorder.service.apiece-(serviceorder.service.apiece*(serviceorder.booking.contract.service_discount/100))
    name=serviceorder.service.name
    args['price']=price
    args['name']=name
    args['message']='Вы действительно хотите заказать услугу:'
    return render (request,'bill/confserviceorder.html',args)

def ValidServiceOrder(request,serviceorder_id):
    if request.user.is_authenticated():
        user=MpUser.objects.get(pk=request.user.id)
        serviceorder=Service_order.objects.get(pk=serviceorder_id)
        if serviceorder.booking.is_delete:
            return HttpResponse('Данное действие невозможно, т.к бронь неактивна.<p><a href="/mypage/myservices/">Вернуться на страницу просмотра заказанных услуг</a>')
        if serviceorder.booking.contract is None and serviceorder.is_delete:
            if serviceorder.booking.person == request.user.id:
                price=serviceorder.service.apiece
                serviceorder.price=price
                serviceorder.is_delete=False
                user.total_money=user.total_money-serviceorder.price
                serviceorder.save()
                user.save()
            else:
                return HttpResponse('Данное действие невозможно, т.к дополнительные услуги может заказывать лишь владелец брони.<p><a href="/mypage/myservices/">Вернуться на страницу просмотра заказанных услуг</a>')
        else:
            if serviceorder.is_delete:
                if serviceorder.booking.person == request.user.id:
                    price=serviceorder.service.apiece-(serviceorder.service.apiece*(serviceorder.booking.contract.service_discount/100))
                    serviceorder.price=price
                    serviceorder.is_delete=False
                    user.total_money=user.total_money-serviceorder.price
                    serviceorder.save()
                    user.save()
                else:
                    return HttpResponse('Данное действие невозможно, т.к дополнительные услуги может заказывать лишь владелец брони.<p><a href="/mypage/myservices/">Вернуться на страницу просмотра заказанных услуг</a>')
        return HttpResponseRedirect("/mypage/myservices/")
    else:
        return HttpResponseRedirect("/login/")

def DeleteServiceOrder(request,serviceorder_id):
    if request.user.is_authenticated():
        user=MpUser.objects.get(pk=request.user.id)
        serviceorder=Service_order.objects.get(pk=serviceorder_id)
        if not serviceorder.is_delete:
            serviceorder.is_delete=True
            user.total_money=user.total_money+serviceorder.price
            serviceorder.save()
            user.save()
        return HttpResponseRedirect("/mypage/myservices/")
    else:
        return HttpResponseRedirect("/login/")

def roomdetail(request,housing,floor,number):
    args={}
    room=get_object_or_404(Room,housing=housing,floor=floor,number=number)
    args['room']=room
    return render(request,'bill/roomdetail.html',args)

def servicelist(request):
    args={}
    services=Service.objects.all()
    args['services']=services
    return render(request,'bill/serviceslist.html',args)
