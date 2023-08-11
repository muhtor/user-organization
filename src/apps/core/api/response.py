from rest_framework.response import Response
from rest_framework import permissions, generics
from rest_framework import status


class RequestController(generics.GenericAPIView):

    def get_language(self):
        """
        Public method
        @return: request headers language
        """
        return self.__check_language()

    def __check_language(self):
        """Private method"""
        # header = self.request.headers
        lang = 'en'
        # if 'Accept-Language' in header:
        #     lang = header['Accept-Language'][:2]
        # else:
        #     lang = 'en'
        return lang


class ResponseController(RequestController):
    NOT_FOUND_ERROR = "Not found"

    def success_response(self, results=None, status_code: int = status.HTTP_200_OK):
        # lang = self.get_language() # maybe backend api response localization

        response = {'success': True, 'message': "OK"}
        if results:
            response = {'success': True, 'message': "OK", "results": results}
        return Response(response, status=status_code)

    def error_response(self, msg=None, status_code: int = status.HTTP_404_NOT_FOUND):
        message = msg if msg else self.NOT_FOUND_ERROR
        return Response({'success': False, 'message': message}, status=status_code)

