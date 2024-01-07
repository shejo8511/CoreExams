from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, Page
from django.db import IntegrityError, transaction
from datetime import date, datetime
import datetime as dt_datetime
import pytz
from django.contrib.auth.models import User
from company.models import Company
from .models import Patient, PatientExam, ExamSample
from exam.models import TypeExam
from datetime import date, datetime
from django.db.models import Q

# Consulta de Pacientes
def consultPatient(id):
    patient = Patient.objects.get(id=id)
    return patient

# Consulta de Compania
def consultCompany(id):
    company = Company.objects.get(id=id)
    return company

# Consulta de Tipo Examen
def consultTypeExam(id):
    type_exam = TypeExam.objects.get(id=id)
    return type_exam

# Consulta de Paciente Examen
def consultPatientExam(id):
    patientExam = PatientExam.objects.get(id=id)
    return patientExam

# Consulta de User
def consultUser(id):
    user = User.objects.get(id=id)
    return user

# Fecha de Ahora
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

# Fecha y Tiempo de Ahora
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

# Calcual la Edad recibiendo la fecha cumpleaños
def calatorAge(birthday_str):
    birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
    hoy = date.today()
    age = hoy.year - birthday.year - ((hoy.month, hoy.day) < (birthday.month, birthday.day))
    return age

#Listado de Pacientes
@login_required
def listPatientExam(request):
    company = Company.objects.filter(user_id=request.user.id).first()
    search_term = request.GET.get('search_term')
    if company:
        if search_term:
            print("----search_term: "+str(search_term))
            #listPatientExam = PatientExam.objects.filter(identification=search_term | full_name=search_term).order_by('-date_exam')
            listPatientExam = PatientExam.objects.filter(
                Q(patient__identification__icontains=search_term) | Q(patient__full_name__icontains=search_term)
            ).order_by('-date_exam')
        else:
            #listPatient = Patient.objects.filter(company_id=company.id)
            listPatientExam = PatientExam.objects.filter(company=company.id).order_by('-date_creation')
        paginator = Paginator(listPatientExam, 10)  # Especifica el número de elementos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual de los parámetros de la URL
        page = paginator.get_page(page_number)  # Obtiene la página solicitada
        context = {'listPatientExam':listPatientExam,'company':company,'page':page}
        return render(request,'list_patient.html',context)

#Crear Paciente
@transaction.atomic
def createPatient(identification,full_name,company,birthday,user):
    # Compara si existe el paciente
    if not Patient.objects.filter(identification=identification,company=company).exists():
        #Calculo de EDAD
        age = calatorAge(birthday)
        #Crear Paciente
        objPatient = Patient.objects.create(full_name=full_name,identification=identification,company=consultCompany(company),birthday=birthday,
                            age=age,create_by_id=user,update_by_id=user)
        objPatient.save()
        return objPatient.id
    else:
        # Consulta y devuelve el Paciente
        objPatient = Patient.objects.filter(identification=identification,company=company).get()
        return objPatient.id

#Crear Examen Paciente
@transaction.atomic
def createPatientExam(patient,type_exam,company,user):
    # Busca y compara si el paciente ya se realizo un examen - busca por paciente,tipo examen,compania,dia y fecha hora
    if not PatientExam.objects.filter(patient=patient,type_exam=type_exam,company=company,date_exam=dateNowEcuador()).exists():
        #Crear Paciente Examen
        objPatientExam = PatientExam.objects.create(patient=consultPatient(patient),company=consultCompany(company),
                                                    type_exam=consultTypeExam(type_exam),date_exam=dateNowEcuador(),
                                                    create_by_id=user,update_by_id=user)
        objPatientExam.save()
        return objPatientExam.id
    else:
        # si xiste devuelve el id
        patientExamObjt = PatientExam.objects.filter(patient=patient,type_exam=type_exam,company=company,date_exam=dateNowEcuador()).get()
        return patientExamObjt.id

@transaction.atomic
def savePatientImg(name,patient,typeExam,patientExam,company,url_folder_sample,sample_url,user):
    #Crear Examen Muestra
    objExamSample = ExamSample.objects.create(name=name,patient=consultPatient(patient),type_exam=consultTypeExam(typeExam),
                                                patientexam=consultPatientExam(patientExam),company=consultCompany(company),
                                                url_folder_sample=url_folder_sample,sample_url=sample_url,
                                                save_date=dateNowEcuador(),create_by_id=user,update_by_id=user)
        
    objExamSample.save()
    return objExamSample.id