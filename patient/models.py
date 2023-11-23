from django.db import models
from company.models import Company
from exam.models import TypeExam
from django.conf import settings

# Entidad Ficha Pasiente Examen
class Patient(models.Model):
    full_name = models.CharField(verbose_name='Nombres',max_length=100)
    identification = models.CharField(verbose_name='Identificacion',max_length=10)
    company = models.ForeignKey(Company,verbose_name='Empresa',on_delete=models.PROTECT)
    birthday = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    # Log
    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pat_create_by', null=True)
    date_creation = models.DateTimeField(auto_now=True,null=True)
    update_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='pat_update_by', null=True)
    date_updated = models.DateTimeField(auto_now=True,null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ('id',)

class PatientExam(models.Model):
    patient = models.ForeignKey(Patient,verbose_name='Paciente',on_delete=models.PROTECT)
    type_exam = models.ForeignKey(TypeExam,verbose_name='Tipo Examen',on_delete=models.PROTECT)
    company = models.ForeignKey(Company,verbose_name='Empresa',on_delete=models.PROTECT)
    date_exam = models.DateField(blank=True, null=True)
    exam_url = models.CharField(verbose_name='Url-PDF',max_length=5000,blank=True, null=True)
    diagnostic_general = models.CharField(verbose_name="Diagnostico General", max_length=2500, blank=True, null=True, default="")
    # Log
    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='patex_create_by', null=True)
    date_creation = models.DateTimeField(auto_now=True,null=True)
    update_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='patex_update_by', null=True)
    date_updated = models.DateTimeField(auto_now=True,null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Paciente Examen'
        verbose_name_plural = 'Examenes del Pacientes'
        ordering = ('id',)

class ExamSample(models.Model):
    name = models.CharField(verbose_name='Nombre',max_length=1000)
    patient = models.ForeignKey(Patient,verbose_name='Paciente',on_delete=models.PROTECT)
    type_exam = models.ForeignKey(TypeExam,verbose_name='Tipo Examen',on_delete=models.PROTECT)
    patientexam = models.ForeignKey(PatientExam,verbose_name='Muestras del Paciente',on_delete=models.PROTECT)
    company = models.ForeignKey(Company,verbose_name='Compania',on_delete=models.PROTECT)
    url_folder_sample = models.CharField(verbose_name='Url-Muestra PNG',max_length=5000)
    sample_url = models.ImageField(blank=True, null=True,verbose_name='Url-Muestra PNG')
    save_date = models.DateField(blank=True, null=True)
    select = models.BooleanField(default=False)
    diagnostic = models.CharField(verbose_name="Diagnostico", max_length=2500, blank=True, null=True, default="")
    # Log
    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='patexmt_create_by', null=True)
    date_creation = models.DateTimeField(auto_now=True,null=True)
    update_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='patexmt_update_by', null=True)
    date_updated = models.DateTimeField(auto_now=True,null=True)
    enabled = models.BooleanField(default=True)