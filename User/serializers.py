from User.models import UserData
from rest_framework import serializers

class UserDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserData
		fields = ('username', 'name', 'password', 'email')
