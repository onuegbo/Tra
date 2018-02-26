from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegistrationForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Driverprofile, Traveller, Tickets
from django.db.models import F, Count, Value


# Create your views here.

def home(request):
    pubs = Tickets.objects.all()
    return render(request, 'gogaga/home.html', {'pubs': pubs})

def pub_details(request, pub_id):
    pub_details = get_object_or_404(Publication, pk=pub_id)
    return render(request, 'gogaga/clients.html', {'pub_details': pub_details})




def reserved(request, ticket_id):
    ticket = get_object_or_404(Tickets, pk=ticket_id)
    try:
        reserved_ticket = ticket.traveller_set.create(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the traveller creating  form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        reserved_ticket.seats_reserved = F('seats_reserved') - 1
        reserved_ticket.save()
        reserved_ticket.refresh_from_db()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('gogaga:reserved', args=(question.id,)))
















#*******************************Auth*****************************************************************************#

def register(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':
     # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gogaga')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm()

    return render(request, 'gogaga/register.html', {'form': form})

@login_required
def profile(request):
    args = {'user': request.user}
    return render(request, 'gogaga/profile.html', args)

@login_required
def profile_edit(request):
     # If this is a POST request then process the Form data
    if request.method == 'POST':
     # create a form instance and populate it with data from the request:
        form = EditProfileForm(request.POST, instance= request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/gogaga/profile')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditProfileForm(instance= request.user)

    return render(request, 'gogaga/profile_edit.html', {'form': form})
@login_required
def changepassword(request):
     # If this is a POST request then process the Form data
    if request.method == 'POST':
     # create a form instance and populate it with data from the request:
        form = PasswordChangeForm(data=request.POST, user= request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/gogaga/profile')
        else:
            return HttpResponseRedirect('gogaga/changepassword.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordChangeForm(user= request.user)

    return render(request, 'gogaga/changepassword.html', {'form': form})




