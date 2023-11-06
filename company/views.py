from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.paginator import Paginator, Page
from .models import Company, Membership
from .forms import CompanyForm, MembershipForm
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
                return render(request, 'membership/list_membership.html',{'company': company_user})
            else:
                if membership_form.errors:
                    message_errMemb = membership_form.errors.as_text()
                    return render(request,'membership/membership.html',{'message':message_errMemb,'membership_form':membership_form,'company':company_user})
        else:
            #GET
            membership_form = MembershipForm()
        print('line36')
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

def listExams(request):
    pass

@login_required
@csrf_exempt
def company_edit(request, company_id):
    try:
        company = Company.objects.filter(id=company_id).first()
        if company:
            user = User.objects.filter(id=company.user_id).first()
        
        if request.method == 'POST':
            print("POST")
            company_form = CompanyForm(request.POST,request.FILES, instance=company)
            user_form = CustomUserChangeForm(request.POST, instance=user)
            if company_form.is_valid() and user_form.is_valid():
                company_form.save()
                user_form.save()
                # Redirigir a una página de éxito o realizar cualquier otra acción necesaria
                return redirect('home')
        else:
            company_form = CompanyForm(instance=company)
            user_form = CustomUserChangeForm(instance=user)

        context = {
            'company': company,
            'company_form': company_form,
            'user_form': user_form,
            #'logos':settings.LOGOS,
        }
        print("company_form: "+str(company_form))
        return render(request,'company_edit.html',context)
        #return render(request, 'register.html', {'user_form': user_form, 'company_form': company_form})
    except Exception as e:
        print("566")
        return render(request, 'register.html', {'message' : e,'user_form': user_form, 'company_form': company_form,'company':company})
