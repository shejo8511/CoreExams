from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from .forms import LoginForm
from company.forms import CompanyForm
from user.forms import CustomUserCreationForm
from company.models import Company, Membership
from exam.models import TypeExam
from django.contrib.auth import login, logout, authenticate
#Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
#Para Fechas (dateTimeNowEcuador,dateNowEcuador)
from datetime import date, datetime
import datetime as dt_datetime
import pytz
import os

#Funciones Fechas
def dateTimeNowEcuador():
    ## Hora Ajustada
    # Obtener el tiempo actual con la zona horaria UTC
    now_utc = dt_datetime.datetime.now(tz=pytz.utc)

    # Convertir a la zona horaria deseada
    timezone = pytz.timezone('America/Guayaquil')  # Cambia 'America/New_York' a la zona horaria deseada
    now_local = now_utc.astimezone(timezone)

    # Restar 5 horas al tiempo local
    adjusted_time = now_local - dt_datetime.timedelta()

    # Formatear la hora ajustada como una cadena
    adjusted_time_str = adjusted_time.strftime('%Y'+'-'+'%m'+'-'+'%d-%H'+':'+'%M'+':'+'%S')

    return adjusted_time_str

def dateNowEcuador():
    # Hora Ajustada
    # Obtener el tiempo actual con la zona horaria UTC
    now_utc = datetime.now(tz=pytz.utc)

    # Convertir a la zona horaria deseada
    timezone = pytz.timezone('America/Guayaquil')  # Cambia 'America/New_York' a la zona horaria deseada
    now_local = now_utc.astimezone(timezone)

    # Restar 5 horas al tiempo local
    adjusted_date = now_local - dt_datetime.timedelta()

    # Formatear la hora ajustada como una cadena
    adjusted_date_str = adjusted_date.strftime('%Y'+'-'+'%m'+'-'+'%d')

    return adjusted_date_str

# Para Cerrar Sesion
def singout (request):
    logout(request)
    return redirect('signin')

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

#Para iniciar la Sesion
@unauthenticated_user
def signin (request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                #print("user: "+ str(user))
                form = LoginForm()
                return render(request, 'signin.html',{
                    'form':form,
                    'message':'Usuario o Contraseña incorrectos'
                })
    else:
        if request.method == 'GET':
            #print("GET")
            #if not User.objects.filter(username='administrador',email="administrador@admin.com.ec",is_active=True).exists():
            #    print("No existe User -- Se Crea Usuario Shejo")
            #    user = User(username = 'administrador',
            #                is_superuser = True,
            #                first_name = 'Administrador',
            #                last_name = 'Admin',
            #                email = 'administrador@admin.com.ec',
            #                is_active = True)
            #    user.set_password('123Stream..')
            #    user.save()
            #    company = Company(company_name='Aministrador',
            #                    name='Admin',
            #                    last_name='Admin',
            #                    identification='1234567890',
            #                    identification_type='CI',
            #                    phone='099999999',
            #                    address='------------',
            #                    registration_date=dateNowEcuador(),
            #                    pay_date=dateNowEcuador(),
            #                    date_creation=dateTimeNowEcuador,
            #                    enabled_comp=1,
            #                    user_id=user.id)
            #    company.save()
            #else:
            #    print("Existe User: "+str(User.objects.filter(username='administrador',email="administrador@admin.com.ec",is_active=True).exists()))
            form = LoginForm()
            return render(request, 'signin.html',{
                'form':form
            })

#Para ir al Inicio de la aplicacion
@login_required
def home (request):
    company = Company.objects.filter(user_id=request.user.id).first()
    type_exams = TypeExam.objects.filter(enabled=1)
    type_exams_list = list(type_exams.values('id', 'name'))
    try:
        if request.method == 'GET':
            context = {
                'company': company,
                'typeExam': type_exams_list,
            }
            return render(request, 'home.html',context)
        else:
            print("linea 135: home")
            return render(request, 'home.html',context)
    except Exception as e:
        print("linea 138: home"+str(e))
        return render(request, 'home.html', {'message' : e, 'company':company})

@login_required
#@user_passes_test(lambda u: u.username == 'administrador', login_url='/home/')
@transaction.atomic
def register(request):
    try:
        company_user = Company.objects.filter(user_id=request.user.id).first()
        memberships = Membership.objects.filter(enabled=1)
        memberships_list = list(memberships.values('id', 'name'))
        if request.method == 'POST':
            print("POST")
            user_form = CustomUserCreationForm(request.POST)
            #print("484")
            company_form = CompanyForm(request.POST,request.FILES)
            #print("486")
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            #membershipInt = membership.objects.get(id=1)
            membPOST = request.POST['membership']
            #print("password1: " + password1 + "== password2: " + password2)
            #logo = company_form.logo
            #print("491 logo: " + str(logo))
            print("149 membPOST: " + str(membPOST))
            if password1 == password2:
                print("493")
                resEmail = User.objects.filter(email=request.POST['email']).first()
                print("resEmail: "+str(resEmail))
                if User.objects.filter(email=request.POST['email']).first():
                    email_errors = 'El Email o Correo Electronico ya existe.'
                    print("491")
                    print("email_errors: "+email_errors)
                    return render(request ,'register.html', {'message':email_errors,'user_form': user_form, 'company_form': company_form,'company':company_user,'memberships_list':memberships_list})
                resIdentification = Company.objects.filter(identification=request.POST['identification']).first()
                print("residentification: "+str(resEmail))
                if Company.objects.filter(identification=request.POST['identification']).first():
                    print("491")
                    identificarion_errors = 'El Numero de Identificacion ya existe.'
                    print("497")
                    return render(request ,'register.html', {'message':identificarion_errors,'user_form': user_form, 'company_form': company_form,'company':company_user,'memberships_list':memberships_list})
                resUserFormValid = user_form.is_valid()
                resCompFormValid = company_form.is_valid()
                print("resUserFormValid: "+str(resUserFormValid))
                print("resCompFormValid: "+str(resCompFormValid))
                if user_form.is_valid() and company_form.is_valid():
                    print('VALID FORM')
                    print('USER')
                    #USUARIO
                    #user_form.cleaned_data['is_superuser'] = True
                    user_form.cleaned_data['is_active'] = True
                    user_form.cleaned_data['first_name'] = request.POST['name']
                    user_form.cleaned_data['last_name'] = request.POST['last_name']
                    user_form.cleaned_data['date_join'] = dateTimeNowEcuador()
                    user = user_form.save()
                    print('COMPANIA')
                    #COMPANIA
                    print("membership line 184")
                    company = company_form.save(commit=False)
                    company_form.cleaned_data['create_by_id'] = request.user.id
                    company_form.cleaned_data['date_creation'] = dateTimeNowEcuador()
                    company.membership_id = membPOST
                    company.user = user
                    company.save()
                    print("company line 192: "+str(company))
                    print('LINEA 509')
                    #Crear Carpeta
                    carpeta = request.POST['username']
                    directorio = os.getcwd()  # obtiene el directorio actual
                    ruta = os.path.join(settings.MEDIA_EXAM_USUARIOS_ROOT, carpeta)  # une el nombre de la carpeta con el directorio
                    os.makedirs(ruta)  # crea la carpeta en la ruta especificada
                    print('LINEA 515')
                    return redirect('home')
                else:
                    print('LINEA 538')
                    
                    #if user_form.errors.get('username', None):
                    #    print('LINEA 538')
                    #    username_errors = user_form.errors.get('username', None)
                    #    return render(request ,'register.html', {'message':username_errors,'user_form': user_form, 'company_form': company_form})
                    #if user_form.errors.get('password2'):
                    #    print('LINEA 542')
                    #    password_errors = user_form.errors.get('password2')
                    #    return render(request ,'register.html', {'message':password_errors,'user_form': user_form, 'company_form': company_form})
                    if user_form.errors:
                        print('LINEA 575')
                        message_errUsr = user_form.errors.as_text()
                        #message_err = str(message_errUsr +'  '+ message_errCmp)
                        print('LINEA 578: ' + message_errUsr)
                        return render(request ,'register.html', {'message':message_errUsr,'user_form': user_form, 'company_form': company_form,'company':company_user,'memberships_list':memberships_list})
                    if company_form.errors:
                        message_errCmp = company_form.errors.as_text()
                        print('LINEA 582: ' + message_errCmp)
                        return render(request ,'register.html', {'message':message_errCmp,'user_form': user_form, 'company_form': company_form,'company':company_user,'memberships_list':memberships_list})
                print('LINEA 584')
            else:
                return render(request ,'register.html', {'message':'Las Contraseñas no conciden','user_form': user_form, 'company_form': company_form,'company':company_user,'memberships_list':memberships_list})
        else:
            print("GET")
            user_form = CustomUserCreationForm()
            company_form = CompanyForm()
            #membership = Membership.objects.filter(enabled=1)#.values_list('id', 'name')
            memberships = Membership.objects.filter(enabled=1)
            memberships_list = list(memberships.values('id', 'name'))
            #print(memberships_list)
        return render(request, 'register.html', {'user_form': user_form, 'company_form': company_form,'company':company_user,'memberships_list':memberships_list})
    except Exception as e:
        print('e: '+ str(e))
        print("223")
        return render(request, 'register.html', {'message' : e,'user_form': user_form, 'company_form': company_form,'company':company_user,'memberships_list':memberships_list})


@api_view(['POST'])
def login_view(request):
    print("linea 706: login_view")
    username = request.data.get('username')
    password = request.data.get('password')
    #print("linea 709: username: "+ str(username) + " | password: " + str(password))
    user = authenticate(request, username=username, password=password)
    #print("linea 711: user: "+str(user))
    if user is not None:
        login(request, user)
        return Response({'message': 'Logged in successfully'},200)
    else:
        return Response({'message': 'Invalid credentials'},400)

def help(request):
    copyri = settings.MEDIA_ROOT + 'copyright.jpg'
    print("copyri: "+copyri)
    return render(request, 'help.html', {'copyri' : copyri})

