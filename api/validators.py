from rest_framework import serializers

from .models import Confirm


class IsExistsValidator:

    def __init__(self, fields) -> None:
        self.fields = fields

    def __call__(self, fields):
        if not Confirm.objects.filter(**fields).exists():
            raise serializers.ValidationError("not found")
