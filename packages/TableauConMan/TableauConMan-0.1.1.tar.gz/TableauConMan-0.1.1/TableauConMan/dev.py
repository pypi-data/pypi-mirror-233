import os
from plan import Plan
from projects_manager import ProjectsManager
from yaml_connector import YamlConnector
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


def provision_settings():
    raw_plan = YamlConnector("provision_plan.yaml")

    plan = Plan()
    plan.load_plan(raw_plan.get_yaml())
    logger.info("Loaded plan")

    provision_projects(plan)


def provision_projects(provision_plan: Plan):
    logger.info("Processing Projects")
    projects = ProjectsManager(provision_plan)
    projects.populate_projects()
    logger.info("Populated projects")
    logger.debug(f"Reference Projects: {projects.reference_projects}")
    logger.debug(f"Reference Project List: {projects.reference_projects_list}")
    logger.debug(f"Target Projects: {projects.target_projects}")
    logger.debug(f"Target Project List: {projects.target_projects_list}")
    logger.debug(f"Target Project Path List: {projects.target_project_paths_list}")
    logger.debug(
        f"Reference Project Path List: {projects.reference_project_paths_list}"
    )

    to_update, to_remove, to_add = projects.get_project_changes()
    logger.debug(f"Add:{to_add}, Remove:{to_remove}, Update: {to_update}")

    projects.add(to_add)

    projects.remove(to_remove)

    logger.info("Processed Projects")

    logger.info("Processing Permissions")
    projects.populate_projects()
    logger.info("Populated projects")
    project_options = projects.get_project_options()

    if project_options.get("update_permissions"):
        projects.populate_users_and_groups()
        projects.populate_project_permissions()
        projects.populate_permission_capabilities()

        to_update, to_remove, to_add = projects.get_permission_changes()
        # logger.debug(f"Add:{to_add}, Remove:{to_remove}, Update: {to_update}")
        logger.debug(f"Add:{to_add}")
        logger.debug(f"Remove:{to_remove}")
        logger.debug(f"Update: {to_update}")

        projects.add_capabilities(to_add)

        # projects.remove_capabilities(to_remove)

    logger.info("Processed Permissions")


if __name__ == "__main__":
    provision_settings()
