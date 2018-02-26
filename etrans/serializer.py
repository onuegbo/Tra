from rest_framework import serializers
from etrans.models import Company
from django.contrib.auth.models import User



class CompanySerializer(serializers.ModelSerializer):
    created  = serializers.ReadOnlyField(source='created.username')
    class Meta:
        model = Company
        fields = ('id', 'name', 'location', 'description', 'numero_telephone', 'created')
        
    
    

class UserSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=True, queryset=Company.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'company')