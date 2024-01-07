from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

#Entidad Membresia o planes
class Membership(models.Model):

    name = models.CharField(verbose_name='Nombre',max_length=50,unique=True)
    description = models.TextField(max_length=10000)
    cost = models.DecimalField(max_digits=7, decimal_places=2)
    connections = models.IntegerField(blank=True, null=True)
    # Log
    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='memb_create_by', null=True)
    date_creation = models.DateTimeField(auto_now=True,null=True)
    update_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='memb_update_by', null=True)
    date_updated = models.DateTimeField(auto_now_add=True,null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Membresia'
        verbose_name_plural = 'Membresias'
        ordering = ('cost',)
    
    def __str__(self):
        return self.name 

#Entidad Pais
class Country(models.Model):

    name = models.CharField(verbose_name='Nombre Pais',max_length=50,unique=True)
    # Log
    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='coun_create_by', null=True)
    date_creation = models.DateTimeField(auto_now=True,null=True)
    update_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='coun_update_by', null=True)
    date_updated = models.DateTimeField(auto_now_add=True,null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        ordering = ('name',)
    
    def __str__(self):
        return self.name

#Entidad Provincia
class Province(models.Model):

    name = models.CharField(verbose_name='Nombre Provincia',max_length=50)
    country = models.ForeignKey(Country, verbose_name="Pais", on_delete=models.PROTECT, related_name='Pais_Provincia')
    # Log
    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='prov_create_by', null=True)
    date_creation = models.DateTimeField(auto_now=True,null=True)
    update_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='prov_update_by', null=True)
    date_updated = models.DateTimeField(auto_now_add=True,null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['country', 'name'], name='unique_country_province')
        ]
    
    def __str__(self):
        return self.name

#Entidad Ciudad
class City(models.Model):

    name = models.CharField(verbose_name='Nombre Ciudad',max_length=50)
    country = models.ForeignKey(Country, verbose_name="Pais", on_delete=models.PROTECT, related_name='Pais_Ciudad')
    province = models.ForeignKey(Province, verbose_name="Provincia", on_delete=models.PROTECT, related_name='Provincia_Ciudad')
    # Log
    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='city_create_by', null=True)
    date_creation = models.DateTimeField(auto_now=True,null=True)
    update_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='city_update_by', null=True)
    date_updated = models.DateTimeField(auto_now_add=True,null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(fields=['country', 'province', 'name'], name='unique_country_province_ciudad')
        ]
    
    def __str__(self):
        return self.name

#Entidad Compania
class Company(models.Model):

    TYPE_IDENTI = (
        ('CI','CI'),
        ('PASS','PASAPORTE'),
        ('RUC','RUC'),
    )

    company_name = models.CharField(verbose_name='Nombre Empresa',max_length=50)
    name = models.CharField(verbose_name='Nombres',max_length=50)
    last_name = models.CharField(verbose_name='Apellidos',max_length=50)
    identification = models.CharField(verbose_name='Identificacion',max_length=13)
    identification_type = models.CharField(verbose_name='Tipo Identificacion',
                                            max_length=10,
                                            choices=TYPE_IDENTI)
    phone = models.CharField(verbose_name='Celular/Telefono',max_length=10)
    address = models.CharField(verbose_name='Direccion',max_length=500)
    registration_date = models.DateTimeField(verbose_name='Fecha de registro',auto_now=True)
    pay_date = models.DateTimeField(verbose_name='Fecha de Pago',blank=True, null=True)
    court_date = models.DateTimeField(verbose_name='Fecha de Corte',blank=True, null=True)
    logo = models.ImageField(upload_to="logos/",blank=True, null=True)
    #logo = models.CharField(upload_to='logos/',null=True)
    #user = models.ForeignKey(User,verbose_name='Usuario - Empresa',on_delete=models.CASCADE)
    country = models.ForeignKey(Country, verbose_name="Pais", on_delete=models.PROTECT, related_name='Pais')
    province = models.ForeignKey(Province, verbose_name="Provincia", on_delete=models.PROTECT, related_name='Provincia')
    city = models.ForeignKey(City, verbose_name="Ciudad", on_delete=models.PROTECT, related_name='Ciudad')
    membership = models.ForeignKey(Membership, verbose_name="Membresia", on_delete=models.PROTECT, related_name='Membresia')
    user = models.OneToOneField(User, verbose_name='Usuario - Empresa', on_delete=models.PROTECT, related_name='Empresa')
    # Log
    create_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='comp_create_by', null=True)
    date_creation = models.DateTimeField(auto_now=True,null=True)
    update_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='comp_update_by', null=True)
    date_updated = models.DateTimeField(auto_now_add=True,null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ('id','registration_date')
    
    def __str__(self):
        return self.user.username