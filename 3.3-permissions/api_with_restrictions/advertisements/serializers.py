from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Advertisement
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'is_draft', 'favorite_for')

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        opened_qty = Advertisement.objects.\
            filter(creator=self.context["request"].user).\
            filter(status='OPEN').count() >= 10
        if 'status' in data and data['status'] == 'OPEN' and opened_qty:
            raise ValidationError('Невозможно изменить статус объявления,' 
                                  'превышен лимит открытых объявлений')
        elif self.context["view"].action == 'create' and opened_qty:
            raise ValidationError('Невозможно создать объявление,'
                                  'превышен лимит открытых объявлений')
        return data
