import os
from typing import Optional
from assets_manager import AssetsManager
from helpers import utils
import tableauserverclient as TSC
from loguru import logger


class DataSourcesManager(AssetsManager):
    def __init__(self, plan) -> None:
        """

        :param plan:
        """
        AssetsManager.__init__(self, plan)
        self.target_datasources: Optional[list[TSC.DatasourceItem]] = None
        self.target_datasources_list: Optional[list] = None
        self.reference_datasources: Optional[list[TSC.DatasourceItem]] = None
        self.reference_datasources_list: Optional[list] = None

    def populate_datasources(self):
        """
        Use object properties to get a comparable list of workbooks from the source and reference
        """

        (
            self.target_datasources,
            self.target_datasources_list,
        ) = self._generate_server_list(
            self.plan.target,
            self.AssetType.Datasources,
            self.plan.target_selection_rules,
        )

        (
            self.reference_datasources,
            self.reference_datasources_list,
        ) = self.get_all_datasources("reference")

    def get_all_datasources(self, server_type: str):
        """
        Can retrieve multiple data sources with the same name.
        Have to collect the data sources from the other Items that can reference them: Workbooks and Flows
        """
        source_server = getattr(self.plan, server_type)
        source_selection_rules = getattr(self.plan, server_type + "_selection_rules")
        datasources, datasource_list = self._generate_server_list(
            source_server,
            self.AssetType.Datasources,
            source_selection_rules,
        )

        workbooks, workbooks_list = self._generate_server_list(
            source_server,
            self.AssetType.Workbooks,
            source_selection_rules,
        )

        logger.debug(f"Workbook Name List: {workbooks_list}")

        (
            workbook_datasource_ids,
            workbook_datasource_names,
        ) = self.get_workbook_datasources(workbooks)

        all_datasources, all_datasources_list = self._generate_server_list(
            source_server,
            self.AssetType.Datasources,
        )

        workbook_datasources = utils.get_filtered_list(
            all_datasources, workbook_datasource_ids, "id"
        )

        with source_server.connect():
            for datasource in workbook_datasources:
                logger.debug(
                    f"Datasource: {datasource.name.replace(' ','')} has {datasource.content_url} content_url"
                )

        """
        Add process to check against the mapping or server request options
        """

        logger.debug(f"Workbook Datasource Names: {workbook_datasource_names}")

        combined_datasources = set(datasources + workbook_datasources)

        combined_datasources_list = set(datasource_list + workbook_datasource_names)

        return combined_datasources, combined_datasources_list

    def get_workbook_datasources(self, workbook_items):
        workbook_ids = list()

        for workbook in workbook_items:
            workbook_ids.append(workbook.id)

        logger.debug(f"List of Workbook ids: {workbook_ids}")

        with self.plan.reference.connect():
            # Execute the query
            query_result = self.plan.reference.server.metadata.query(
                """
              query findWorkbookDatasource($luids: [String]) {
                workbooksConnection(filter: {luidWithin: $luids}) {
                  nodes{
                    name
                    upstreamDatasources {
                      name
                      luid
                    }
                  }
                }
              }
              """,
                {"luids": workbook_ids},
            )

            workbook_datasource_ids = list()

            workbook_datasource_names = list()

            logger.debug(f"Metadata query result: {query_result}")

            result_data = query_result.get("data")
            data_nodes = result_data.get("workbooksConnection")
            workbook_list = data_nodes.get("nodes")

            for workbook in workbook_list:
                for datasource in workbook.get("upstreamDatasources"):
                    logger.debug(
                        f"Workbook: {workbook} | Datasource: {datasource.get('name')} | luid: {datasource.get('luid')} "
                    )
                    workbook_datasource_ids.append(datasource.get("luid"))
                    workbook_datasource_names.append(datasource.get("name"))

            return workbook_datasource_ids, workbook_datasource_names

    def _generate_server_list(
        self, source, asset_type, request_filter: Optional[TSC.RequestOptions] = None
    ):
        """

        :param source:
        :param asset_type:
        :param filter:
        :return:
        """
        asset = getattr(source.server, asset_type)

        with source.connect():
            asset_items = list(TSC.Pager(asset, request_filter))
            """
          Generalized: can be moved to parent class
          Find a way to included updated_at check.  Might be able to use dict to
          """

            asset_list = []
            for asset in asset_items:
                asset_list.append(asset.name)
            return asset_items, asset_list

    def get_datasource_options(self):
        """

        :return:
        """
        datasource_options = self.plan.asset_options.get("datasources")
        return datasource_options

    def get_datasource_changes(self):
        """

        :return:
        """
        common, to_remove, to_add = self.get_changes(
            self.target_datasources_list, self.reference_datasources_list
        )

        update = []
        for datasource_name in common:
            target_datasource = self.get_item_from_list(
                datasource_name, self.target_datasources
            )

            reference_datasource = self.get_item_from_list(
                datasource_name, self.reference_datasources
            )

            logger.debug(
                f"Datasource {reference_datasource.name} | Reference Updated At: {reference_datasource.updated_at.strftime('%Y-%m-%d, %H:%M:%S')} | Target Updated At {target_datasource.updated_at.strftime('%Y-%m-%d, %H:%M:%S')}"
            )

            if reference_datasource.updated_at > target_datasource.updated_at:
                update.append(datasource_name)

        return update, to_add, to_remove

    def delete(self, server, datasource):
        """

        :param server:
        :param datasource:
        """
        with server.connect():
            server.server.datasources.delete(datasource.id)

    def download(self, server, datasource):
        """

        :param server:
        :param datasource:
        :return:
        """
        with server.connect():
            file_path = server.server.datasources.download(datasource.id)

        return file_path

    def format_target_datasource(self, reference_datasource):
        """

        :param reference_datasource:
        :return:
        """
        target_datasource = TSC.DatasourceItem("")
        target_datasource.name = reference_datasource.name
        # target_datasource.content_url = reference_datasource.content_url
        target_datasource.project_id = self.get_target_project()

        return target_datasource

    def get_target_project(self):
        """
        Get the target project based on the plan asset project_type option
        """
        datasource_options = self.get_datasource_options()
        datasource_mapping = datasource_options.get("mapping")
        request_options = self.plan.format_rule(
            datasource_mapping.get("project_filter")
        )
        server = self.plan.target
        with server.connect():
            server_project = self.plan.target.server.projects.get(request_options)[0][0]
        target_project = server_project.id
        return target_project

    def upload(self, server, datasource, file_path):
        """

        :param server:
        :param datasource:
        :param file_path:
        :return:
        """
        with server.connect():
            new_workbook = server.server.datasources.publish(
                datasource, file_path, "Overwrite"
            )

        logger.debug(
            f"Datasource {new_workbook.name} has a content url of: {new_workbook.content_url}"
        )

        return new_workbook

    def add(
        self,
        list_to_add: list,
        list_to_update: list = [],
        datasource_options: dict = {},
    ):
        """
        Match the workbook from list to reference object
        Download reference workbook
        Get source project object
        Set workbook project to source project_id
        Upload workbook
        Delete downloaded workbook file
        """
        to_add_and_update = list_to_add + list_to_update

        if len(to_add_and_update) > 0:
            for datasource_name in to_add_and_update:
                logger.info(f"Processing Addition of Datasource: {datasource_name}")
                reference_datasource = self.get_item_from_list(
                    datasource_name, self.reference_datasources
                )

                file_path = self.download(self.plan.reference, reference_datasource)
                target_datasource = self.format_target_datasource(reference_datasource)
                uploaded_datasource = self.upload(
                    self.plan.target, target_datasource, file_path
                )

                logger.debug(
                    f"Reference content URL: {reference_datasource.content_url} | Uploaded content URL: {uploaded_datasource.content_url}"
                )
                if reference_datasource.content_url != uploaded_datasource.content_url:
                    logger.warning(
                        f"The reference content URL,{reference_datasource.content_url}, does not match the content URL of the uploaded datasource,{uploaded_datasource.content_url}.  This may cause errors in uploaded workbooks"
                    )

                os.remove(file_path)

                if datasource_name in list_to_add and (
                    datasource_options.get("include_published_datasources")
                    or not uploaded_datasource.has_extracts
                ):
                    logger.info(
                        f"Processing Datasource Connections for: {datasource_name} | {uploaded_datasource.has_extracts}"
                    )
                    self.update_connection_credentials(
                        uploaded_datasource, self.AssetType.Datasources
                    )
                    logger.info(
                        f"Processed Datasource Connections for: {datasource_name} | {uploaded_datasource.has_extracts}"
                    )
        logger.info(f"Added {len(to_add_and_update)} Datasources")

    def remove(self, remove_list: list):
        """
        Match the workbook from list to reference object
        Delete Workbook
        """
        if len(remove_list) > 0:
            for datasource_name in remove_list:
                datasource = self.get_item_from_list(
                    datasource_name, self.target_datasources
                )

                self.delete(self.plan.target, datasource)
                logger.info(f"Datasource {datasource.name} deleted")
        logger.info(f"Removed {len(remove_list)} Datasources")
