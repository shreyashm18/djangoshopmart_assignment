from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .forms import UserForm

# Create your views here.

def home(request):
    return render(request,'home.html')    

# def register(request):
#     if request.method == "POST":
#         first_name = request.POST['firstname']
#         last_name = request.POST['lastname']
#         user_name = request.POST['username']
#         email=request.POST['email']
#         password1=request.POST['password1']
#         password2=request.POST['password2']
#         print(request.POST)
#         if password1 == password2:
#             if not User.objects.filter(email=email).exists():
#                 if not User.objects.filter(username=user_name).exists():
#                     user = User.objects.create_user(username=user_name,email=email,password=password1,first_name=first_name,last_name=last_name)
#                     user.save()
#                     print('user created')
#                     return redirect('home')
#                 else:
#                     print('username taken')
#                     return redirect('register')
#             else:
#                 print('email taken')
#                 return redirect('register')

#         else:
#             print('password not matching')
#             return redirect('register')

#     else:
#         return render(request,'register.html')

def employee_add(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            u = user_form.save()    
            return redirect('home')
        else:
            return render(request, 'add.html', context)
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        return render(request, 'add.html', context)

def user_login(request):
    if request.method =="POST":
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(request,username = username, password = password)
        if user:
            auth.login(request,user=user)
            if request.GET.get('next', None):
                return redirect(request.GET["next"])
            return redirect('all_products')
        else:
            return render(request,'login.html',{'error':'Please provide correct credintials'})
    else:
        return render(request,'login.html')
        
@login_required(login_url = 'user_login')
def user_logout(request):
    auth.logout(request)
    return redirect('home')
