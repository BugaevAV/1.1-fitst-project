from django.contrib.auth.models import User
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Advertisement
from .serializers import AdvertisementSerializer, UserSerializer

from .filters import AdvertisementFilter
from .permissions import IsSuperuserOrOwnerOrReadOnly


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        ads = super().get_queryset()
        if self.request.user.is_anonymous:
            ads = ads.filter(is_draft=False)
        else:
            ads = ads.filter(Q(is_draft=False) | Q(creator=self.request.user))
        return ads

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSuperuserOrOwnerOrReadOnly()]
        return []

    @action(methods=['patch'], detail=True)
    def favorite(self, request, pk=None):
        ad = Advertisement.objects.get(pk=pk)
        u = User.objects.filter(username=request.user)
        if u[0].id != ad.creator_id:
            u[0].favorite.add(ad)
        else:
            return Response('Нельзя добавить в избранное свое объявление')
        return Response(AdvertisementSerializer(ad).data)

    @action(methods=['get'], detail=False)
    def favorite_ads(self, request):
        filtered_obj = Advertisement.objects.filter(creator=request.user).\
            exclude(favorite_for=None)
        filtered_obj = AdvertisementSerializer(filtered_obj, many=True)
        return Response(filtered_obj.data)
