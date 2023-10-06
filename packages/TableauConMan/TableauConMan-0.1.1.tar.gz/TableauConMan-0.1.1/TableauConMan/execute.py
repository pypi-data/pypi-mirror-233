import os
from plan import Plan
from workbooks_manager import WorkbooksManager
from data_sources_manager import DataSourcesManager
from groups_manager import GroupsManager
from yaml_connector import YamlConnector
import fire
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


def migrate_content():
    raw_plan = YamlConnector("public_sync_plan.yaml")

    plan = Plan()
    plan.load_plan(raw_plan.get_yaml())
    logger.info("Loaded plan")

    migrate_datasources(plan)

    migrate_workbooks(plan)


def migrate_datasources(migrate_plan: Plan):
    logger.info("Processing Datasources")
    datasources = DataSourcesManager(migrate_plan)
    datasources.populate_datasources()
    logger.info("Populated datasources")
    # logger.debug(datasources.reference_datasources)

    datasource_options = datasources.get_datasource_options()

    to_update, to_add, to_remove = datasources.get_datasource_changes()
    logger.debug(f"Update:{to_update}, Add:{to_add}, Remove:{to_remove}")

    datasources.remove(to_remove)

    datasources.add(
        to_add,
        to_update,
        datasource_options,
    )

    logger.info("Processed Datasources")


def migrate_workbooks(migration_plan: Plan):
    logger.info("Processing Workbooks")
    workbooks = WorkbooksManager(migration_plan)
    workbooks.populate_workbooks()
    logger.info("Populated workbooks")
    logger.debug(workbooks.reference_workbooks)

    workbook_options = workbooks.get_workbook_options()
    to_update, to_add, to_remove = workbooks.get_workbook_changes()
    logger.debug(f"Update:{to_update}, Add:{to_add}, Remove:{to_remove}")

    workbooks.remove(to_remove)

    workbooks.add(to_add, to_update, workbook_options)

    logger.info("Processed Workbooks")


def provision_settings():
    raw_plan = YamlConnector("provision_plan.yaml")

    plan = Plan()
    plan.load_plan(raw_plan.get_yaml())
    logger.info("Loaded plan")

    provision_groups(plan)


def provision_groups(provision_plan: Plan):
    logger.info("Processing Groups")
    groups = GroupsManager(provision_plan)
    groups.populate_groups()
    logger.info("Populated groups")
    logger.debug(f"Target Groups: {groups.target_groups_list}")
    logger.debug(f"Reference Groups: {groups.reference_groups_list}")
    logger.debug(f"Target Group Memberships: {groups.target_group_memberships_list}")
    logger.debug(
        f"Reference Group Memberships: {groups.reference_group_memberships_list}"
    )
    groups.populate_users()

    to_add, to_remove, to_update = groups.get_group_changes()
    logger.debug(f"Add:{to_add}, Remove:{to_remove}, Update: {to_update}")

    groups.remove(to_remove)

    groups.add(to_add)

    groups.update(to_update)

    logger.info("Processed Groups")


if __name__ == "__main__":
    fire.Fire(
        {"migrate_content": migrate_content, "provision_settings": provision_settings}
    )
