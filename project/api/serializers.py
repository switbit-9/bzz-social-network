from rest_framework import serializers
from accounts.models import User

from rest_framework.serializers import Serializer
from rest_framework.renderers import JSONRenderer

CHOICES = (
    ("m", "Male"),
    ("f", "Female"),
)

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=True, allow_blank=True, max_length=50)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=CHOICES)
    location = serializers.CharField( required=False)
    birthday = serializers.DateField(required=False)

    class Meta:
        model = User
        exclude = ['password', 'createdDate']


    def create(self, validated_data):
        return User(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance