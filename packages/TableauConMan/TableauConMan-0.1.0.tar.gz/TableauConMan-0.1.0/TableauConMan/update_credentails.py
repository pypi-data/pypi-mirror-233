import os
import tableauserverclient as TSC
import fire
from loguru import logger


class UpdateCredentials:
    def __init__(self, token_name, token_secret, tableau_url, site_name):
        """

        :param token_name:
        :param token_secret:
        :param tableau_url:
        :param site_name:
        """
        self.auth = TSC.PersonalAccessTokenAuth(
            token_name,
            token_secret,
            site_name,
        )
        logger.info("Successfully authenticated using PAT")
        self.server = TSC.Server(tableau_url, use_server_version=True)
        logger.info("Successfully connected server")

        self.endpoints = {
            "WorkbookItem": self.server.workbooks,
            "DatasourceItem": self.server.datasources,
            "FlowItem": self.server.flows,
        }

        self.output = []

    def get_server_connections(self):
        with self.server.auth.sign_in(self.auth):
            resource_list = []
            for endpoint in self.endpoints.values():
                resources = list(TSC.Pager(endpoint))

                for resource in resources:
                    endpoint.populate_connections(resource)

                resource_list.extend(resources)
            return resource_list

    def update_connection(self, resource, connection, username, password):
        connection.username = username
        connection.password = password
        # Not used?
        endpoint = self.endpoints.get(resource.__class__.__name__)

        self.output.append(
            f"{resource.__class__.__name__}: {resource.name} | Connection Type: {connection.connection_type} | Connection User Name: {connection.username} | Embed Password: {connection.embed_password} "
        )

    def update_user_connections(self, username, password):
        server_connections = self.get_server_connections()

        with self.server.auth.sign_in(tableau_auth):
            for resource in server_connections:
                user_connections = list(
                    filter(
                        lambda x: x.username.lower() == username
                        and x.connection_type == "snowflake"
                        and x.embed_password is True,
                        resource.connections,
                    )
                )

                for connection in user_connections:
                    self.update_connection(resource, connection, username, password)


if __name__ == "__main__":
    token_name = os.environ.get("TABLEAU_TOKEN_NAME")
    token_secret = os.environ.get("TABLEAU_TOKEN_SECRET")
    server_url = os.environ.get("TABLEAU_URL")
    site_name = os.environ.get("TABLEAU_SITE_NAME")

    # access the tableau site
    tableau_auth = TSC.PersonalAccessTokenAuth(
        token_name,
        token_secret,
        site_name,
    )

    uc = UpdateCredentials(token_name, token_secret, server_url, site_name)
    fire.Fire(uc.update_user_connections)

    with open(
        "update_credentials_output.txt", mode="wt", encoding="utf-8"
    ) as output_file:
        output_file.write("\n".join(uc.output))
