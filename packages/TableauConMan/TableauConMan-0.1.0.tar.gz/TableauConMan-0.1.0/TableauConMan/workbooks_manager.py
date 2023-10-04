"""Module for classes and functions for managing Tableau Workbooks"""
import os
from typing import Optional
from assets_manager import AssetsManager
from plan import Plan
from data_sources_manager import DataSourcesManager
import tableauserverclient as TSC
from loguru import logger


class WorkbooksManager(AssetsManager):
    """Class for managing Tableau Workbook items"""

    def __init__(self, plan) -> None:
        """

        :param plan:
        """
        AssetsManager.__init__(self, plan)
        self.asset_type = self.AssetType.Workbooks
        self.target_workbooks: Optional[list[TSC.WorkbookItem]] = None
        self.target_workbooks_list: Optional[list] = None
        self.reference_workbooks: Optional[list[TSC.WorkbookItem]] = None
        self.reference_workbooks_list: Optional[list] = None

    def populate_workbooks(self):
        """
        Use object properties to get a comparable list of workbooks from the source and reference
        """
        self.target_workbooks, self.target_workbooks_list = self._generate_server_list(
            self.plan.target, "workbooks", self.plan.target_selection_rules
        )

        (
            self.reference_workbooks,
            self.reference_workbooks_list,
        ) = self._generate_server_list(
            self.plan.reference, "workbooks", self.plan.reference_selection_rules
        )

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
            # print(workbooks)
            """
          Generalized: can be moved to parent class
          Find a way to included updated_at check.  Might be able to use dict to
          """

            asset_list = []
            for asset in asset_items:
                # print(workbook.name)
                asset_list.append(asset.name)
            # print(workbook_list)
            return asset_items, asset_list

    def get_workbook_options(self):
        """

        :return:
        """
        workbook_options = self.plan.asset_options.get("workbooks")

        return workbook_options

    def get_workbook_changes(self):
        """

        :return:
        """
        common, to_remove, to_add = self.get_changes(
            self.target_workbooks_list, self.reference_workbooks_list
        )

        update = []
        for workbook_name in common:
            target_workbook = self.get_item_from_list(
                workbook_name, self.target_workbooks
            )

            reference_workbook = self.get_item_from_list(
                workbook_name, self.reference_workbooks
            )

            # logger.debug(f"Reference Updated At: {reference_datasource.updated_at.strftime('%Y-%m-%d, %H:%M:%S')} | Target Updated At {target_datasource.updated_at.strftime('%Y-%m-%d, %H:%M:%S')}")

            if reference_workbook.updated_at > target_workbook.updated_at:
                update.append(workbook_name)

        return update, to_add, to_remove

    def delete(self, server, workbook):
        """

        :param server:
        :param workbook:
        """
        with server.connect():
            server.server.workbooks.delete(workbook.id)

    def download(self, server, workbook):
        """

        :param server:
        :param workbook:
        :return:
        """
        with server.connect():
            file_path = server.server.workbooks.download(workbook.id)

        return file_path

    def format_target_workbook(self, reference_workbook):
        """

        :param reference_workbook:
        :return:
        """
        target_workbook = TSC.WorkbookItem("")
        target_workbook.name = reference_workbook.name
        target_workbook.project_id = self.get_target_project()

        return target_workbook

    def get_target_project(self):
        """
        Get the target project based on the plan asset project_type option
        """
        workbook_options = self.get_workbook_options()
        workbook_mapping = workbook_options.get("mapping")
        request_options = self.plan.format_rule(workbook_mapping.get("project_filter"))
        server = self.plan.target
        with server.connect():
            server_project = self.plan.target.server.projects.get(request_options)[0][0]
        target_project = server_project.id
        return target_project

    def upload(self, server, workbook, file_path):
        """

        :param server:
        :param workbook:
        :param file_path:
        :return:
        """
        with server.connect():
            new_workbook = server.server.workbooks.publish(
                workbook,
                file_path,
                "Overwrite",
                skip_connection_check=True,
            )

        return new_workbook

    def add(
        self,
        list_to_add: list,
        list_to_update: list = [],
        workbook_options: dict = {},
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
            processed_wordbooks_count = 0
            for workbook_name in to_add_and_update:
                reference_workbook = self.get_item_from_list(
                    workbook_name, self.reference_workbooks
                )

                # populate connections and look at what if it matches the known datasources

                file_path = self.download(self.plan.reference, reference_workbook)
                target_workbook = self.format_target_workbook(reference_workbook)
                try:
                    uploaded_workbook = self.upload(
                        self.plan.target, target_workbook, file_path
                    )

                    self.update_connection_credentials(
                        uploaded_workbook, self.AssetType.Workbooks
                    )
                    logger.info(
                        f"Processed Datasource Connections for: {workbook_name}"
                    )
                    processed_wordbooks_count += 1
                except Exception as exc:
                    logger.warning(
                        f"There was a problem processing workbook {workbook_name}: {exc}"
                    )
                finally:
                    os.remove(file_path)
                    continue

        logger.info(f"Added {processed_wordbooks_count} Workbooks")

    def remove(self, remove_list: list):
        """
        Match the workbook from list to reference object
        Delete Workbook
        """
        if len(remove_list) > 0:
            for workbook_name in remove_list:
                workbook = self.get_item_from_list(workbook_name, self.target_workbooks)

                self.delete(self.plan.target, workbook)
                logger.info(f"Workbook {workbook.name} deleted")
        logger.info(f"Removed {len(remove_list)} Workbooks")
