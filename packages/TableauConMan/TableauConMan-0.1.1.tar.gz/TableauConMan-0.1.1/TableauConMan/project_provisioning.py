import os
from operator import itemgetter
from treelib import Tree
from loguru import logger

import yaml
import tableauserverclient as TSC


token_name = os.environ.get("TABLEAU_API_PUBLIC_TOKEN_NAME")
token_secret = os.environ.get("TABLEAU_API_PUBLIC_TOKEN_SECRET")
server_url = os.environ.get("TABLEAU_API_PUBLIC_URL")
site_name = os.environ.get("TABLEAU_API_PUBLIC_SITE_NAME")

# access the tableau site
tableau_auth = TSC.PersonalAccessTokenAuth(
    token_name,
    token_secret,
    site_name,
)

server = TSC.Server(server_url, use_server_version=True)

SPEC_FILE_PATH = "../tests/test_spec.yaml"

output = []

asset_types = ["project", "workbook", "datasource"]

"""
,
    'flow',
    'lens',
    'datarole',
    'metric'
"""


def get_server_projects(server):
    with server.auth.sign_in(tableau_auth):
        server_projects = list(TSC.Pager(server.projects))

        return server_projects


def get_server_project_permissions(server):
    with server.auth.sign_in(tableau_auth):
        server_projects = list(TSC.Pager(server.projects))

        for project in server_projects:
            server.projects.populate_permissions(project)
            server.projects.populate_workbook_default_permissions(project)
            server.projects.populate_datasource_default_permissions(project)
            # server.projects.populate_flow_default_permissions(project)
            # server.projects.populate_lens_default_permissions(project)
            # server.projects.populate_datarole_default_permissions(project)
            # server.projects.populate_metric_default_permissions(project)

        return server_projects


def parse_projects_to_tree(server_projects):
    tree = Tree()
    tree.create_node("tableau", "tableau", data="tableau")

    list_root = []
    for project in server_projects:
        if project.parent_id is None:  # not in project.keys()
            tree.create_node(
                project.id, project.id, parent="tableau", data=project.name
            )
            list_root.append(server_projects.index(project))

    index_list = list(set(range(len(server_projects))).difference(list_root))
    # print(f"The projects object {index_list}" )
    if len(index_list) > 0:
        project_list = list(
            itemgetter(*index_list)(server_projects)
        )  # list(itemgetter(*index_list)(all_projects))  #

        while len(index_list) > 0:
            remove_index = list()
            for index, curr_project in enumerate(project_list):
                # print(f"The projects object {curr_project}" )
                parent_project_id = curr_project.parent_id  # ['@parentProjectId']
                child_project_id = curr_project.id  # ['@id']
                child_name = curr_project.name  # ['@name']
                if tree.get_node(parent_project_id) is not None:
                    tree.create_node(
                        child_project_id,
                        child_project_id,
                        parent=parent_project_id,
                        data=child_name,
                    )
                    remove_index.append(index)

            index_list = list(set(range(len(project_list))).difference(remove_index))
            if len(index_list) > 0:
                project_list = list(
                    itemgetter(*index_list)(project_list)
                )  # list(project_list.itemgetter(*index_list)) #
    return tree


def get_project_paths(server_projects):
    project_tree = parse_projects_to_tree(server_projects)

    project_path_dict = {}

    for project in server_projects:
        nodes = list(project_tree.rsearch(project.id))
        nodes.reverse()
        node_path = "/".join([project_tree.get_node(node).data for node in nodes[1:]])
        project_path_dict[node_path] = project.id
        # project_path_dict[project.id] = f"{node_path}"

        # project_json["projects"].append(project_path_dict)

    return project_path_dict


def get_server_project_path_list(server_project_path_map):
    path_list = list(server_project_path_map.keys())
    # print(path_list)
    return path_list


def get_server_project_content_permissions_list(
    server_projects, server_project_path_map
):
    content_permissions_list = []
    for project in server_projects:
        project_path = list(
            filter(
                lambda x: server_project_path_map[x] == project.id,
                server_project_path_map,
            )
        )[0]
        content_permissions = project.content_permissions
        content_permissions_list.append(f"{project_path} | {content_permissions}")

    return content_permissions_list


def get_spec_project_list(spec_file_path: str):
    """

    :param spec_file_path:
    :return:
    """
    with open(spec_file_path, "r", encoding="UTF-8") as stream:
        try:
            group_list = yaml.safe_load(stream).get("projects")
            return group_list
        except yaml.YAMLError as exc:
            print(exc)


def get_spec_permission_templates_list(spec_file_path: str):
    """

    :param spec_file_path:
    :return:
    """
    with open(spec_file_path, "r") as stream:
        try:
            group_list = yaml.safe_load(stream).get("permission_templates")
            return group_list
        except yaml.YAMLError as exc:
            print(exc)


def get_spec_project_path_list(spec_projects):
    path_list = []
    for project in spec_projects:
        path_list.append(project.get("project_path"))
    # print(path_list)
    return path_list


def get_spec_project_content_permissions_list(spec_projects):
    content_permissions = []
    for project in spec_projects:
        content_permissions.append(
            f"{project['project_path']} | {project['content_permissions']}"
        )
    # print(path_list)
    return content_permissions


def get_list_overlaps(list_a, list_b):
    # print(list_a)
    in_a_and_b = sorted(list(set(list_a) & set(list_b)))
    in_a_not_b = sorted(list(set(list_a) ^ set(in_a_and_b)))
    in_b_not_a = sorted(list(set(list_b) ^ set(in_a_and_b)))
    # print(in_b_not_a)
    return in_a_and_b, in_a_not_b, in_b_not_a


def get_server_project(server_project_path_map, server_projects, project_path):
    try:
        project_id = server_project_path_map[project_path]
        project = list(filter(lambda x: x.id == project_id, server_projects))[0]
        return project
    except Exception as exc:
        output.append(f"Could not find project: {project_path}")
        logger.debug(exc)


def remove_server_project(server, project):
    # Project should be moved, by updating the parent_id, to an archived area that only admins can access as all content
    # in a project is deleted with the project.
    output.append(f"  {project.name}: {project.id}, Parent id: {project.parent_id}")


def create_server_project(
    server, spec_projects, server_project_path_map, project_path
):  # server,spec_projects,
    # print(spec_projects)
    # try:
    project_parent_path_end = project_path.rfind("/")
    # A top level project will not have a '/' in the path

    if project_parent_path_end == -1:
        project_parent_path = project_path
        parent_project_id = None
    else:
        project_parent_path = project_path[0:project_parent_path_end]
        parent_project_id = server_project_path_map[project_parent_path]

    # print(server_project_path_map)

    spec_project = list(
        filter(lambda x: x.get("project_path") == project_path, spec_projects)
    )[0]
    new_project = TSC.ProjectItem(
        name=spec_project.get("project_name"),
        content_permissions=spec_project.get("content_permissions"),
        description=spec_project.get("description"),
        parent_id=parent_project_id,
    )
    # with server.auth.sign_in(tableau_auth):
    #   server.projects.create(new_project)
    # print(new_project.name)
    output.append(f"  {new_project.name}, Project Path: {project_path}")


# except:
# print(f"Could not find parent project at path: {project_parent_path}")


def get_project_permission_object(asset_type, project):
    if asset_type == "project":
        permission_object_name = "permissions"
    else:
        permission_object_name = f"default_{asset_type}_permissions"

    permission_object = getattr(project, permission_object_name)

    return permission_object


def get_inherited_grantees(project):
    inherited_grantees = []
    for permission in project.permissions:
        if permission.capabilities.get("InheritedProjectLeader") is not None:
            if permission.capabilities.get("InheritedProjectLeader") == "Allow":
                inherited_grantees.append(permission.grantee.id)

    return inherited_grantees


def get_server_capabilities_list(server):
    server_projects = get_server_project_permissions(server)

    server_project_path_map = get_project_paths(server_projects)
    # print(server_project_path_map)

    # filter_id = list(filter(lambda x: x[0] == 'Development/Team Member', server_project_path_map.items()))[0]
    # print(filter_id)

    # server_projects = list(filter(lambda x: x.id== '3fa8cb67-b906-420d-9b51-7cb7bda90348', server_projects))

    server_capabilities_list = []

    with server.auth.sign_in(tableau_auth):
        server_users = list(TSC.Pager(server.users))
        server_groups = list(TSC.Pager(server.groups))
        for project in server_projects:
            project_path = list(
                filter(
                    lambda x: server_project_path_map[x] == project.id,
                    server_project_path_map,
                )
            )[0]
            # Check for inheritance and filer out permissions
            inherited_grantees = get_inherited_grantees(project)
            for asset_type in asset_types:
                permission_object = get_project_permission_object(asset_type, project)
                for permission in permission_object:
                    # print(project.id,permission.grantee.tag_name,permission.capabilities)
                    if permission.grantee.id not in inherited_grantees:
                        if permission.grantee.tag_name == "user":
                            user_item = list(
                                filter(
                                    lambda x: x.id == permission.grantee.id,
                                    server_users,
                                )
                            )[0]
                            # user_item = server.users.get_by_id(permission.grantee.id)
                            grantee_name = user_item.name
                        elif permission.grantee.tag_name == "group":
                            group_item = list(
                                filter(
                                    lambda x: x.id == permission.grantee.id,
                                    server_groups,
                                )
                            )[0]
                            grantee_name = group_item.name

                        for capability in permission.capabilities.keys():
                            server_capability_detail = {}

                            server_capability_detail.update(
                                {"project_path": project_path}
                            )
                            server_capability_detail.update(
                                {"grantee_type": permission.grantee.tag_name}
                            )
                            server_capability_detail.update(
                                {"grantee_name": grantee_name}
                            )
                            server_capability_detail.update({"asset_type": asset_type})
                            server_capability_detail.update({"capability": capability})
                            server_capability_detail.update(
                                {"mode": permission.capabilities.get(capability)}
                            )
                            # print(server_capability_detail)
                            # server_capabilities_list.append(server_capability_detail)
                            server_capabilities_list.append(
                                f"{project_path} | {permission.grantee.tag_name} | {grantee_name} | {asset_type} | {capability} | {permission.capabilities.get(capability)}"
                            )

    return server_capabilities_list


def get_spec_capabilities_list(spec_file_path):
    spec_projects = get_spec_project_list(spec_file_path)

    # spec_projects = list(filter(lambda x: x['project_path'] == 'Pilot/Business Insights', spec_projects))

    spec_permission_templates = get_spec_permission_templates_list(spec_file_path)

    # print(spec_permission_templates)

    spec_capabilities_list = []

    for project in spec_projects:
        permission_set = project.get("permission_set")
        if permission_set is not None:
            # print(project['permission_set'])
            for permission in permission_set:
                if permission.get("group_name") is not None:
                    grantee_type = "group"
                    grantee_name = permission.get("group_name")
                elif permission.get("user_name") is not None:
                    grantee_type = "user"
                    grantee_name = permission.get("user_name")
                # print(permission['permission_rule'])
                try:
                    permission_template = list(
                        filter(
                            lambda x: x.get("name")
                            == permission.get("permission_rule"),
                            spec_permission_templates,
                        )
                    )[0]
                except Exception as exc:
                    logger.info(
                        f"Project {project.get('project_path')} does not have a valid permission template: {permission.get('permission_rule')} "
                    )
                    logger.debug(exc)
                # print(permission_template)
                for asset_type, capabilities in permission_template.items():
                    # print(asset_type,capabilities, permission['permission_rule'])
                    if asset_type != "name" and asset_type in asset_types:
                        # print(asset_type,capabilities)
                        for capability, mode in capabilities.items():
                            # print(capability,asset_type[capability])
                            spec_capability_detail = {}

                            spec_capability_detail.update(
                                {"project_path": project.get("project_path")}
                            )
                            spec_capability_detail.update(
                                {"grantee_type": grantee_type}
                            )
                            spec_capability_detail.update(
                                {"grantee_name": grantee_name}
                            )
                            spec_capability_detail.update({"asset_type": asset_type})
                            spec_capability_detail.update({"capability": capability})
                            spec_capability_detail.update({"mode": mode})
                            # print(server_capability_detail)
                            # spec_capabilities_list.append(spec_capability_detail)
                            spec_capabilities_list.append(
                                f"{project.get('project_path')} | {grantee_type} | {grantee_name} | {asset_type} | {capability} | {mode}"
                            )

    return spec_capabilities_list


def provision_projects():
    server_projects = get_server_projects(server)
    server_project_path_map = get_project_paths(server_projects)

    server_project_path_list = get_server_project_path_list(server_project_path_map)

    spec_projects = get_spec_project_list(SPEC_FILE_PATH)
    spec_project_path_list = get_spec_project_path_list(spec_projects)

    common, to_remove, to_add = get_list_overlaps(
        server_project_path_list, spec_project_path_list
    )

    output.append("****** Project on Server but not in Spec ******")
    # print("****** Groups on Server but not in Spec ******", file=open('output.txt', 'a'))
    for project_path in to_remove:
        project = get_server_project(
            server_project_path_map, server_projects, project_path
        )
        if project is not None:
            # remove_server_project(server, project)
            output.append(
                f"  {project.name}: {project.id}, Project Path: {project_path}"
            )

    output.append("****** Projects in Spec but not on Server ******")
    # print("****** Groups in Spec but not on Server ******", file=open('output.txt', 'a'))
    for project_path in to_add:
        create_server_project(
            server, spec_projects, server_project_path_map, project_path
        )


def provision_capabilities():
    server_capabilities_list = sorted(get_server_capabilities_list(server))

    # print(server_capabilities_list)

    spec_capabilities_list = sorted(get_spec_capabilities_list(SPEC_FILE_PATH))

    common, to_delete, to_add = get_list_overlaps(
        server_capabilities_list, spec_capabilities_list
    )
    """ The next step is it get the grantee item and create the capabilities objects and combine them in a Rule"""
    # output.append("****** Capabilities on Server ******")
    # output.extend(server_capabilities_list)

    # output.append("****** Capabilities in Spec ******")
    # output.extend(spec_capabilities_list)

    output.append("****** Capabilities on Server but not in Spec ******")
    output.extend(to_delete)

    output.append("****** Capabilities in Spec but not on Server ******")
    output.extend(to_add)


def provision_content_permissions():
    server_projects = get_server_projects(server)
    server_project_path_map = get_project_paths(server_projects)

    server_project_content_permissions_list = (
        get_server_project_content_permissions_list(
            server_projects, server_project_path_map
        )
    )

    spec_projects = get_spec_project_list(SPEC_FILE_PATH)
    spec_project_content_permissions_list = get_spec_project_content_permissions_list(
        spec_projects
    )

    common, to_delete, to_add = get_list_overlaps(
        server_project_content_permissions_list, spec_project_content_permissions_list
    )

    output.append("****** Content Permissions on Server but not in Spec ******")
    output.extend(to_delete)

    output.append("****** Content Permissions in Spec but not on Server ******")
    output.extend(to_add)


if __name__ == "__main__":
    provision_projects()

    provision_content_permissions()

    provision_capabilities()

    with open(
        "project_provisioning_output.txt", mode="wt", encoding="utf-8"
    ) as output_file:
        output_file.write("\n".join(output))
