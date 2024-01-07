import os
from os import path
import pytz
import base64
import json
from PIL import Image
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
#from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.core.paginator import Paginator, Page
#import playsound
#import simpleaudio as sa
from datetime import date, datetime
import datetime as dt_datetime
from .models import TypeExam
from .forms import TypeExamForm
from company.models import Company
from .models import TypeExam
from patient.models import Patient, PatientExam, ExamSample
from patient.views import createPatient, createPatientExam, savePatientImg
#PDF
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4,landscape
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa

#Fechas y Horas
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

# Consulta de Tipo Examen ID
def consultTypeExam(id):
    type_exam = TypeExam.objects.get(id=id)
    return type_exam

# Consulta PatientExam ID
def consultPatientExam(id):
    patientExam = PatientExam.objects.get(id=id)
    return patientExam

# Consulta de Tipo Examen ID
def consultPatientSampleExam(id):
    patientSampleExam = ExamSample.objects.get(id=id)
    return patientSampleExam

# Consulta de Tipo Examen Nombre
def consultTypeExamName(name):
    type_exam = TypeExam.objects.get(name=name)
    return type_exam.id

# Consulta de Paciente identification
def consultPatient(identification,company):
    patient = Patient.objects.get(identification=identification,company=company)
    return patient.id

# Consulta de Paciente OBJETO
def consultPatientObj(id):
    objPatient = Patient.objects.filter(id=id).values()
    return objPatient

@login_required
def listTypeExam(request):
    company = Company.objects.filter(user_id=request.user.id).first()
    if company:
        listTypeExam = TypeExam.objects.filter(enabled=1).order_by('-name')
        paginator = Paginator(listTypeExam, 10)  # Especifica el número de elementos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual de los parámetros de la URL
        page = paginator.get_page(page_number)  # Obtiene la página solicitada
        context = {
            'listTypeExam':listTypeExam,
            'company':company,
            'page':page,
            }
        return render(request,'type_exam/list_type_exam.html', context)

@login_required
@csrf_exempt
@transaction.atomic
def typeExam(request):
    try:
        company_user = Company.objects.filter(user_id=request.user.id).first()
        if request.method == 'POST':
            #POST
            type_exam_form = TypeExamForm(request.POST)
            if type_exam_form.is_valid():
                type_exam_form.save()
                return render(request, 'type_exam/list_type_exam.html',{'company': company_user})
            else:
                if type_exam_form.errors:
                    message_errMemb = type_exam_form.errors.as_text()
                    return render(request,'type_exam/type_exam.html',{'message':message_errMemb,'type_exam_form':type_exam_form,'company':company_user})
        else:
            #GET
            type_exam_form = TypeExamForm()
        return render(request,'type_exam/type_exam.html',{'company': company_user,'type_exam_form':type_exam_form})
    except Exception as e:
        return render(request, 'type_exam/type_exam.html', {'message' : e,'type_exam_form': type_exam_form,'company':company_user})

@login_required
@csrf_exempt
def guardar_captura(request):
    try:
        company_user = Company.objects.filter(user_id=request.user.id).first()
        print("Dentro de Guardar-captura: linea 63")
        if request.method == 'POST':
            # Obtiene los datos del Paciente
            identification = request.POST.get('identification')
            typeExam = (request.POST.get('typeExam')).upper()
            idExam = (request.POST.get('idExam'))
            print("idExam: "+idExam)
            # Obtiene la captura de pantalla enviada por el cliente
            captura_pantalla = request.POST.get('capture')
            # Decodifica la captura de pantalla desde Base64
            imagen_decodificada = base64.b64decode(captura_pantalla.split(',')[1])
            sigNum = 0
            if ExamSample.objects.filter(patientexam_id=idExam):
                print("Si Existen")
                num = ExamSample.objects.filter(patientexam_id=idExam).count()
                sigNum = num + 1
                print("line 170: sigNum: "+str(sigNum))
            else:
                sigNum = 1
                print("Inicio-line 173: sigNum: "+str(sigNum))
            # Guarda la captura de pantalla en el sistema de archivos
            folder = os.path.join(settings.MEDIA_EXAM_USUARIOS_ROOT + request.user.username + '/' + idExam + '_' + identification + '_'+ typeExam +'_' + dateNowEcuador())
            url = settings.MEDIA_EXAMS_USUARIOS_URL + request.user.username + '/' + idExam + '_' + identification + '_' + typeExam + '_' + dateNowEcuador()
            print("folder: "+str(folder))
            print("url: "+str(url))
            
            if not os.path.exists(folder):
                os.makedirs(folder)
            else:
                with open(os.path.join(folder, str(sigNum) +'_'+ idExam +'_'+identification +'_'+ typeExam +'_'+ dateNowEcuador() +'.jpg'), 'wb') as f:
                    if f.write(imagen_decodificada):
                        #Nombre de la Imagen
                        name = str(sigNum) + '_' + idExam + '_' + identification + '_'+ typeExam +'_' + dateNowEcuador() + '.jpg' 
                        idPatient = consultPatient(identification,company_user.id)
                        idTypeExam = consultTypeExamName(typeExam)
                        sample_url = url +'/' + str(sigNum) + '_' + idExam + '_' + identification +'_'+ typeExam +'_'+ dateNowEcuador() +'.jpg'
                        ResExamSample = savePatientImg(name,idPatient,idTypeExam,idExam,company_user.id,url,sample_url,request.user.id)
                        if not ResExamSample:
                            return render(request, 'stream/videoStream.html', {'message' : e,'company':company_user})
            #else:
            #    message = "La Captura no puede Guardarse no existe la Capeta para el Cliente: "+identification + " - " + full_name
            #    return render(request ,'stream.html', {'message':message})
            # Envía una respuesta de éxito al cliente
            #pathSound = path.join(settings.MEDIA_ROOT_SOUNDS, 'camara_5.mp3')
            #playsound(pathSound, use_py2=True)
            #wave_obj = sa.WaveObject(pathSound)
            #audio_data = bytes(wave_obj.audio_data)
            #wave_obj.play(audio_data)

            return JsonResponse({'success': True})
        else:
            # Si se recibe un método de solicitud diferente, envía una respuesta de error
            return JsonResponse({'error': 'Método no permitido'}, status=405)
    except HttpResponseServerError as message:
        print("error: "+ str(message))

@login_required
@csrf_exempt
@transaction.atomic
def videoStream(request):
    company_user = Company.objects.filter(user_id=request.user.id).first()
    try:
        if request.method == 'POST':
            identification = request.POST.get('identification')
            birthday = request.POST.get('birthday')
            full_name = request.POST.get('full_name')
            typeExam = request.POST.get('typeExam')
            # Crea el Paciente o devulve el paciente si existe
            print("line 183: objPatient; ")
            objPatient = createPatient(identification,full_name,company_user.id,birthday,request.user.id)
            print("line 185: objPatient; "+str(objPatient))
            print("line 186: company_user; "+str(company_user))
            print("line 187: company_user.id; "+str(company_user.id))
            # Verfica que el paciente se creo o devuelve el id del paciente
            if objPatient:
                print("line 190: objPatient; "+str(objPatient))
                patientExam = createPatientExam(objPatient,typeExam,company_user.id,request.user.id)
                print("linea 192: patientExam: "+str(patientExam))
                if os.path.isdir((settings.MEDIA_EXAM_USUARIOS_ROOT + request.user.username)):
                    #Crear Carpeta
                    nueva_carpeta = str(str(patientExam) + '_' +request.POST.get('identification')) + '_' + str(consultTypeExam(request.POST.get('typeExam'))).upper() + '_' + dateNowEcuador()
                    #directorio = os.getcwd()  # obtiene el directorio actual
                    ruta = os.path.join(settings.MEDIA_EXAM_USUARIOS_ROOT + request.user.username+'/', nueva_carpeta)  # une el nombre de la carpeta con el directorio
                    if not os.path.isdir(ruta):
                        os.makedirs(ruta)  #crea la carpeta en la ruta especificada
                context = { 'company':company_user,
                        'identification':identification,
                        'birthday':birthday,
                        'full_name':full_name,
                        'typeExam':consultTypeExam(typeExam),
                        'idExam':patientExam,
                        'username':company_user}
                return render(request, 'stream/videoStream.html',context)
        if request.method == 'GET':
            print("linea 208: videoStream")
            #type_exams = TypeExam.objects.filter(enabled=1)
            #type_exams_list = list(type_exams.values('id', 'name'))
            #context = {
            #    'company': company_user,
            #    'typeExam': type_exams_list,
            #}
            return redirect("home")
            #return render(request, "home.html", context)
    except Exception as e:
        #company_user = Company.objects.filter(user_id=request.user.id).first()
        print("linea 212: videoStream-company_user: "+str(company_user))
        print("linea 213: videoStream-e: "+str(e))
        return render(request, 'home.html', {'message' : e,'company':company_user})


    print("line 266 - user: "+ str(iduser))
    print("line 267 - idExam: "+ str(idExam))
    try:
        print("linea 269 generate_pdf: "+str(iduser))
        company_user = Company.objects.filter(user_id=iduser).first()
        #-----------------------------
        # Ruta donde se encuentran las imágenes
        ruta_imagenes = ExamSample.objects.filter(patientexam_id=idExam).first()
        examPatient = PatientExam.objects.filter(id=idExam).first()
        patient = Patient.objects.filter(id=examPatient.patient_id).first()
        print("line 276 - ruta_imagenes.url_folder_sample: " + str(ruta_imagenes.url_folder_sample))
    ##    ruta_imagenes = str(settings.MEDIA_EXAM_USUARIOS_ROOT + request.user.username +'/'+ identification +'_'+ dateNowEcuador())
        ruta_imagenes = str(ruta_imagenes.url_folder_sample)
        #nombre_pdf = str(identification + '_EXAM_'+ dateNowEcuador()+'.pdf')
        print("line 280 - patient.identification: "+str(patient.identification))
        print("line 281 - patient: "+str(examPatient.type_exam))
        nombre_pdf = str(patient.identification + '_' + str(examPatient.type_exam) + '_' + dateNowEcuador() + '.pdf')
        print("linea 283 - nombre del PDF: " + nombre_pdf)
        print("linea 284 - PDF_SAVE: " + settings.PDF_SAVE_ROOT)
    ##    ruta_pdf = settings.MEDIA_EXAM_USUARIOS_ROOT +request.user.username+'/'+identification+'_'+dateNowEcuador()+'/'+identification+'_EXAM_'+dateNowEcuador()+".pdf"
        ruta_pdf = settings.PDF_SAVE_ROOT + username + '/' + idExam + '_' + patient.identification + '_' +str(examPatient.type_exam) + '_' + dateNowEcuador() + '/' + patient.identification + '_' + str(examPatient.type_exam) + '_' + dateNowEcuador() + '.pdf'
        print("linea 287 ruta_pdf: "+ str(ruta_pdf))
        #imagenes = [os.path.join(ruta_imagenes, f) for f in os.listdir(ruta_imagenes) if os.path.isfile(os.path.join(ruta_imagenes, f))]
        print("linea 289 - EXAMS_SAMPLE_ROOT: " + settings.EXAMS_SAMPLE_ROOT)
        #imagenes = [archivo for archivo in os.listdir(settings.EXAMS_SAMPLE_ROOT + username +'/'+ idExam +'_' + patient.identification + '_'+ str(examPatient.type_exam) +'_'+ dateNowEcuador()) if archivo.endswith(".jpg")]
        imagenes = []
        list_img_select = ExamSample.objects.filter(patientexam=idExam,select = 1)
        print("line 293 - list_img_select: " + str(list_img_select))
        for img in list_img_select:
            print("line 295 - img: "+ str(img.id))
            objExamPatient = ExamSample.objects.get(id=img.id)
            imagenes.append([objExamPatient.name+'.jpg'])
        print("imagenes 298: "+str(imagenes))
        #Remover PDF
        if os.path.exists(ruta_pdf):
            os.remove(ruta_pdf)

        # Crear PDF
        pdf = canvas.Canvas(ruta_pdf, pagesize=A4)
        titulo = "Resultado de Examenes"
        pdf.setFont("Courier", 18)
        pdf.drawString(10, 800, titulo)
        w, h = A4
        xlist = [100, 150, 350]
        ylist = [h - 5, h - 120]
        pdf.grid(xlist, ylist)

        # Guardar y cerrar el PDF
        print("linea 314 : generate_pdf")
        pdf.save()
        print("linea 316 : generate_pdf")
        return True
        #print("linea 321 : username: "+username)
        #print("linea 322 : idExam: "+idExam)
        #download_pdf(username,idExam)
    except Exception as e:
        return render(request, 'reports/examsSelect.html', {'message' : e,'company':company_user})

#Renderiza el HTML para Crear el PDF
def render_to_pdf(template_src,iduser, context_dict={}):
    ##Imagen de Marca de AGUA
    #company_user = Company.objects.filter(user_id=request.user.id).first()
    company = Company.objects.get(user_id=iduser)
    logo = company.logo #settings.STATIC_IMG_URL + 'noLogo.jpg'
    logoUrl = settings.MEDIA_ROOT +'/' + str(logo)
    print("314 logoUrl-renderToPDF: "+str(logoUrl))
    

    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result,encoding='utf-8')
    if not pdf.err:
        image = Image.open(logoUrl)
        #pdf.add_watermark(image=image,position='center',opacity=0.5)
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# Clase para Reporte.
class ReportExam01(View):

    def getPDF(iduser,username,idExam):
        print("get-ReportExam01")
        #identification = str(request.GET.get('identification'))
        ruta_imagenes = ExamSample.objects.filter(patientexam_id=idExam).first()
        examPatient = PatientExam.objects.filter(id=idExam).first()
        patient = Patient.objects.filter(id=examPatient.patient_id).first()
        patientExam = PatientExam.objects.filter(id=idExam).first()
        #Ruta donde se encuentran las imágenes
        #print("line 322 - examPatient.type_exam: " +str(examPatient.type_exam))
        ruta_dir_pdf = str(settings.EXAMS_SAMPLE_ROOT + username +'/'+ idExam + '_' + patient.identification + '_' + str(examPatient.type_exam) +'_'+ dateNowEcuador()+'/')
        rutaImg = str(settings.EXAMS_SAMPLE_ROOT + username +'/'+ idExam + '_' + patient.identification + '_' + str(examPatient.type_exam) +'_'+ dateNowEcuador()+'/')
        #rutaImg = str('media/exams/usuario/'+ username + '/' + idExam + '_' + patient.identification + '_' + str(examPatient.type_exam) +'_'+ dateNowEcuador()+'/')
        print("linea 327: rutaImg: "+str(rutaImg))
        #nombre_pdf = str(identification + '_EXAM_'+ dateNowEcuador()+'.pdf')
        #ruta_pdf = settings.MEDIA_EXAM_USUARIOS_ROOT +request.user.username+'/'+identification+'_'+dateNowEcuador()+'/'+identification+'_EXAM_'+dateNowEcuador()+".pdf"
        #imagenes = [os.path.join(ruta_imagenes, f) for f in os.listdir(ruta_imagenes) if os.path.isfile(os.path.join(ruta_imagenes, f))]
        #imagenes = [archivo for archivo in os.listdir(settings.MEDIA_EXAM_USUARIOS_ROOT + request.user.username +'/'+ identification +'_'+ dateNowEcuador()) if archivo.endswith(".jpg")]
        imagenes = []
        diagnostic = []
        #list_img_select = ExamSample.objects.filter(patientexam=idExam,select = 1)
        #print("line 329 - list_img_select: " + str(list_img_select))
        # Consulta que extrae un objeto específico
        # Consulta que devuelve un objeto con los valores de los campos especificados
        sample_exam = ExamSample.objects.filter(patientexam=idExam, select=1).all()
        #print("line 337 - sample_exam: " + str(sample_exam))
        #for sample in sample_exam:
        #    print("line 333 - id: "+ str(sample.id))
        #    print("line 334 - sample_url: "+ str(sample.sample_url))
        #    print("line 335 - diagnostic: "+ str(sample.diagnostic))
            #objExamPatient = ExamSample.objects.get(id=img.id)
            #imagenes.append(objExamPatient.sample_url)
            #diagnostic.append(objExamPatient.diagnostic)


        #grupos = [imagenes[i:i+3] for i in range(0, len(imagenes), 3)]
        #grupos_dig = [diagnostic[i:i+3] for i in range(0, len(diagnostic), 3)]
        #primeros_seis_imagenes = imagenes[:6]
        #print("grupos 350: "+str(grupos))
        #print("grupos_dig 351: "+str(grupos_dig))
        ##=================##
        company = Company.objects.get(user_id=iduser)
        #patient = PatientExam.objects.get(identification=examPatient.identification,date_exam=dateNowEcuador())
        #nombreCompany = company.company_name
        logo = company.logo #settings.STATIC_IMG_URL + 'noLogo.jpg'
        #print("357 logo: "+str(logo))
        logoUrl = settings.MEDIA_ROOT +'/' + str(logo)
        print("360 logoUrl: "+str(logoUrl))
        #print("identification: " + str(identification))
        #print("*args: " + str(*args))
        
        data = {
            'patient': patient,
            'patientExam':patientExam,
            'logo':logoUrl,
            'company': company,
            #'imagenes':primeros_seis_imagenes,
            #'grupos':grupos,
            #'grupos_dig':grupos_dig,
            'sample_exam':sample_exam,
            'rutaImg':rutaImg
        }
        #request_path = request.path
        #print(request_path)
        # Guarda el PDF en la ruta especificada
        print("line 375: "+str(iduser))
        pdf = render_to_pdf('reports/reportExam01.html', iduser, data)
        print("line 375" + str(pdf))
        if pdf:
            print("line 382")
            nombrePDF = idExam + '_' + patient.identification + '_' + str(examPatient.type_exam) + '_' + dateNowEcuador()+'.pdf'
            ruta_pdf = os.path.join(ruta_dir_pdf, nombrePDF)
            examPatient.exam_url = ruta_dir_pdf + nombrePDF
            with open(ruta_pdf, 'wb') as f:
                f.write(pdf.content)
            examPatient.save()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+nombrePDF+'.pdf"'
        return response

    def guardarPDF(request,pdf):
        pass

@login_required
@csrf_exempt
#@transaction.atomic
def examsSelect(request):
    print("examsSelect - linea 351: ")
    company_user = Company.objects.filter(user_id=request.user.id).first()
    try:
        # Process the diagnostic text
        idExam = 0
        diagnostic_list = []
        select_list = []
        if request.method == 'POST':

            idExam = request.POST.get('idExam')
            diagnostic_general = request.POST.get('diagnostic_general')
            print("POST - line: 429: "+str(idExam))
            print("POST - linea 430: ")
            print("POST - linea 431: "+str(diagnostic_general))
            #listSamplesExam = request.POST.getlist('listSamplesExam')
            select_value = request.POST.getlist('select')
            print("select_value - linea 434: " + str(select_value))
            
            #Valida si es mayor a 9 imagenes seleccionadas
            """if len(select_list) > 9:
                print("select_list line 438: " + str(select_list))
                print("No puede seleccionar más de 9 elementos")
                message = "No puede seleccionar más de 9 elementos"
                print("linea 419: GET examsSelect")
                idExam = request.POST.get('idExam')
                print("linea 421: GET idExam: " + str(idExam))
                objExamPatient = PatientExam.objects.filter(id=idExam,company=company_user.id).values()
                objPatient = consultPatientObj(objExamPatient[0]['patient_id'])
                listSamplesExam = ExamSample.objects.filter(patientexam_id=idExam)
                birthday = objPatient[0]['birthday'].strftime('%Y-%m-%d')
                diagnostic_general = objExamPatient[0]['diagnostic_general']
                context = { 'company':company_user,
                            'identification':objPatient[0]['identification'],
                            'birthday':birthday,
                            'full_name':objPatient[0]['full_name'],
                            'typeExam':consultTypeExam(objExamPatient[0]['type_exam_id']),
                            'idExam':idExam,
                            'listSamplesExam':listSamplesExam,
                            'diagnostic_general': diagnostic_general,
                            'message' : message,
                }
                return render(request, 'reports/examsSelect.html', context)"""

            # Create List for Select
            for row in select_value:
                id_object, select = row.split(',')
                select_list.append([id_object, select])

            diagnostic = request.POST.getlist('diagnostic')
            #print("diagnostic_list - linea 238: " + str(diagnostic))
            
            # Create List for diagnostic
            for select_value, diagnostic in zip(select_value, diagnostic):
                id_object, value = select_value.split(',')
                diagnostic_list.append([id_object,diagnostic])
            
            #print("diagnostic_list - linea 244: " + str(diagnostic_list))
            
            #Update Select
            for row_select in select_list:
                id_select, select = row_select
                objSampleExam = consultPatientSampleExam(id_select)
                objSampleExam.select = True
                objSampleExam.save()
                #print("id_select - linea 258: " + str(id_select))
                #print("select - linea 259: " + str(select))
            
            #Update Diagnostic
            for row_diagnostic in diagnostic_list:
                id_diagnostic, diagnostic = row_diagnostic
                objSampleExam = consultPatientSampleExam(id_diagnostic)
                objSampleExam.diagnostic = diagnostic
                objSampleExam.save()
                #print("id_diagnostic - linea 248: " + str(id_diagnostic))
                #print("diagnostic - linea 249: " + str(diagnostic))
                # Buscar el objeto en la base de datos
                #object = get_object_by_id(id_object)

                # Actualizar el objeto en la base de datos
                #object.status = True
                #update_object(object)
            print("POST - linea 454: ")
            objPatientExam = consultPatientExam(idExam)
            print("POST - linea 454: "+str(idExam))
            print("POST - linea 454: "+str(objPatientExam))
            objPatientExam.diagnostic_general = diagnostic_general
            objPatientExam.save()
            print("line 382 - ExamSample: ")
            ReportExam01.getPDF(request.user.id,request.user.username,idExam)
            #print("line 383 - idExam: " + str(idExam))
            #if generate_pdf(request.user.id,request.user.username,idExam):
            #    print("generate_pdf 385 Exams: ")
            #    print("request.user.id 387 Exams: " + str(request.user.id))
            #    print("request.user.username 387 Exams: " + str(request.user.username))
            #    print("idExam 388 idExams: " + str(idExam))
            #    response = pdf_download(request.user.id,request.user.username,idExam)
            context = { 'company':company_user,
                        #'identification':objPatient[0]['identification'],
                        #'birthday':birthday,
                        #'full_name':objPatient[0]['full_name'],
                        #'typeExam':consultTypeExam(objExamPatient[0]['type_exam_id']),
                        #'idExam':idExam,
                        #'listSamplesExam':listSamplesExam
            }
            return redirect("home")
        if request.method == 'GET':
            print("linea 419: GET examsSelect")
            idExam = request.GET.get('idExam')
            print("linea 421: GET idExam: " + idExam)
            objExamPatient = PatientExam.objects.filter(id=idExam,company=company_user.id).values()
            objPatient = consultPatientObj(objExamPatient[0]['patient_id'])
            listSamplesExam = ExamSample.objects.filter(patientexam_id=idExam)
            birthday = objPatient[0]['birthday'].strftime('%Y-%m-%d')
            diagnostic_general = objExamPatient[0]['diagnostic_general']
            context = { 'company':company_user,
                        'identification':objPatient[0]['identification'],
                        'birthday':birthday,
                        'full_name':objPatient[0]['full_name'],
                        'typeExam':consultTypeExam(objExamPatient[0]['type_exam_id']),
                        'idExam':idExam,
                        'listSamplesExam':listSamplesExam,
                        'diagnostic_general': diagnostic_general,
            }
            return render(request,'reports/examsSelect.html',context)
    except Exception as e:
        return render(request, 'reports/examsSelect.html', {'message' : e,'company':company_user})

@login_required
@csrf_exempt
def saveExams(request,idExam):
    print("saveExams - linea 256: ")
    company_user = Company.objects.filter(user_id=request.user.id).first()
    try:
        if request.method == 'POST':
            print("saveExams - linea 260: ")
            return redirect("home")
        if request.method == 'GET':
            print("saveExams - linea 263: ")
            return redirect("home")
    except Exception as e:
        return render(request, 'reports/examsSelect.html', {'message' : e,'company':company_user})

@login_required
@csrf_exempt
def guardar_select_diagnostic(request):
    try:
        company_user = Company.objects.filter(user_id=request.user.id).first()
        print("Dentro de Guardar-captura: linea 63")
        if request.method == 'POST':
            # Obtiene los datos del Paciente
            listSamplesExam = json.loads(request.POST.get('listSamplesExam'))
            
            print("listSamplesExam: "+str(listSamplesExam))
            # Devuelve una respuesta de éxito
            return JsonResponse({'success': 'Datos guardados con éxito'}, status=200)
        else:
            # Si se recibe un método de solicitud diferente, envía una respuesta de error
            return JsonResponse({'error': 'Método no permitido'}, status=405)
    except HttpResponseServerError as message:
        print("error: "+ str(message))

@login_required
def download_pdf(request):
    identification = str(request.GET.get('identification'))
    #print("identification: " + str(request.GET.get('identification')))
    # Obtener la ruta del archivo PDF
    pdf_path = os.path.join(settings.MEDIA_EXAM_USUARIOS_ROOT + request.user.username + '/' + identification + '_' + dateNowEcuador() , identification + '_EXAM_'+ str(dateNowEcuador()) +'.pdf')
    #print('pdf_path: ',pdf_path)
    filename = (identification +'_EXAM_'+ str(dateNowEcuador()))+'.pdf'
    print("filename: "+filename)
    # Abrir el archivo y leer su contenido
    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()

    # Crear una respuesta HTTP con el contenido del PDF
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="'+filename+'"'
    return response

@transaction.atomic
def record_diagnostic(request):
    if request.method == 'POST':
        diagnostic = request.POST.get('diagnostic')
        identification = request.POST.get('identification')
        #print("434 - request: "+str(diagnostic))
        #print("434 - request: "+str(identification))
        objePatientExam = PatientExam.objects.get(identification=identification,date_exam=dateNowEcuador())
        if objePatientExam:
            objePatientExam.diagnostic = diagnostic
            objePatientExam.save()
        else:
            return JsonResponse({'success': False,'message':'No se guardo o actualizo el Diagnostico'})
        #return JsonResponse({'success': True,'message':'Se guardo o actualizo el Diagnostico'})
    return JsonResponse({'success': True,'message':'Se guardo o actualizo el Diagnostico'})

def abrir_pdf(request, exam_id):
    print("exam_id: "+str(exam_id))
    exam = PatientExam.objects.get(id=exam_id)
    #pdf_url = exam.exam_url
    #exam = get_object_or_404(PatientExam, id=exam_id)
    file_path = exam.exam_url  # Obtener la ruta del archivo PDF desde el campo exam_url

    # Realiza alguna validación adicional si es necesario
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    #return redirect(pdf_url)

@login_required
@csrf_exempt
def cancel(request):
    return redirect('home')