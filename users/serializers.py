from rest_framework import serializers

from .models import Confirm, Profile
from .validators import IsExistsValidator


STAFF_GROUPS = ('moderator', 'admin')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'username',
                  'email', 'bio', 'role')


class CreateConfirmCodeSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.HiddenField(default='')

    class Meta:
        model = Confirm
        fields = ('email', 'confirmation_code', )


class RetrieveTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = Confirm
        fields = '__all__'
        validators = [
            IsExistsValidator(
                fields=('email', 'confirmation_code', )
            )
        ]
