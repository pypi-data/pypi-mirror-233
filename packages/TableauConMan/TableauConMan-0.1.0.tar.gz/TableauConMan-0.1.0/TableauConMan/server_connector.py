"""A module to set up the connections to a Tableau server"""
from typing import Optional
import tableauserverclient as TSC


class ServerConnector:
    """Class represnting the connection details and methods for connecting to a Tableau server"""

    def __init__(self, site_name, server_url, token_name, token_secret):
        """

        :param site_name:
        :param server_url:
        :param token_name:
        :param token_secret:
        """
        self.server_name: Optional[str] = site_name
        self.server_url: str = server_url
        self.token_name: str = token_name
        self.token_secret: str = token_secret
        self.authentication: Optional[TSC.PersonalAccessTokenAuth] = None
        self.server: Optional[TSC.Server] = None

    def __repr__(self):
        """

        :return:
        """
        return "<Server {server_name} server_object={_server} auth_object={_authentication}>".format(
            **self.__dict__
        )

    @property
    def server(self) -> Optional[TSC.Server]:
        """

        :return:
        """
        return self._server

    @server.setter
    def server(self, value):
        """

        :param value:
        """
        if value is None:
            self._server = TSC.Server(self.server_url, use_server_version=True)
        elif not isinstance(value, TSC.Server):
            raise TypeError("server must be of TSC.Server class")
        else:
            self._server = value

    @property
    def authentication(self) -> Optional[TSC.PersonalAccessTokenAuth]:
        """

        :return:
        """
        return self._authentication

    @authentication.setter
    def authentication(self, value):
        """

        :param value:
        """
        if value is None:
            self._authentication = TSC.PersonalAccessTokenAuth(
                self.token_name,
                self.token_secret,
                self.server_name,
            )
        elif not isinstance(value, TSC.PersonalAccessTokenAuth):
            raise TypeError(
                "authentication must be of  TSC.PersonalAccessTokenAuth class"
            )
        else:
            self._authentication = value

    def connect(self):
        """

        :return:
        """
        connection = self.server.auth.sign_in(self.authentication)
        return connection
