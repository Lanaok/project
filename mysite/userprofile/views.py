from django.shortcuts import render
from .models import user_logged_in_receiver
from allauth.account.signals import user_logged_in
from django.contrib.auth import  get_user_model
def contact(request):
    if request.user.is_authenticated:
        return render(request, "temps/profileview.html")


# Create your views here.
