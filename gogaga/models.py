from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
#from django.db.models.signals import post_save

# Create your models here.
fs = FileSystemStorage(location='/media/', base_url='/drivers/photo')

class Driverprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(storage=fs, height_field=None, width_field=None, max_length=100)
    car_type = models.CharField(max_length=20)
    immatriculation = models.CharField(max_length=15)
    telephone = models.IntegerField(default = 0)
def __str__(self):
        return self.user.username

#def createprofile(sender, **kwargs):
#        if kwargs['created']:
#            driverprofile = Driverprofile.objects.create(driver=kwargs['instance'])

#post_save.connect(createprofile, sender=User)
    
   

class Traveller(models.Model):
    traveller_name = models.CharField(max_length=20)
    traveller_surname = models.CharField(max_length=20)
    traveller_info = models.TextField(max_length=100)
    seats_reserved = models.IntegerField(default = 1)
    traveller_number = models.IntegerField(default = 0)
    reservation_time = models.DateTimeField(auto_now_add=True, null=True)
    ticket= models.ForeignKey('Tickets', null= True, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.traveller_name

    class Meta:
        ordering = ('traveller_surname',)

class Tickets(models.Model):
    published_by= models.ForeignKey(User, related_name='Tickets')
    departure = models.CharField(max_length=20)
    arrival = models.CharField(max_length=20)
    price= models.IntegerField()
    pub_date = models.DateField('date published')
    number_seat = models.IntegerField(default=0)
    departure_time = models.TimeField(null = True)
    

    def __str__(self):
        return self.departure
    
    class Meta:
        ordering = ('published_by',)


# Tickets and Travellers are OneToMany Relationship
#Tickets are sold to Travellers
#Each Traveller is entitiled to one Ticket at a time