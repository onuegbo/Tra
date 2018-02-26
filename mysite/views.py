from django.shortcuts import redirect
from django.shortcuts import render_to_response

def login_redirect(request):
    return redirect('/etrans/login')

