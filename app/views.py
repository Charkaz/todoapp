from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,LoginUser,addTask,Paylas,addComent
from .models import newtasks,serhs
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from .tasks import add,sendemail
from datetime import datetime,timedelta,time

from django.core.mail import send_mail


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")

            newUser = User(username = username,email = email)
            newUser.set_password(password)
            newUser.save()
            
            #add.apply_async('alisan','cerkez',eta=now + timedelta(seconds=10))

            #tomorrow = datetime.utcnow() + timedelta(days=1)
            #add.apply_async((14,15), countdown=10)
            recipient_list = [email,]
            sendemail.apply_async(("todoapp'e xos gelmisiniz ","Qeydiyyatiniz ugurla tamamlanmisdir.","todoapp98@gmail.com",recipient_list), countdown=10)
            #sendemails()


            messages.success(request,"Qeydiyyat ugurla tamamlandi !",extra_tags="success")
            context = {
            'form':form
        }
     
            
    else:
        form = RegisterForm()

        context = {
            'form':form
        }
    return render(request,"register.html",context)


def loginUser(request):

    form = LoginUser(request.POST or None)


    Context = {
        'form':form
    }

    if form.is_valid():
        username=form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username,password=password)

        if user is None:
            messages.info(request,"Bele istifadeci movcud deyil",extra_tags="info")
            return redirect("register")
        messages.info(request,"Ugurla daxil oldunuz",extra_tags="info")

        login(request,user)

        return redirect("dashboard")

    return render(request,"login.html",Context)



def dashboard(request):
    task = newtasks.objects.filter(author = request.user)

    Context = {
        'task':task
    }
    return render(request,"dashboard.html",Context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Hesabdan ugurla cixildi .",extra_tags="success")
    return  redirect("register")

def newtask(request):
    form = addTask(request.POST or None)

    Context = {
        'form':form
    }
     
    if form.is_valid():
        task = form.save(commit = False)
        task.author = request.user
        task.paylasan=request.user
        task.save()
        dates= task.deadline-task.created_date
        dates -= timedelta(1)
        
        tarix = int(dates.days)*86400
        
        
        

        print(tarix)
        
        recipient_list = [request.user.email,]
        sendemail.apply_async(("xatirlatma ","sizin tapsirigin bitme vaxtina 1 gun ve ya daha az qalib .","todoapp98@gmail.com",recipient_list), countdown=tarix)
           

        messages.success(request,"Yeni Task Ugurla yaradildi .",extra_tags="success")
        return redirect("dashboard")

    return render(request,"newtask.html",Context)


def details(request,pk):

    task = get_object_or_404(newtasks,pk=pk)

    serhler = serhs.objects.filter(task_id = pk)

    Context = {
        'task':task,
        'serhler':serhler
    }

    return render(request,"details.html",Context)



def update(request,pk):
    task = get_object_or_404(newtasks,pk=pk)
    form = addTask(instance=task,data=request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("dashboard")
    Context = {
        'form':form,
        'task':task
    }
    return render(request,"update.html",context=Context)

def delete(request,pk):
    task = get_object_or_404(newtasks,pk=pk)
    tasklar = newtasks.objects.filter(title=task.title,text=task.text,created_date = task.created_date)
    for data in tasklar:
        data.delete()
    return redirect("dashboard")

def share(request,pk):
    task = get_object_or_404(newtasks,pk=pk)
    form = Paylas(request.POST or None)
    Context = {
        'form':form,
        
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        user = User.objects.get(username = username)
        task.author = user
        title =task.title
        paylasan = task.paylasan
        text =task.text
        deadline =task.deadline
        created_date =task.created_date
        task2 = newtasks(author = user,title=title,text=text,deadline=deadline,created_date=created_date,paylasan = paylasan)
        task2.save()
        messages.success(request,"Yeni Task Ugurla yaradildi .",extra_tags="success")
        return redirect("dashboard")

    return render(request,"share.html",Context)


def comments(request,pk):

    form = addComent(request.POST or None)

   

    Context ={
        'form':form
        

    }
    if form.is_valid():
        serh = form.cleaned_data.get("serh")
      
        task = newtasks.objects.get(pk=pk)
        title = task.title
        text= task.text
        created_date = task.created_date
        ikincitask = newtasks.objects.filter(title=title,text=text,created_date=created_date)
        for i in ikincitask:
            tsk = newtasks.objects.get(pk=i.pk)
            coment = serhs(task = tsk ,serh=serh,user=request.user)
            coment.save()

        
        messages.success(request,"şərh ugurla qeyd edildi.",extra_tags="success")

        return redirect("details",pk)
        

    return render(request,"comments.html",Context)


def deletecoment(request,pk):
    serhim = get_object_or_404(serhs,pk=pk)

    serh = serhs.objects.filter(serh = serhim.serh , created_date = serhim.created_date)

    for data  in serh:
        data.delete()
    
    
    return redirect("dashboard")




def updatecoment(request,pk):
    serhim = get_object_or_404(serhs,pk=pk)
    

    form = addComent(instance=serhim,data=request.POST or None)
    serh = serhs.objects.filter(serh = serhim.serh , created_date = serhim.created_date)
    if form.is_valid():
        yenicoment = form.cleaned_data.get("serh")
        for data in serh:
            print(data.id)
            data.serh = yenicoment
            data.save()
        return redirect("dashboard")


    Context = {
        'form':form,
        'task':serhim
    }
    return render(request,"updatecoment.html",context=Context)



