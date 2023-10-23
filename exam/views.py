import os
from os import path
import pytz
import base64
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
#from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.core.paginator import Paginator, Page
#import playsound
import simpleaudio as sa
from datetime import date, datetime
import datetime as dt_datetime
from .models import TypeExam
from .forms import TypeExamForm
from company.models import Company
from .models import TypeExam
from patient.models import Patient, PatientExam, ExamSample
from patient.views import createPatient, createPatientExam, savePatientImg

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
@csrf_exempt
def cancel(request):
    return redirect("home")

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
        print('line36')
        return render(request,'type_exam/type_exam.html',{'company': company_user,'type_exam_form':type_exam_form})
    except Exception as e:
        print('Exeption: ' + str(e))
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
            # Guarda la captura de pantalla en el sistema de archivos
            folder = os.path.join(settings.MEDIA_ROOT_USUARIOS + request.user.username + '/' + idExam + '_' + identification + '_'+ typeExam +'_' + dateNowEcuador())
            if not os.path.exists(folder):
                os.makedirs(folder)
            else:
                with open(os.path.join(folder, identification +'_'+ typeExam +'_'+ dateTimeNowEcuador() +'.jpg'), 'wb') as f:
                    if f.write(imagen_decodificada):
                        name = idExam + '_' + identification + '_'+ typeExam +'_' + dateNowEcuador()
                        idPatient = consultPatient(identification,company_user.id)
                        idTypeExam = consultTypeExamName(typeExam)
                        sample_url = folder + identification +'_'+ typeExam +'_'+ dateTimeNowEcuador() +'.jpg'
                        ResExamSample = savePatientImg(name,idPatient,idTypeExam,idExam,company_user.id,folder,sample_url,request.user.id)
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
def videoStream(request):
    company_user = Company.objects.filter(user_id=request.user.id).first()
    try:
        if request.method == 'POST':
            identification = request.POST.get('identification')
            birthday = request.POST.get('birthday')
            full_name = request.POST.get('full_name')
            typeExam = request.POST.get('typeExam')
            # Crea el Paciente o devulve el paciente si existe
            print("line 177: objPatient; ")
            objPatient = createPatient(identification,full_name,company_user.id,birthday,request.user.id)
            print("line 179: objPatient; "+str(objPatient))
            print("line 180: company_user; "+str(company_user))
            print("line 180: company_user.id; "+str(company_user.id))
            # Verfica que el paciente se creo o devuelve el id del paciente
            if objPatient:
                print("line 184: objPatient; "+str(objPatient))
                patientExam = createPatientExam(objPatient,typeExam,company_user.id,request.user.id)
                print("linea 186: patientExam: "+str(patientExam))
                if os.path.isdir((settings.MEDIA_ROOT_USUARIOS + request.user.username)):
                    #Crear Carpeta
                    nueva_carpeta = str(str(patientExam) + '_' +request.POST.get('identification')) + '_' + str(consultTypeExam(request.POST.get('typeExam'))).upper() + '_' + dateNowEcuador()
                    #directorio = os.getcwd()  # obtiene el directorio actual
                    ruta = os.path.join(settings.MEDIA_ROOT_USUARIOS + request.user.username+'/', nueva_carpeta)  # une el nombre de la carpeta con el directorio
                    if not os.path.isdir(ruta):
                        os.makedirs(ruta)  #crea la carpeta en la ruta especificada
                context = { 'company':company_user,
                        'identification':identification,
                        'birthday':birthday,
                        'full_name':full_name,
                        'typeExam':consultTypeExam(typeExam),
                        'idExam':patientExam}
                return render(request, 'stream/videoStream.html',context)
        if request.method == 'GET':
            #print("linea 202: videoStream")
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

@login_required
@csrf_exempt 
def examsSelect(request):
    print("examsSelect - linea 225: ")
    company_user = Company.objects.filter(user_id=request.user.id).first()
    try:
        if request.method == 'POST':
            print("linea 229: POST ID")
            #print("linea:225: examsSelect: - identification: "+str(request.POST.get('identification'))+" birthday: "+ str(request.POST.get('birthday')) +" full_name: "+str(request.POST.get('full_name'))+" typeExam: "+str(request.POST.get('typeExam'))+" idExam: "+str(request.POST.get('idExam')))
            #identification = request.POST.get('identification')
            #birthday = request.POST.get('birthday')
            #full_name = request.POST.get('full_name')
            #typeExam = request.POST.get('typeExam')
            idExam = request.POST.get('idExam')
            print("examsSelect - linea 236: idExam: "+str(idExam))
            objExamPatient = PatientExam.objects.filter(id=idExam,company=company_user.id).values()
            #print("linea 237: objExamPatient " + str(objExamPatient))
            #print("linea 238: patient " + str(objExamPatient[0]['patient_id']))
            objPatient = consultPatientObj(objExamPatient[0]['patient_id'])
            listSamplesExam = ExamSample.objects.filter(patientexam=idExam)
            print("linea 242: listSamplesExam " + str(listSamplesExam))
            print("linea 243: birthday " + str(objPatient[0]['birthday'].strftime("%d/%m/%Y")))
            #print("linea 234: patient " + str(objExamPatient.patient))
            context = { 'company':company_user,
                        'identification':objPatient[0]['identification'],
                        'birthday':objPatient[0]['birthday'].strftime("%d/%m/%Y"),
                        'full_name':objPatient[0]['full_name'],
                        'typeExam':consultTypeExam(objExamPatient[0]['type_exam_id']),
                        'idExam':idExam,
                        'listSamplesExam':listSamplesExam
            }
            #print("linea:238: examsSelect: - identification: "+str(identification)+" birthday: "+ str(birthday) +" full_name: "+str(full_name)+" typeExam: "+str(typeExam)+" idExam: "+str(idExam))
            print("linea 239: ")
            return render(request,'reports/examsSelect.html',context)
        if request.method == 'GET':
            #print(" examsSelect linea:258 - GET")
            return redirect("home")
    except Exception as e:
        return render(request, 'stream/videoStream.html', {'message' : e,'company':company_user})

@login_required
def download_pdf(request):
    identification = str(request.GET.get('identification'))
    #print("identification: " + str(request.GET.get('identification')))
    # Obtener la ruta del archivo PDF
    pdf_path = os.path.join(settings.MEDIA_ROOT_USUARIOS + request.user.username + '/' + identification + '_' + dateNowEcuador() , identification + '_EXAM_'+ str(dateNowEcuador()) +'.pdf')
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

@login_required
def generate_pdf(request):
    #if method == "GET":
    identification = request.GET.get('identification')
    #filename_pdf = settings.MEDIA_ROOT_USUARIOS +request.user.username+'/'+identification+'_'+dateNowEcuador()+'/'+identification+'_EXAM_'+dateNowEcuador()+".pdf"
    #print("filename_pdf: "+ str(filename_pdf))
    #imagenes_jpg = [archivo for archivo in os.listdir(settings.MEDIA_ROOT_USUARIOS + request.user.username +'/'+ identification +'_'+ dateNowEcuador()) if archivo.endswith(".jpg")]
    #imagenes_jpg_bytes = [open(settings.MEDIA_ROOT_USUARIOS +request.user.username +'/'+ identification +'_'+ dateNowEcuador() +'/'+ archivo, "rb").read() for archivo in imagenes_jpg]
    
    #lista_imagenes = imagenes_jpg_bytes

    # Obtenemos la lista de imágenes
    #ruta_imagenes = settings.MEDIA_ROOT_USUARIOS +request.user.username+'/'+identification+'_'+dateNowEcuador()
    #lista_imagenes = [archivo for archivo in os.listdir(settings.MEDIA_ROOT_USUARIOS + request.user.username +'/'+ identification +'_'+ dateNowEcuador()) if archivo.endswith(".jpg")]
    #print("ruta_imagenes: " + ruta_imagenes)
    #print("lista_imagenes: " + str(lista_imagenes))

    #-----------------------------
    # Ruta donde se encuentran las imágenes
    ruta_imagenes = str(settings.MEDIA_ROOT_USUARIOS + request.user.username +'/'+ identification +'_'+ dateNowEcuador())
    #nombre_pdf = str(identification + '_EXAM_'+ dateNowEcuador()+'.pdf')
    ruta_pdf = settings.MEDIA_ROOT_USUARIOS +request.user.username+'/'+identification+'_'+dateNowEcuador()+'/'+identification+'_EXAM_'+dateNowEcuador()+".pdf"
    #imagenes = [os.path.join(ruta_imagenes, f) for f in os.listdir(ruta_imagenes) if os.path.isfile(os.path.join(ruta_imagenes, f))]
    imagenes = [archivo for archivo in os.listdir(settings.MEDIA_ROOT_USUARIOS + request.user.username +'/'+ identification +'_'+ dateNowEcuador()) if archivo.endswith(".jpg")]
    print("imagenes 240: "+str(imagenes))
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

    #pdf.setFillColorRGB(0.14, 0.59, 0.74)
    #pdf.drawString(60, 750, "Videojuegos")
    #variables = "UNO","DOS"
    
    # Escribir cabecera
    #pdf.drawString(50, 750, titulo)
    #pdf.drawString(50, 730, f"Variable 1: {variables[0]}")
    #pdf.drawString(50, 710, f"Variable 2: {variables[1]}")

    # Agregar imágenes al PDF
    #for i in range(len(imagenes)):
    #    if i % 4 == 0:
    #        pdf.showPage()

        # Calcular coordenadas de la imagen
    #    j = i % 4
    #    x = (j % 2) * (A4[1] / 2) + 25
    #    y = (j // 2) * (A4[0] / 2) + 75

        # Abrir imagen y dibujarla en el PDF
        #imagen = Image.open(imagenes[i])
        #pdf.drawImage(ruta_imagenes +'/'+ imagenes[i], x, y, A4[1] / 2, A4[0] / 2)
    #    pdf.drawImage(ruta_imagenes +'/'+ imagenes[i], x, y, 2.5*inch, 2.5*inch)
    # Guardar y cerrar el PDF
    pdf.save()
    download_pdf(request)

    #-----------------------------

    # Creamos el objeto PDF
    #nombre_pdf = identification+'_EXAM_'+dateNowEcuador()+".pdf"
    #print("nombre_pdf: " + nombre_pdf)
    #pdf = canvas.Canvas(nombre_pdf, pagesize=A4)

    # Definimos los valores de la cabecera
    #titulo = "Título del documento"
    #fecha = dateTimeNowEcuador()
    #variable1 = "Valor de la variable 1"
    #variable2 = "Valor de la variable 2"

    # Escribimos la cabecera
    #pdf.setFont("Helvetica-Bold", 16)
    #pdf.drawCentredString(4.25*inch, 10.5*inch, titulo)

    #pdf.setFont("Helvetica", 12)
    #pdf.drawString(0.75*inch, 10*inch, "Fecha: " + fecha)
    #pdf.drawString(5.5*inch, 10*inch, "Variable 1: " + variable1)
    #pdf.drawString(5.5*inch, 9.75*inch, "Variable 2: " + variable2)

    # Escribimos las imágenes
    #posicion_x = 3.75
    #posicion_y = 15.5

    #for i, imagen in enumerate(lista_imagenes):
    #    if i % 4 == 0 and i != 0:
    #        pdf.showPage()
    #        posicion_x = 0.75
    #        posicion_y = 8.5
    #    print("ruta_imagenes: " + ruta_imagenes)
    #    print("imagen: " + imagen)
    #    ruta_completa_imagen = os.path.join(ruta_imagenes, imagen)
    #    print("ruta_completa_imagen: " + ruta_completa_imagen)
    #    pdf.drawImage(ruta_completa_imagen, posicion_x*inch, posicion_y*inch, 2.5*inch, 2.5*inch)

    #    if (i + 1) % 2 == 0:
    #        posicion_y -= 2.75
    #        posicion_x = 0.75
    #    else:
    #        posicion_x += 2.75
    
    # Cerramos el objeto PDF
    #pdf.save()

    # Añadimos el contenido al PDF existente
    #ruta_pdf_existente = "ruta/del/pdf/existente.pdf"
    #ruta_pdf_existente = filename_pdf
    #print("ruta_pdf_existente: "+ruta_pdf_existente)
    #pdf_existente = PdfFileReader(open(ruta_pdf_existente, "rb"))
    #pdf_nuevo = PdfFileReader(open(nombre_pdf, "rb"))
    #pdf_salida = PdfFileWriter()

    #for i in range(pdf_nuevo.getNumPages()):
    #    pagina_nueva = pdf_nuevo.getPage(i)
    #    pagina_existente = pdf_existente.getPage(i)
    #    pagina_existente.mergePage(pagina_nueva)
    #    pdf_salida.addPage(pagina_existente)

    #with open(ruta_pdf_existente, "wb") as f:
    #    pdf_salida.write(f)
        
    # Borramos el PDF temporal
    #os.remove(nombre_pdf)

    #with open(settings.MEDIA_ROOT_USUARIOS +request.user.username+'/'+identification+'_'+dateNowEcuador()+'/'+identification+'_EXAM_'+dateNowEcuador()+".pdf", "wb") as documento:
    #    documento.write(titulo)
        #print("imagenes_jpg: "+str(imagenes_jpg))
        #print("imagenes_jpg_bytes: "+str(imagenes_jpg_bytes))
    #    if imagenes_jpg and imagenes_jpg_bytes:
    #        documento.write(img2pdf.convert(imagenes_jpg_bytes))
    #        print("Existen Imagenes")
    #    else:
    #        print("No Existen Imagnes disponibles")
    download_pdf(request)
    return JsonResponse({'mensaje': 'La función se ejecutó correctamente'})

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

# Clase para Reporte.
class ReportExam01(View):

    @login_required
    @csrf_exempt
    def get(request):
        print("get-ReportExam01")
        identification = str(request.GET.get('identification'))
        ##=================##
        #-----------------------------
        #Ruta donde se encuentran las imágenes
        ruta_dir_pdf = str(settings.MEDIA_ROOT_USUARIOS + request.user.username +'/'+ identification +'_'+ dateNowEcuador()+'/')
        ruta_imagenes = str(settings.MEDIA_ROOT_USUARIOS + request.user.username +'/'+ identification +'_'+ dateNowEcuador()+'/')
        #nombre_pdf = str(identification + '_EXAM_'+ dateNowEcuador()+'.pdf')
        #ruta_pdf = settings.MEDIA_ROOT_USUARIOS +request.user.username+'/'+identification+'_'+dateNowEcuador()+'/'+identification+'_EXAM_'+dateNowEcuador()+".pdf"
        #imagenes = [os.path.join(ruta_imagenes, f) for f in os.listdir(ruta_imagenes) if os.path.isfile(os.path.join(ruta_imagenes, f))]
        imagenes = [archivo for archivo in os.listdir(settings.MEDIA_ROOT_USUARIOS + request.user.username +'/'+ identification +'_'+ dateNowEcuador()) if archivo.endswith(".jpg")]
        grupos = [imagenes[i:i+3] for i in range(0, len(imagenes), 3)]
        #primeros_seis_imagenes = imagenes[:6]
        print("grupos 394: "+str(grupos))
        ##=================##
        
        company = Company.objects.get(user_id=request.user.id)
        examPatient = PatientExam.objects.get(identification=identification,date_exam=dateNowEcuador())
        #nombreCompany = company.company_name
        logo = company.logo #settings.STATIC_IMG_URL + 'noLogo.jpg'
        logo_url = settings.MEDIA_ROOT + str(logo)
        #print("490 logo: "+str(logo_url))
        #print("examPatient: " + str(examPatient.diagnostic))
        #print("identification: " + str(identification))
        #print("*args: " + str(*args))
        #print("**kwargs: " + str(**kwargs))
        data = {
            'examPatient': examPatient,
            'diagnostic':examPatient.diagnostic,
            'logo':logo_url,
            'company': company,
            #'imagenes':primeros_seis_imagenes,
            'grupos':grupos,
            'ruta':ruta_imagenes
        }
        #request_path = request.path
        #print("request_path")
        #print(request_path)
        # Guarda el PDF en la ruta especificada
        
        pdf = render_to_pdf('reports/reportExam01.html', data)

        if pdf:
            nombrePDF = identification+'_'+dateNowEcuador()+'.pdf'
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