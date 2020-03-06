from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    sprite_id = serializers.IntegerField()

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['sprite_id'] = self.validated_data.get('sprite_id', '')
        return data_dict
