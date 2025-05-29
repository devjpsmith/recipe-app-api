"""
Views for the recipe apis
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe apis"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def validate_immutable_fields(self, data):
        """Make sure client is not modifying fields they shouldn't be"""
        if 'user' in data:
            raise ValidationError({'user': 'You cannot set this field'})

    def get_serializer_class(self):
        """Return recipe serializer class"""
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        self.validate_immutable_fields(request.data)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.validate_immutable_fields(request.data)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.validate_immutable_fields(request.data)
        return super().partial_update(request, *args, **kwargs)
