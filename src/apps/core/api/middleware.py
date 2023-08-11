from .exceptions import CustomValidationError
from .response import ResponseController
from rest_framework import status


class APIMiddleware(ResponseController):
    """ Layer between view and response (Middleware) """

    ASC = "id"
    DESC = "-id"

    ORDER_BY = {
        "ASC": ASC,
        "DESC": DESC
    }

    def order_by_lookup(self, by):
        return self.ORDER_BY.get(by, self.DESC)

    def get_object_pk(self):
        if self.kwargs:
            try:
                return self.get_object()
            except Exception as e:
                raise CustomValidationError(msg=str(e.args[0]), status_code=status.HTTP_404_NOT_FOUND)
        else:
            raise CustomValidationError(msg="Expected URL keyword argument ID")
