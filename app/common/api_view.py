from flask.views import MethodView

from app.controllers.api import FavQsApi


class APIView(MethodView):
    """Class with api field.
    Inherits from the primary MethodView class.
    """
    api: FavQsApi = FavQsApi()
