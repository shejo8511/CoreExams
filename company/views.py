import json
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.paginator import Paginator, Page
from .models import Company, Membership, Country, Province, City
from .forms import CompanyForm, MembershipForm, CountryForm, ProvinceForm, CityForm
from user.forms import CustomUserChangeForm

# Create your views here.
@login_required
@csrf_exempt
def membership(request):
    try:
        company_user = Company.objects.filter(user_id=request.user.id).first()
        if request.method == 'POST':
            #POST
            membership_form = MembershipForm(request.POST)
            if membership_form.is_valid():
                membership_form.save()
                return redirect(request, 'membership/list_membership.html',{'company': company_user})
            else:
                if membership_form.errors:
                    message_errMemb = membership_form.errors.as_text()
                    return render(request,'membership/membership.html',{'message':message_errMemb,'membership_form':membership_form,'company':company_user})
        else:
            #GET
            membership_form = MembershipForm()
            print('GET - line30')
            return render(request,'membership/membership.html',{'company': company_user,'membership_form':membership_form})
    except Exception as e:
        print('Exeption: ' + str(e))
        return render(request, 'membership/membership.html', {'message' : e,'membership_form': membership_form,'company':company_user})

@login_required
def listMembership(request):
    company = Company.objects.filter(user_id=request.user.id).first()
    if company:
        list_membership = Membership.objects.filter(enabled=1).order_by('cost')
        paginator = Paginator(list_membership, 10)  # Especifica el número de elementos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual de los parámetros de la URL
        page = paginator.get_page(page_number)  # Obtiene la página solicitada
        context = {
            'list_membership':list_membership,
            'company':company,
            'page':page,
            }
        return render(request,'membership/list_membership.html', context)

@login_required
@csrf_exempt
def country(request):
    try:
        company_user = Company.objects.filter(user_id=request.user.id).first()
        if request.method == 'POST':
            country_form = CountryForm(request.POST)
            if country_form.is_valid():
                country_form.save()
                return redirect('/company/location/country/list_country/',{'company': company_user})
            else:
                if country_form.errors:
                    message_errMemb = country_form.errors.as_text()
                    return render(request,'location/country/country.html',{'message':message_errMemb,'country_form':country_form,'company':company_user})
        if request.method == 'GET':
            country_form = CountryForm()
            return render(request,'location/country/country.html',{'company': company_user,'country_form':country_form})
            
    except Exception as e:
        return render(request, 'location/country/country.html', {'message' : e,'country_form': country_form,'company':company_user})
        
@login_required
def listCountry(request):
    company = Company.objects.filter(user_id=request.user.id).first()
    if company:
        list_country = Country.objects.filter(enabled=1).order_by('name')
        print("list_country: "+str(list_country))
        paginator = Paginator(list_country, 5)  # Especifica el número de elementos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual de los parámetros de la URL
        page = paginator.get_page(page_number)  # Obtiene la página solicitada
        print("paginator: "+str(paginator))
        print("page_number: "+str(page_number))
        print("page: "+str(page))
        context = {
            #'list_country':list_country,
            'page_objects': page.object_list,
            'company':company,
            'page':page,
            }
        return render(request,'location/country/list_country.html', context)

@login_required
@csrf_exempt
def province(request):
    try:
        company_user = Company.objects.filter(user_id=request.user.id).first()
        country_list = Country.objects.filter(enabled=1)
        if request.method == 'POST':
            province_form = ProvinceForm(request.POST)
            if province_form.is_valid():
                province = province_form.save(commit=False)  # Evita guardar de inmediato
                province.country = province_form.cleaned_data['country']  # Asigna el país seleccionado
                province_form.save()
                return redirect('/company/location/province/list_province/',{'company': company_user, 'country_list': country_list,})
            else:
                if province_form.errors:
                    message_errMemb = province_form.errors.as_text()
                    return render(request,'location/province/province.html',{'message':message_errMemb,'province_form':province_form,'company':company_user,'country_list': country_list,})
        if request.method == 'GET':
            province_form = ProvinceForm()
            return render(request,'location/province/province.html',{'company': company_user,'province_form':province_form,'country_list': country_list,})
            
    except Exception as e:
        return render(request, 'location/province/province.html', {'message' : e,'province_form': province_form,'company':company_user,'country_list': country_list,})

@login_required
def listProvince(request):
    company = Company.objects.filter(user_id=request.user.id).first()
    if company:
        list_province = Province.objects.filter(enabled=1).order_by('name')
        paginator = Paginator(list_province, 5)  # Especifica el número de elementos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual de los parámetros de la URL
        page = paginator.get_page(page_number)  # Obtiene la página solicitada
        context = {
            'page_objects': page.object_list,
            'company':company,
            'page':page,
            }
        return render(request,'location/province/list_province.html', context)

def ajax_provinces_city(request,country_id):
    listProvince = Province.objects.filter(country=country_id).order_by('name')
    resListProvince = list(listProvince.values('id', 'name'))
    return JsonResponse({
        'province' : resListProvince,
    })

def ajax_provinces(request,company_id,country_id):
    listProvince = Province.objects.filter(country=country_id).order_by('name')
    resListProvince = list(listProvince.values('id', 'name'))
    return JsonResponse({
        'province' : resListProvince,
    })

def ajax_citys(request,company_id,province_id):
    listCity = City.objects.filter(province=province_id).order_by('name')
    resListCity = list(listCity.values('id', 'name'))
    return JsonResponse({
        'city' : resListCity,
    })

@login_required
@csrf_exempt
def city(request):
    try:
        company_user = Company.objects.filter(user_id=request.user.id).first()
        country_list = Country.objects.filter(enabled=1)
        province_list = Province.objects.filter(enabled=1)
        if request.method == 'POST':
            city_form = CityForm(request.POST)
            if city_form.is_valid():
                city = city_form.save(commit=False)  # Evita guardar de inmediato
                city.country = city_form.cleaned_data['country']  # Asigna el país seleccionado
                city.province = city_form.cleaned_data['province']  # Asigna el province seleccionado
                city_form.save()
                return redirect('/company/location/city/list_city/',{'company': company_user, 'country_list': country_list,})
            else:
                if city_form.errors:
                    message_errMemb = city_form.errors.as_text()
                    return render(request,'location/city/city.html',{'message':message_errMemb,'city_form':city_form,'company':company_user,'country_list': country_list,})
        if request.method == 'GET':
            city_form = ProvinceForm()
            return render(request,'location/city/city.html',{'company': company_user,'city_form':city_form,'country_list': country_list,})
            
    except Exception as e:
        return render(request, 'location/city/city.html', {'message' : e,'city_form': city_form,'company':company_user,'country_list': country_list,})

@login_required
def listCity(request):
    company = Company.objects.filter(user_id=request.user.id).first()
    if company:
        list_city = City.objects.filter(enabled=1).order_by('name')
        paginator = Paginator(list_city, 5)  # Especifica el número de elementos por página
        page_number = request.GET.get('page')  # Obtiene el número de página actual de los parámetros de la URL
        page = paginator.get_page(page_number)  # Obtiene la página solicitada
        context = {
            'page_objects': page.object_list,
            'company':company,
            'page':page,
            }
        return render(request,'location/city/list_city.html', context)

def listExams(request):
    pass

@login_required
@csrf_exempt
def company_edit(request, company_id):
    try:
        company = Company.objects.filter(id=company_id).first()
        country_list = Country.objects.filter(enabled=1)
        print(" company.logo: " + str(company.logo))
        if company:
            user = User.objects.filter(id=company.user_id).first()
        
        if request.method == 'POST':
            print("POST")
            company_form = CompanyForm(request.POST,request.FILES, instance=company)
            
            user_form = CustomUserChangeForm(request.POST, instance=user)
            if company_form.is_valid() and user_form.is_valid():
                company = company_form.save(commit=False)  # Evita guardar de inmediato
                company.country = company_form.cleaned_data['country']
                company.province = company_form.cleaned_data['province']
                company.city = company_form.cleaned_data['city']
                company_form.save()
                user_form.save()
                # Redirigir a una página de éxito o realizar cualquier otra acción necesaria
                return redirect('home')
        else:
            company_form = CompanyForm(instance=company)
            print("company_form: "+str(company_form))
            print("company.country: "+str(company.country))
            print("company.province: "+str(company.province))
            print("company.city: "+str(company.city))
            user_form = CustomUserChangeForm(instance=user)
            
        context = {
            'company': company,
            'logo': company.logo,
            'company_form': company_form,
            'user_form': user_form,
            'country_list': country_list,
            'country_id': company.country.id,
            'province_id': company.province.id,
            'city_id': company.city.id
            #'logos':settings.LOGOS,
        }
        return render(request,'company_edit.html',context)
        #return render(request, 'register.html', {'user_form': user_form, 'company_form': company_form})
    except Exception as e:
        print("566")
        context = {
            'message' : e,
            'company': company,
            'logo': company.logo,
            'company_form': company_form,
            'user_form': user_form,
            'country_list': country_list
            #'logos':settings.LOGOS,
        }
        return render(request, 'register.html',context) #{'message' : e,'user_form': user_form, 'company_form': company_form,'company':company})
