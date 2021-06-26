from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import (ComponentsSerializer, FavoriteSerializer,
                             FollowSerializer, PurchasesSerializer)
from prod_h.models import Cart, Favorite, Follow, ListOfIngridients, Recipe


class CreateDestroyMethod(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class FollowViewSet(CreateDestroyMethod):
    """
    Table:  Follow
    Available methods:
        POST, DELETE
    Args:
        author: id
    """
    queryset = Follow.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer
    lookup_field = 'author'

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Follow,
                                     user=request.user,
                                     author=kwargs.get('author')
                                     )
        self.perform_destroy(instance)
        content = {'success': True}
        return Response(content, status=status.HTTP_200_OK)


class FavoriteViewSet(CreateDestroyMethod):
    """
    Table: Favorite
    Available methods:
        POST, DELETE
    Args:
        recipe: id
    """
    queryset = Favorite.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FavoriteSerializer
    lookup_field = 'recipe'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        id = serializer.data['recipe']
        recipe = get_object_or_404(Recipe, id=id)
        recipe.save()

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Favorite,
                                     user=request.user,
                                     recipe=kwargs.get('recipe')
                                     )
        self.perform_destroy(instance)
        content = {'success': True}
        return Response(content, status=status.HTTP_200_OK)


class PurchasesViewSet(CreateDestroyMethod):
    """
    Table: Cart
    Available methods:
        POST, DELETE
    Args:
        item: id
    """
    queryset = Cart.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PurchasesSerializer
    lookup_field = 'item'

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Cart,
                                     customer=request.user,
                                     item=kwargs.get('item')
                                     )
        self.perform_destroy(instance)
        content = {'success': True}
        return Response(content, status=status.HTTP_200_OK)


class ComponentsViewSet(generics.ListAPIView, viewsets.GenericViewSet):
    """
    Search ingredients
    Table: ListOfIngridients
    Available methods:
        GET
    Args:
        query params
    """
    serializer_class = ComponentsSerializer

    def get_queryset(self):
        data = self.request.GET['query']
        if data is not None:
            queryset = ListOfIngridients.objects.filter(name__istartswith=data)
            return queryset
        return ListOfIngridients.objects.none()
