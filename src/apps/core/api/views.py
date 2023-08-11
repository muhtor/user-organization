from rest_framework.views import APIView


class CustomAPIView(APIView):
    def get(self,request):
        pagenumber = request.GET['pagenum']
        products_per_page = request.GET['productsPerPage']
        pagenum = request.GET['pagenum']