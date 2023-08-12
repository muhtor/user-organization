from rest_framework import generics, viewsets
from rest_framework_simplejwt.views import TokenViewBase
from apps.core.api.middleware import APILayer
from apps.core.services.pagination import CustomPagination
from rest_framework.response import Response


class CustomTokenView(TokenViewBase, APILayer):
    """ JWT TokenViewBase View """
    pass


class CustomCreateView(APILayer, generics.CreateAPIView):
    """ Generic Api View """
    pass


class CustomUpdateDestroyView(APILayer, generics.RetrieveUpdateDestroyAPIView):
    """ Generic Api View """
    pass


class CustomListView(APILayer, generics.ListAPIView, CustomPagination):
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



