from django.shortcuts import render, HttpResponse, redirect

from accounts.models import UserAccount
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from accounts.models import UserAccount
from .forms import UserAccountForm

from .utils import generate_ref_code, send_email
# from .emails import send_verification_email, send_change_password_email

def register_page(request):
    domain_name = request.build_absolute_uri('/')[:-1]

    if request.method == "POST":
        form = UserAccountForm(request.POST)

        if form.is_valid():
            user = form.save()
            
            return redirect('/accounts/login/')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
                    
            return render(request, "accounts/register.html", { 'form': form })
                
    user_form = UserAccountForm()

    context = {
        'form': user_form,
    }

    return render(request, "accounts/register.html", context)


def login_page(request):
    # user = request.user
    domain_name = request.build_absolute_uri('/')[:-1]
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")

        else:
            messages.error(request, f'The email or password is incorrect')

    return render(request, "accounts/login.html")


def logout_page(reqeust):
    logout(reqeust)
    return redirect("/")

# @login_required
def forgot_password(request):
    if request.method == "POST":
        # email = request.POST["email"]
        new_password = request.POST["new_password"]
        conform_new_password = request.POST["confirm_password"]

        # Gate keeping.
        if new_password != conform_new_password:
            messages.error(
                request, "Passwords didn't match, Please try again.")
            return redirect(f"/accounts/forgot_password/")
        # if len(new_password) < 8:
        #     messages.error(
        #         request, "Passwords must contain at least 8 characters.")
        #     return redirect(f"/accounts/forgot_password/")

        # All Correct.

        # OK, Change password.
        request.user.set_password(new_password)
        request.user.save()

        messages.success(request, "Password changed successfully!")
        return redirect('/')

    return render(request, "accounts/forgot_password.html")
