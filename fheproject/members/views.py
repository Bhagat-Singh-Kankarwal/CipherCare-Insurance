from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm


from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


# Create your views here.

def activation_sent(request):

    return render(request, "authenticate/account_activation_sent.html", {})



def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive initially
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('authenticate/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, message)  # Send activation email
            messages.success(request, ("Registration complete..."))
            return redirect('activation_sent')  # Redirect to registration complete page
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')  # Redirect to desired page after activation
    else:
        return render(request, 'authenticate/account_activation_invalid.html')




def logout_user(request):

    logout(request)
    messages.success(request, ("You were logged out..."))

    return redirect('home')



def login_user(request):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('home')
            # Redirect to a success page.
            
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There was an error logging in..."))
            return redirect('login')
        
    else:
        return render(request, 'authenticate/login.html', {})