"""Module management of provided plans"""
import os
import tableauserverclient as TSC
from server_connector import ServerConnector


class Plan:
    """Class for reading and formatting configs and options from the provided plan"""

    def __init__(self):
        self.target: str = None
        self.reference: str = None
        self.target_selection_rules: TSC.RequestOptions() = None
        self.reference_selection_rules: TSC.RequestOptions() = None
        self.assets: list = None
        self.asset_options: dict = None
        self.operation: str = None
        self.connections: dict = None
        self.raw_plan: dict = None

    def load_plan(self, raw_plan: dict) -> None:
        """

        :param raw_plan:
        """
        if not isinstance(raw_plan, dict):
            raise TypeError("The raw plan must be a dictionary")

        self.target = self.format_connection(raw_plan.get("target"))
        self.reference = self.format_connection(raw_plan.get("reference"))
        self.target_selection_rules = self.format_rule(
            raw_plan.get("target_selection_rules")
        )
        self.reference_selection_rules = self.format_rule(
            raw_plan.get("reference_selection_rules")
        )
        self.assets = list(raw_plan.get("assets"))
        self.asset_options = raw_plan.get("assets")
        self.operation = raw_plan.get("operation")
        self.connections = raw_plan.get("connections")
        self.raw_plan = raw_plan

    @staticmethod
    def format_rule(rules):
        """

        :param rules:
        :return:
        """
        formatted_rule = TSC.RequestOptions()

        for rule in rules:
            field = getattr(formatted_rule.Field, rule.get("field"))
            operator = getattr(formatted_rule.Operator, rule.get("operator"))
            value = rule.get("value")
            formatted_rule.filter.add(TSC.Filter(field, operator, value))

        return formatted_rule

    def format_connection(self, connection):
        """

        :param connection:
        :return:
        """
        if connection.get("type") == "server":
            connection = self.format_server(connection)

        return connection

    def format_server(self, connection):
        """

        :param connection:
        :return:
        """
        token_name, token_secret, server_url, site_name = self.get_server_secrets(
            connection
        )

        server = ServerConnector(site_name, server_url, token_name, token_secret)

        return server

    @staticmethod
    def get_server_secrets(server):
        """

        :param server:
        :return:
        """
        secrete_prefix = server.get("secrete_prefix")
        token_name = os.environ.get(secrete_prefix + "_TOKEN_NAME")
        token_secret = os.environ.get(secrete_prefix + "_TOKEN_SECRET")
        server_url = os.environ.get(secrete_prefix + "_URL")
        site_name = os.environ.get(secrete_prefix + "_SITE_NAME")

        return token_name, token_secret, server_url, site_name

    @staticmethod
    def get_connection_secretes(connection):
        """

        :param connection:
        :return:
        """
        secrete_prefix = connection.get("secrete_prefix")

        username = os.environ.get(secrete_prefix + "_USERNAME")
        password = os.environ.get(secrete_prefix + "_PASSWORD")

        return username, password
