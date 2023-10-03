from .data import HTTPRequest
from .app_processor import AppProcessor


class AppController(AppProcessor):
    """Module with which you can define AWS APIGateway endpoints.
    :param base_path: base resource url.
    """

    def __init__(self, base_path: str):
        self._routes = dict()
        self._base_url = base_path

    @property
    def data_type(self) -> type:
        return HTTPRequest

    @property
    def handlers(self) -> dict[str, tuple[callable, dict | None]]:
        return self._routes

    def route(self, path: str, method: str, qualifier: dict = None):
        """Function that represents an endpoint.
        :param path: Resource url.
        :param method: HTTP method.
        :param qualifier: Dictionary used by injection package in order to
         specify components by name in case of multiple implementations.
        """

        def _route(func: callable):
            self._routes[f"{self._base_url}{path}::{method}"] = func, qualifier
            return func

        return _route

    def get(self, path: str = "", qualifier: dict = None):
        """Function that represents an HTTP GET method endpoint.
        :param path: Resource url.
        :param qualifier: Dictionary, used by injection package in order to
         specify components by name in case of multiple implementations.
        """

        return self.route(path, "GET", qualifier)

    def post(self, path: str = "", qualifier: dict = None):
        """Function that represents an HTTP POST method endpoint.
        :param path: Resource url.
        :param qualifier: Dictionary, used by injection package in order to
         specify components by name in case of multiple implementations.
        """

        return self.route(path, "POST", qualifier)

    def patch(self, path: str = "", qualifier: dict = None):
        """Function that represents an HTTP PATCH method endpoint.
        :param path: Resource url.
        :param qualifier: Dictionary, used by injection package in order to
         specify components by name in case of multiple implementations.
        """

        return self.route(path, "PATCH", qualifier)

    def delete(self, path: str = "", qualifier: dict = None):
        """Function that represents an HTTP DELETE method endpoint.
        :param path: Resource url.
        :param qualifier: Dictionary, used by injection package in order to
         specify components by name in case of multiple implementations.
        """

        return self.route(path, "DELETE", qualifier)

    def put(self, path: str = "", qualifier: dict = None):
        """Function that represents an HTTP PUT method endpoint.
        :param path: Resource url.
        :param qualifier: Dictionary, used by injection package in order to
         specify components by name in case of multiple implementations.
        """

        return self.route(path, "PUT", qualifier)
