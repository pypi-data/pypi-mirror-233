import tableauserverclient as TSC
import csv
import yaml
from treelib import Tree
from operator import itemgetter
import os


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

server = TSC.Server(server_url, use_server_version=True)

workbook_dataset = []
workbook_header = ["Workbook Name", "Project name", "Type", "Name", "Capabilities"]
workbook_file_name = "tableau_workbook_permissions"

project_permissions_dataset = []
project_permissions_header = [
    "Project name",
    "Object Type" "Content Permissions" "Type",
    "Name",
    "Capabilities",
]
project_permissions_filename = "tableau_project_permissions"
project_permissions_json = {"project_permissions": []}

user_dataset = []
user_header = [
    "User Name",
    "User Email",
    "Site Role",
    "Authentication Setting",
    "Groups",
]
user_filename = "tableau_users"
users_json = {"users": []}

group_dataset = []
group_filename = "tableau_groups"
group_json = {"groups": []}

project_filename = "tableau_projects"
project_json = {"projects": []}


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


def write_result(header, dataset, filename):
    # write data to csv

    with open(
        f"{filename}.csv",
        "w",
        encoding="utf-8",
        newline="",
    ) as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(dataset)


def write_result_yml(dict_file, filename):
    with open(f"{filename}.yaml", "w") as file:

        documents = yaml.dump(
            dict_file,
            file,
            default_flow_style=False,
            sort_keys=False,
            Dumper=IndentDumper,
        )


import os


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * (level)
        print("{}{}/".format(indent, os.path.basename(root)))
        subindent = " " * 4 * (level + 1)
        for f in files:
            print("{}{}".format(subindent, f))


def list_directory(startpath):
    directory_json = {"directory": []}
    directory_filename = "repo_directory"
    for root, dirs, files in os.walk(startpath):
        dir_dict = {}
        dir_dict["directory_path"] = "{}/{}".format(
            os.path.dirname(root).replace(startpath, ""), os.path.basename(root)
        )
        dir_dict["directory_name"] = "{}".format(os.path.basename(root))
        # print('{}/{}'.format(os.path.dirname(root).replace(startpath, ''),os.path.basename(root)))
        # print('{}'.format(os.path.basename(root)))

        directory_json["directory"].append(dir_dict)

    write_result_yml(directory_json, directory_filename)


def get_workbook_permissions(workbooks, dataset):
    for workbook in workbooks:
        workbook_name = workbook.name
        workbook_id = workbook.id
        created_at = workbook.created_at
        project_name = workbook.project_name

        # Admins can not access permission on workbooks in a personal space.
        try:
            server.workbooks.populate_permissions(workbook)
            permissions = workbook.permissions
        except:
            print(
                f"An exception occurred: Project {project_name} | {workbook_name}: {workbook_id}"
            )

        for permitee in permissions:
            group_user_type = permitee.grantee.tag_name
            group_user_id = permitee.grantee.id
            capabilities = permitee.capabilities

            row_data = []

            if group_user_type == "user":
                user_item = server.users.get_by_id(permitee.grantee.id)
                group_user_name = user_item.name
            elif group_user_type == "group":
                for group_item in TSC.Pager(server.groups):
                    if group_item.id == group_user_id:
                        group_user_name = group_item.name
                        break

            # create row_data record for adding to the csv file
            row_data.extend(
                [
                    workbook.name,
                    workbook.project_name,
                    group_user_type.capitalize(),
                    group_user_name,
                    capabilities,
                ]
            )
            # add the record to the dataset
            dataset.append(row_data)


def get_project_populate_object(object_name):
    if object_name == "project":
        populate_object_name = "populate_permissions"
    else:
        populate_object_name = f"populate_{object_name}_default_permissions"

    populate_object = getattr(server.projects, populate_object_name)

    return populate_object


def get_project_permission_object(object_name, project):
    if object_name == "project":
        permission_object_name = "permissions"
    else:
        permission_object_name = f"default_{object_name}_permissions"

    permission_object = getattr(project, permission_object_name)

    return permission_object


def get_project_permissions(projects, dataset, object_name):

    for project in projects:
        project_name = project.name
        project_id = project.id
        project_content_permissions = project.content_permissions
        project_parent_id = project.parent_id

        # Admins can not access permission on workbooks in a personal space.
        populate_object = get_project_populate_object(object_name)
        populate_object(project)
        # server.projects.populate_metric_default_permissions(project) #  populate_flow_default_permissions populate_permissions
        permissions = get_project_permission_object(object_name, project)
        # permissions = project.default_metric_permissions    #  default_flow_permissions permissions
        # try:

        # except:
        # print(f"An exception occurred: {project_name}: {project_id}" )

        row_data_json = {}

        row_data_json["project_name"] = project_name
        row_data_json["object_name"] = object_name
        row_data_json["project_content_permissions"] = project_content_permissions

        for permitee in permissions:
            group_user_type = permitee.grantee.tag_name
            group_user_id = permitee.grantee.id
            capabilities = permitee.capabilities

            row_data = []

            if group_user_type == "user":
                user_item = server.users.get_by_id(permitee.grantee.id)
                group_user_name = user_item.name
            elif group_user_type == "group":
                for group_item in TSC.Pager(server.groups):
                    if group_item.id == group_user_id:
                        group_user_name = group_item.name
                        break

            row_data_json["group_user_name"] = group_user_name
            # row_data_json['group_user_type'] = group_user_type.capitalize()
            # row_data_json['group_user_name']['object_name']['capabilities'] = capabilities

            project_permissions_json["project_permissions"].append(row_data_json)

            # create row_data record for adding to the csv file
            row_data.extend(
                [
                    project_name,
                    object_name,
                    project_content_permissions,
                    group_user_type.capitalize(),
                    group_user_name,
                    capabilities,
                ]
            )
            # add the record to the dataset
            dataset.append(row_data)


def get_users(users, dataset):
    for user in users:
        user_name = user.name
        user_email = user.email
        user_site_role = user.site_role
        user_auth_setting = user.auth_setting

        try:
            server.users.populate_groups(user)
            groups = user.groups
        except:
            print(f"An exception occurred: User {user_name} ")

        group_names = []

        for group in groups:
            if group.name != "All Users":
                group_names.append(group.name)

        row_data = []

        # create row_data record for adding to the csv file
        row_data.extend(
            [
                user_name,
                user_email,
                user_site_role,
                user_auth_setting,
                group_names,
            ]
        )
        # add the record to the dataset
        dataset.append(row_data)

        row_data_json = {}

        row_data_json["user_name"] = user_email
        row_data_json["site_role"] = user_site_role
        row_data_json["auth_setting"] = user_auth_setting
        row_data_json["groups"] = group_names

        users_json["users"].append(row_data_json)


def get_groups(groups, dataset):
    for group in groups:
        group_name = group.name
        group_site_role = group.minimum_site_role
        group_license_mode = group.license_mode

        row_data_json = {}

        row_data_json["group_name"] = group_name
        row_data_json["group_site_role"] = group_site_role
        row_data_json["group_license_mode"] = group_license_mode

        group_json["groups"].append(row_data_json)


def parse_projects_to_tree(all_projects):

    tree = Tree()
    tree.create_node("tableau", "tableau", data="tableau")

    list_root = []
    for project in all_projects:
        if project.parent_id == None:  # not in project.keys()
            tree.create_node(
                project.id, project.id, parent="tableau", data=project.name
            )
            list_root.append(all_projects.index(project))

    index_list = list(set(range(len(all_projects))).difference(list_root))
    # print(f"The projects object {list_root}" )
    if len(index_list) > 0:
        project_list = list(
            itemgetter(*index_list)(all_projects)
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


def get_project_paths(all_projects):
    project_tree = parse_projects_to_tree(all_projects)

    project_path_dict = {}

    for project in all_projects:
        nodes = list(project_tree.rsearch(project.id))
        nodes.reverse()
        node_path = "/".join([project_tree.get_node(node).data for node in nodes[1:]])
        project_path_dict[node_path] = project.id
        # project_path_dict[project.id] = f"{node_path}"

        # project_json["projects"].append(project_path_dict)

    return project_path_dict


def get_projects(projects):

    project_tree = get_project_paths(projects)

    for project in projects:
        project_name = project.name
        project_description = project.description
        project_content_permissions = project.content_permissions
        project_path = list(project_tree.keys())[
            list(project_tree.values()).index(project.id)
        ]

        row_data_json = {
            "project_name": project_name,
            "description": project_description,
            "content_permissions": project_content_permissions,
            "project_path": project_path,
        }

        project_json["projects"].append(row_data_json)


def get_sites():
    pass


with server.auth.sign_in(tableau_auth):

    # get all workbook names and IDs
    all_workbooks, pagination_item = server.workbooks.get()
    print("\nThere are {} workbooks on site: ".format(pagination_item.total_available))

    # get_workbook_permissions(all_workbooks,workbook_dataset)
    # write_result(workbook_header,workbook_dataset,workbook_file_name)

    # get all project names and IDs
    all_projects, pagination_item = server.projects.get()
    print("\nThere are {} projects on site: ".format(pagination_item.total_available))

    # all_projects = list(TSC.Pager(server.projects))

    # get_project_paths(all_projects)

    # get_projects(all_projects)

    # write_result_yml(project_json, project_filename)

    # get_project_permissions(all_projects, project_permissions_dataset, "project")
    # get_project_permissions(all_projects,project_permissions_dataset,'datasource')
    # write_result(project_header,project_dataset,project_filename)
    # write_result_yml(project_permissions_json, project_permissions_filename)

    # get all users
    all_users, pagination_item = server.users.get()
    print("\nThere are {} users on site: ".format(pagination_item.total_available))

    # all_users = list(TSC.Pager(server.users))

    # get_users(all_users,user_dataset)
    # write_result(user_header,user_dataset,user_filename)
    # write_result_yml(users_json,user_filename)

    # get all groups
    all_users, pagination_item = server.groups.get()
    print("\nThere are {} groups on site: ".format(pagination_item.total_available))

    # all_groups = list(TSC.Pager(server.groups))

    # get_groups(all_groups,group_dataset)
    # write_result(user_header,user_dataset,user_filename)
    # write_result_yml(group_json,group_filename)

    # list_directory('~/repos/tableau/site_gitlab/')

    # get all sites
    # site = server.sites.get_by_id('2ae725b5-5a7b-40ba-a05c-35b7aa9ab731')
    # site_attributes = site.__dict__
    # print("\nThere are {} attributes on site: ".format(site.name))
    # write_result_yml(site_attributes,"gitlab_site_attributes")
