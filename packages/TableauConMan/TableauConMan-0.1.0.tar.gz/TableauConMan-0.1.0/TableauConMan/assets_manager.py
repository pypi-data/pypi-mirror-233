"""Module for general Tableau Asset Manager"""
from helpers import utils


class AssetsManager:
    """Class for housing the common attributes and methods for asset management"""

    class AssetType:
        """Inner class for defining strings needed for generalizing methods"""

        Workbooks = "workbooks"
        Datasources = "datasources"

    def __init__(self, plan) -> None:
        self.plan = plan

    @staticmethod
    def get_changes(list_a: list, list_b: list):
        """
        Compares the target and reference lists to get the differences
        """
        in_a_and_b, in_a_not_b, in_b_not_a = utils.compare_lists(list_a, list_b)

        return in_a_and_b, in_a_not_b, in_b_not_a

    @staticmethod
    def get_item_from_list(item_name, item_list):
        """
        Filters a list of items based on the name of the item
        """
        item = utils.get_item_from_list(item_name, item_list)

        return item

    def update_connection_credentials(self, asset, asset_type):
        """
        Updates the connection credentials with a valid ses of credentials
        """
        # logger.info(f"Processing Datasource Connections for: {datasource_name} | {uploaded_datasource.has_extracts}")
        valid_connections = self.plan.connections
        target = self.plan.target
        server_asset = getattr(target.server, asset_type)
        with target.connect():
            server_asset.populate_connections(asset)

            for connection in asset.connections:
                for valid_connection in valid_connections:
                    if connection.connection_type == valid_connection.get(
                        "type"
                    ):  # In a workbook Published Datasource are of connection_type = sqlproxy
                        username, password = self.plan.get_connection_secretes(
                            valid_connection
                        )

                        connection.username = username
                        connection.password = password
                        connection.embed_password = True

                        server_asset.update_connection(asset, connection)
