from django.shortcuts import render,render_to_response,redirect,get_object_or_404
from django.views.generic import ListView,CreateView
from django.views.generic.edit import FormView
from mypage.forms import LoginForm,RegistrationForm,UserCreationForm,MyPageForm,AddMoneyForm
from django.contrib import auth
from django.http import HttpResponseRedirect,HttpResponse
from .models import MpUser,Company,Contract
from comments.models import Comment,Rating
from bill.models import Booking,Service_order
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.db.models import Count


def home_page(request):
    args={}
    rules=get_object_or_404(Comment,title='Приветствие')
    args['rules']=rules
    comments=Rating.objects.all().order_by('value')[:5]
    args['top']=comments
    return render(request, 'mypage/index.html',args)

def aboutpage(request):
    args={}
    rules=get_object_or_404(Comment,title='О проекте')
    args['rules']=rules
    comments=Rating.objects.all().order_by('value')[:5]
    args['top']=comments
    return render(request, 'mypage/index.html',args)

def login_user(request):
    if request.user.is_authenticated():
        return redirect('views.home_page')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/')

    return render(request, 'mypage/login.html', {'form': form})

@login_required
def profileedit(request):
    message = 'Your Personal Information has been changed. Thanks!'
    message2 = ':('
    form = MyPageForm(instance = request.user)
    if request.method == 'POST':
        form = MyPageForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return render(request, 'mypage/profile_edit.html', {'form': form,'message': message})
        return render(request, 'mypage/profile_edit.html', {'form': form,'message': message2})
    return render(request, 'mypage/profile_edit.html', {'form': form,})


@login_required
def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def registrate(request):
    args={}
    args.update(csrf(request))
    args['form']=UserCreationForm()
    if request.POST:
        newuser_form=UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(
                email=newuser_form.cleaned_data['email'],
                password=newuser_form.cleaned_data['password2']
                )
            auth.login(request,newuser)
            return HttpResponseRedirect('/')
        else:
            args['form']=newuser_form
    return render_to_response('mypage/register.html', args)

def profileview(request):
    return render(request,'mypage/view.html')

def myBookings(request):
    if request.user.is_authenticated():
        args={}
        mybookings=Booking.objects.filter(person=request.user)
        args['mybookings']=mybookings
        return render(request,'mypage/mybookings.html',args)
    else:
        return HttpResponseRedirect("/login/")

def myServices(request):
    if request.user.is_authenticated():
        args={}
        myso=Service_order.objects.filter(person=request.user)
        args['myso']=myso
        return render(request,'mypage/myservices.html',args)
    else:
        return HttpResponseRedirect("/login/")

def companylist(request,cob='0',sdate='2015-01-01 00:00',edate='2051-01-01 00:00'):
    if request.user.is_authenticated():
        if request.user.staff=='manager':
            companylist=Company.objects.all()
            args={}
            args['companylist']=companylist
            cbc={}
            for company in companylist:
                bookings=Booking.objects.filter(company=company).count()
                if bookings>=int(cob):
                    cbc[company]=bookings
            args['cbc']=cbc.items()
            args['sdate']=sdate
            args['edate']=edate
            args['cob']=cob
            return render(request, 'mypage/complist.html',args)
        else:
            return HttpResponse('У данного юзера недостаточно прав для доступа к данной странице.<p> <a href="/">Вернутся на главную страницу</a>')
    else:
        return HttpResponseRedirect("/login/")

def income(request,sdate,edate):
    if request.user.is_authenticated():
        if request.user.staff=='manager':
            args={}
            bookings=Booking.objects.filter(date__range=(sdate,edate)).filter(e_date__range=(sdate,edate),is_delete=False)
            serviceorders=Service_order.objects.filter(date__range=(sdate,edate),is_delete=False)
            incomebookings=0
            incomeserviceorders=0
            for booking in bookings:
                incomebookings+=booking.price
            for serviceorder in serviceorders:
                incomeserviceorders+=serviceorder.price
            args['bookings']=bookings
            args['serviceorders']=serviceorders
            args['ib']=incomebookings
            args['iso']=incomeserviceorders
            args['sdate']=sdate
            args['edate']=edate
            return render(request,'mypage/income.html',args)
        else:
            return HttpResponse('У данного юзера недостаточно прав для доступа к данной странице.<p> <a href="/">Вернутся на главную страницу</a>')

    else:
        return HttpResponseRedirect("/login/")

def newusers(request,sdate,edate):
    if request.user.is_authenticated():
        if request.user.staff=='manager':
            args={}
            newusers=MpUser.objects.filter(register_date__range=(sdate,edate))
            args['sdate']=sdate
            args['edate']=edate
            args['newusers']=newusers
            return render(request,'mypage/newusers.html',args)
        else:
            return HttpResponse('У данного юзера недостаточно прав для доступа к данной странице.<p> <a href="/">Вернутся на главную страницу</a>')
    else:
        return HttpResponseRedirect("/login/")

def userdetail(request,user_id):
    if request.user.is_authenticated():
        if request.user.staff=='manager':
            args={}
            user=get_object_or_404(MpUser,pk=user_id)
            usersbooking=Booking.objects.filter(person=user, is_delete=False)
            usersserviceorders=Service_order.objects.filter(person=user,is_delete=False)
            args['user']=user
            args['ub']=usersbooking
            args['uso']=usersserviceorders
            return render(request,'mypage/userdetail.html',args)
        else:
            return HttpResponse('У данного юзера недостаточно прав для доступа к данной странице.<p> <a href="/">Вернутся на главную страницу</a>')
    else:
        return HttpResponseRedirect("/login/")

def addmoney(request):
    if request.user.is_authenticated():
        user=MpUser.objects.get(pk=request.user.id)
        args={}
        args.update(csrf(request))
        args['form']=AddMoneyForm()
        if request.POST:
            addmoneyform=AddMoneyForm(request.POST, instance = request.user)
            if addmoneyform.is_valid():
                user.total_money=user.total_money+addmoneyform.cleaned_data['total_money']
                user.save()
                return HttpResponseRedirect("/mypage/view/")
        return render_to_response('mypage/addmoney.html', args)
    else:
        return HttpResponseRedirect("/login/")

def compdetail(request,sdate,edate,comp_id):
    comp=get_object_or_404(Company,pk=comp_id)
    if request.user.is_authenticated():
        if request.user.staff=='manager':
            args={}
            comp=get_object_or_404(Company,pk=comp_id)
            bookings=Booking.objects.filter(date__range=(sdate,edate)).filter(e_date__range=(sdate,edate),is_delete=False,company=comp)
            serviceorders=Service_order.objects.filter(date__range=(sdate,edate),is_delete=False,booking_id__company=comp)
            incomebookings=0
            incomeserviceorders=0
            for booking in bookings:
                incomebookings+=booking.price
            for serviceorder in serviceorders:
                incomeserviceorders+=serviceorder.price
            args['ib']=incomebookings
            args['iso']=incomeserviceorders
            args['comp']=comp
            args['bookings']=bookings
            args['serviceorders']=serviceorders
            return render(request,'mypage/compdetail.html',args)
        else:
            return HttpResponse('У данного юзера недостаточно прав для доступа к данной странице.<p> <a href="/">Вернутся на главную страницу</a>')
    else:
        return HttpResponseRedirect("/login/")

def discountlist(request,sdate):
    if request.user.is_authenticated():
        args={}
        discs=Contract.objects.filter(s_date=sdate,is_active=True,company=None)
        args['discounts']=discs
        args['sdate']=sdate
        return render(request,'mypage/discslist.html',args)
    else:
        return HttpResponseRedirect("/login/")

def discountdetail(request,disc_id):
    if request.user.is_authenticated():
        args={}
        disc=get_object_or_404(Contract,pk=disc_id)
        args['disc']=disc
        return render(request,'mypage/discdetail.html',args)
    else:
        return HttpResponseRedirect("/login/")
