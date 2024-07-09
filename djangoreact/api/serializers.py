from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate
from myapp.models import Languages, Reasons


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'

class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Must include username and password')
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('User not found')
        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            raise serializers.ValidationError('Incorrect username or password')
        
        attrs['user'] = user
        return attrs
    

class LASER_QueriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LASER_Queries
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = '__all__'

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reasons
        fields = '__all__'


