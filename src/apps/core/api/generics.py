from rest_framework import permissions, generics, viewsets
from rest_framework.views import APIView
from apps.core.api.middleware import APIMiddleware
from apps.core.services.pagination import CustomPagination
from rest_framework.response import Response


class CustomAPIView(APIMiddleware, APIView):
    """ Generic Api View """
    pass


class CustomGenericAPIView(APIMiddleware, generics.GenericAPIView):
    """ Generic Api View """
    pass


class CustomCreateAPIView(APIMiddleware, generics.CreateAPIView):
    """ Generic Api View """
    pass


class CustomListView(APIMiddleware, generics.ListAPIView, CustomPagination):
    """ Pagination List View """

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if qs:
            result = self.paginated_queryset(qs, request)
            serializer = self.serializer_class(result, many=True)
            response = self.paginated_response(data=serializer.data)
            return Response(response)
        else:
            return Response({"success": True, "code": 0, "message": "OK", "results": []})


class CustomSimpleListView(APIMiddleware, generics.ListAPIView):
    """ Simple List View (no paginate) """

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        data = {
            "success": True,
            "code": 0,
            "message": "OK,",
            "results": serializer.data,
        }
        return Response(data)


class CustomUpdateAPIView(APIMiddleware, generics.UpdateAPIView):
    """ Create Update API View """
    pass


class CustomRetrieveUpdateAPIView(APIMiddleware, generics.RetrieveUpdateAPIView):
    """ Create Retrieve Update API View """
    pass


class CustomCrudView(APIMiddleware, generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """ Create Retrieve Update API View """
    pass


class CustomDestroyAPIView(APIMiddleware, generics.DestroyAPIView):
    """ Create CRUD API View """
    pass


class CustomCrudViewSet(APIMiddleware, viewsets.ViewSet):
    """ Custom CRUD ViewSet Mixin """

    def list(self, request):
        """ LIST """
        pass

    def retrieve(self, request, pk=None):
        """ GET """
        pass

    def create(self, request):
        """ POST """
        pass

    def update(self, request, pk=None):
        """ PUT """
        pass

    def partial_update(self, request, pk=None):
        """ PATCH """
        pass

    def destroy(self, request, pk):
        """ DELETE """
        pass




