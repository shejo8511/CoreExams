from django.db import models
from django.conf import settings

# Create your models here.
class TypeExam(models.Model):

    name = models.CharField(verbose_name='Nombre',max_length=50,unique=True)
    description = models.TextField(max_length=10000)
     # Log
    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='tyexm_create_by', null=True)
    date_creation = models.DateTimeField(auto_now=True,null=True)
    update_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='tyexm_update_by', null=True)
    date_updated = models.DateTimeField(auto_now_add=True,null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tipo Examen'
        verbose_name_plural = 'Tipos de Examenes'
        ordering = ('name',)
    
    def __str__(self):
        return self.name
