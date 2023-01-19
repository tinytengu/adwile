from django.http.response import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Teaser
from .serializers import (
    TeaserCreateSerializer,
    TeaserViewSerializer,
    TeaserUpdateSerializer,
    TeaserUpdateAdminSerializer,
)
from .permissions import IsOwnerOrAdmin


class TeaserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = Teaser.objects.all()

    def list(self, request, *args, **kwargs):
        """Custom `list` action, redirects to `/my` endpoint if the user is not a staff member."""

        if not self.request.user.is_staff:
            return HttpResponseRedirect("my")

        return super().list(request, *args, **kwargs)

    @action(detail=False)
    def my(self, request: Request):
        """Displays all the user teasers."""

        teasers = self.queryset.filter(author=request.user)

        if (page := self.paginate_queryset(teasers)) is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(teasers, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        """Returns custom action- and role-based serializers."""
        if self.action == "create":
            return TeaserCreateSerializer

        if self.action in ("update", "partial_update"):
            return (
                TeaserUpdateAdminSerializer
                if self.request.user.is_staff
                else TeaserUpdateSerializer
            )

        return TeaserViewSerializer

    def perform_create(self, serializer):
        """Autoassigns `author` field from the logged in user."""
        serializer.save(author=self.request.user)
