from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from customadmin.models import Signup
from django.http import HttpResponse
from django.contrib import messages
import re
from django.db.models import Q


def homedisp(request):
    return render(request,'customadmin/home.html') 


def logindisp(request):
      if 'username' in request.session:
          return render(request,'customadmin/dashboard.html')  
      if request.method=='POST':
        uname=request.POST.get("username")
        pword=request.POST.get("password")
        res=authenticate(username=uname,password=pword)
        if res is not None:
            request.session['username']=uname
            return render(request,'customadmin/dashboard.html')
        else:
            return render(request,'customadmin/adminlogin.html',{"errormsg":"Sorry,Invalid Credentials!"})
      return render(request,'customadmin/adminlogin.html')

@never_cache
def logoutdisp(request):
    if 'username' in request.session:
        request.session.flush()   
        return redirect(logindisp)


def datasdisp(request):
    credentials=User.objects.all()
    return render(request,"customadmin/datas.html",{"cr":credentials})

def datasdispcustomers(request):
    credentials2=Signup.objects.all()
    return render(request,"customadmin/datascustomers.html",{"cr2":credentials2})


def adddisp(request):
    if request.method=="POST":
        un=request.POST.get("username")
        em=request.POST.get("email")
        pw=request.POST.get("password")
        cpw=request.POST.get("cpassword")
        if not un.isalpha():
            editmsg1="Name should not contain numbers"

        elif len(un)<4:
            addmsg1="Name should have atleast 4 characters"
            
        elif len(un)>10:
            addmsg1="Username can only have at the most 10 characters"
             
           
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', em):
            addmsg1="Invalid Email"

        elif len(pw)<6:
            addmsg1="Password must altleast contain 6 characters"
            
        elif pw!=cpw:
            addmsg1="Passwords doesn't match to Confirm password!" 

        else:
            newres=User(username=un,email=em,password=pw)
            newres.save()
            return redirect(datasdisp)


        if addmsg1:
             credentials=User.objects.all()
             return render(request,"customadmin/datas.html",{"cr":credentials,"addmsg1":addmsg1})

        # if type(un) is int:
        #     messages.error(request, 'Invalid form submission')
        #     return redirect(datasdisp)
        # if pw!=cpw:
        #     messages.error(request, 'password and confirmpassword doesnt match')
        #     return redirect(datasdisp)
        





    


def updatedisp(request,myid):
     if request.method=="POST":
         name=request.POST.get("username")
         email=request.POST.get("email") 
         password=request.POST.get("password")
         cpassword=request.POST.get("cpassword")
         if not name.isalpha():
            editmsg1="Name should not contain numbers"

         elif len(name)<4:
            editmsg1="Name should have atleast 4 characters"
            
         elif len(name)>10:
            editmsg1="Username can only have at the most 10 characters"
             
           
         elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            editmsg1="Invalid Email"

         elif len(password)<6:
            editmsg1="Password must altleast contain 6 characters"
            
         elif password!=cpassword:
            editmsg1="Passwords doesn't match to Confirm password!" 

         else:
            updated=User(id=myid,username=name,email=email,password=password)
            updated.save()
            return redirect(datasdisp)
             

         if editmsg1:
             credentials=User.objects.all()
             return render(request,"customadmin/datas.html",{"cr":credentials,"editmsg1":editmsg1})
        



     


def deletedisp(request,myid2):
    if request.method=="POST":
        User.objects.filter(id=myid2).delete()

    
    return redirect(datasdisp)


def signupdisp(request):
    if 'cusername' in request.session:
        return redirect(homedisp)
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")
        phonenumber=request.POST.get("phonenumber")
        address=request.POST.get("address")

        if not username.isalpha():
            msg1="Name should not contain numbers"

        elif len(username)<4:
            msg1="Name should have atleast 4 characters"
            
        elif len(username)>10:
            msg1="Username can only have at the most 10 characters"
        
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            msg1="Invalid Email"

        elif len(password)<6:
            msg1="Password must altleast contain 6 characters"
            
        elif password!=cpassword:
            msg1="Passwords doesn't match to Confirm password!" 

        elif phonenumber.isalpha():
            msg1="Please enter a valid phone number" 

        elif len(phonenumber)!=10:
            msg1="Phone number should have ten digits" 

        elif not address.isalpha():
            msg1="Address should only contain alphabets"



        
            
        if msg1:

            return render(request,"customadmin/signup.html",{"msg1":msg1})


        res=Signup(username=username,email=email,password=password,cpassword=cpassword,phonenumber=phonenumber,address=address)
        res.save()
        msg="Signup Successfull"
        return render(request,"customadmin/signup.html",{"msg":msg})
        
    return render(request,"customadmin/signup.html")

@never_cache 
def customerlogindisp(request):
    if 'cusername' in request.session:
        myuser=request.session["cusername"]
        contents=Signup.objects.filter(username=myuser)
        return render(request,"customadmin/customerhomepage.html",{"contents":contents})
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        count=Signup.objects.filter(username=username,password=password).count()
        if count==1:
            request.session["cusername"]=username
            contents=Signup.objects.filter(username=username)# require only our details
            return render(request,"customadmin/customerhomepage.html",{"contents":contents})
        else:
            return render(request,"customadmin/customerlogin.html",{"cerror":"Sorry Invalid Credentials!"})
        




    return render(request,"customadmin/customerlogin.html")

# @never_cache 
# def customerhomepagedisp(request):
#     if 'cusername' in request.session:
#          contents=Signup.objects.all()
#          return render(request,"customadmin/customerhomepage.html",{"contents":contents})
    
@never_cache    
def customerlogoutdisp(request):
    if 'cusername' in request.session:
        request.session.flush()
        return render(request,'customadmin/customerlogin.html')

   
def searchdisp(request):
    if request.method=="GET":
        usernamesearch= request.GET.get('search')
        credentials=User.objects.filter(username__istartswith=usernamesearch)
        return render(request,"customadmin/datas.html",{"cr":credentials})
        

















# def dashboarddisp(request):
#     if request.method=='POST':
#         uname=request.POST("username")
#         pword=request.POST("password")
#         res=User.objects.filter(username=uname,password=pword).count()
#         if res==1:
#             return render(request,'customadmin/dashboard.html')
#         else:
#             return render(request,'customadmin/adminlogin.html',{"errormsg":"Invalid Credentials"})

    
