from django.shortcuts import render, HttpResponse, redirect
from .admin import models
# from accounts.models import UserAccount
from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse

# from .models import GeneralData
# from core.models import Level, Subject
# from courses.models import Chapter

# Custom modules
# from django.contrib import admin
# rmodels = admin.site._registry

import datetime
today = datetime.date.today()


# UTILITY FUNCTIONS
def get_model(name:str): 
    '''Returns the registered array from the admin.py. '''
    for TableClass in models:
        if TableClass.name == name:
            return TableClass
        
    raise ValueError("Table Not Found")

def create_form(model):
    '''Create and return a django ModelForm for the given model'''
    model_obj = model
    class AutoForm(ModelForm):
        class Meta:
            model = model_obj
            fields = "__all__"
            
    return AutoForm

def is_admin(user):
    return user.is_superuser

# VIEW FUNCTIONS
# Dashboard Page
@login_required(login_url="/accounts/login/")
@user_passes_test(is_admin)
def dashboard_page(request):
    # customers = UserAccount.objects.filter()
    return redirect('/admin/table/Testimonial/')
    # context = {
    #     # 'customers': customers.count(),
    #     # 'revenue': load("revenue"),
    #     'tables': models,
    # }
    # return render(request, "customadmin/dashboard.html", context)

# Settings Page.
@login_required(login_url="/accounts/login/")
@user_passes_test(is_admin)
def settings_page(request):
    # general_data = GeneralData.get_or_create()

    # if request.method == "POST":
        # Set price for method 1
        
    return render(request, "customadmin/settings.html")


# TABLES (CRUD) ->
#  - (Create)
@login_required(login_url="/accounts/login/")
@user_passes_test(is_admin)
def create_row_page(request, model_name):
    TableClass = get_model(model_name)
    name = TableClass.name
    model = TableClass.model

    FormClass = create_form(model=model)

    if request.method == "POST":
        form = FormClass(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect(f"/admin/table/{name}")

        else:
            raise ValueError("Invalid Form!")

    form = FormClass()

    context = {
        'model': model,
        'custom_name': name,
        'form':form,

        'tables': models,
    }
    if name == "Sub Chapters":
        levels = Level.objects.all()
        subjects = Subject.objects.all()
        # Create a select input field for levels
        levels_select = '<select name="selected_level" id="id_selected_level">'
        levels_select += f'<option value=""> ---- </option>'
        for level in levels:
            levels_select += f'<option value="{level.id}">{level.name}</option>'
        levels_select += '</select>'

        # Create a select input field for subjects
        subjects_select = '<select name="selected_subject" id="id_selected_subject">'
        subjects_select += f'<option value=""> ---- </option>'
        for subject in subjects:
            subjects_select += f'<option value="{subject.id}">{subject.name}</option>'
        subjects_select += '</select>'
        context["levels"] = levels_select
        context["subjects"] = subjects_select

    return render(request, "customadmin/create_row.html", context)


#  - (Update & Delete)
@user_passes_test(is_admin)
def edit_row_page(request, model_name, id):
    
    # Loading registered values from the admin.py
    TableClass = get_model(model_name)
    # Mendatory
    name = TableClass.name
    model = TableClass.model

    obj = model.objects.get(id=id)

    # Create form for editing.
    FormClass = create_form(model=model)
    
    # Action reqeust
    if request.method == "POST":
        if "save" in request.POST:
            form = FormClass(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form.save()
                return redirect(f"/admin/table/{name}")

            else:
                raise ValueError("Invalid Form")

        elif "delete" in request.POST:
            obj.delete()
            return redirect(f"/admin/table/{name}")
        
    form = FormClass(instance=obj)

    context = {
        'model': model,
        'custom_name': name,
        'obj':obj,
        'form':form,

        'tables': models,
    }
    if name == "Sub Chapters":
        levels = Level.objects.all()
        subjects = Subject.objects.all()
        # Create a select input field for levels
        levels_select = '<select name="selected_level" id="id_selected_level">'
        levels_select += f'<option value=""> ---- </option>'
        for level in levels:
            if level == obj.chapter.level: 
                levels_select += f'<option value="{level.id}" selected>{level.name}</option>'
                continue
            levels_select += f'<option value="{level.id}">{level.name}</option>'

        levels_select += '</select>'

        # Create a select input field for subjects
        subjects_select = '<select name="selected_subject" id="id_selected_subject">'
        subjects_select += f'<option value=""> ---- </option>'
        for subject in subjects:
            if subject == obj.chapter.subject: 
                subjects_select += f'<option value="{subject.id}" selected>{subject.name}</option>'
                continue
            subjects_select += f'<option value="{subject.id}">{subject.name}</option>'
        subjects_select += '</select>'
        context["levels"] = levels_select
        context["subjects"] = subjects_select

    return render(request, "customadmin/edit_row.html", context)


#  - (Read)
@login_required(login_url="/accounts/login/")
@user_passes_test(is_admin)
def show_table_page(request, model_name):
    # Loading registered values from the admin.py
    TableClass = get_model(model_name)

    # Mendatory
    name = TableClass.name
    model = TableClass.model

    # Optionals
    if TableClass.fields:
        # If fields are specified.
        fields = TableClass.fields
    else:
        # Fetch all fields that the model has.
        fields = [f.get_attname() for f in model._meta.fields]

    if TableClass.order_by:
        table = model.objects.order_by(*TableClass.order_by)
    else:
        table = model.objects.all()

    context = {
        'model': model,
        'table_name': model.objects.model._meta.db_table,
        'table': table,
        'name': name,
        'fields': fields,
        
        'tables': models,
    }

    return render(request, "customadmin/tables.html", context)


@user_passes_test(is_admin)
def get_chapters(request):
    subject_id = request.GET.get('subject')
    level_id = request.GET.get('level')
    print("subject_id: ", subject_id)
    print("level_id: ", level_id)
    # Filter chapters based on subject and level
    chapters = Chapter.objects.filter(subject_id=subject_id, level_id=level_id)

    # Create a JSON response
    data = [{'id': chapter.id, 'name': chapter.name} for chapter in chapters]
    return JsonResponse(data, safe=False)

