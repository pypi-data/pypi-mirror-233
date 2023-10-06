import os
import tableauserverclient as TSC
import yaml
from loguru import logger


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


def get_spec_group_list(spec_file_path: str):
    """

    :param spec_file_path:
    :return:
    """
    with open(spec_file_path, "r") as stream:
        try:
            group_list = yaml.safe_load(stream).get("groups")
            return group_list
        except yaml.YAMLError as exc:
            print(exc)


def get_spec_user_list(spec_file_path):
    """

    :param spec_file_path:
    :return:
    """
    with open(spec_file_path, "r") as stream:
        try:
            user_list = yaml.safe_load(stream).get("users")
            return user_list
        except yaml.YAMLError as exc:
            print(exc)


def get_spec_group_membership(spec_file_path: str):
    user_list = get_spec_user_list(spec_file_path)
    group_list = get_spec_group_list(spec_file_path)

    # print(group_list)
    for group in group_list:
        group.update({"users": []})
        for user in user_list:
            if "groups" in user:
                for user_group in user.get("groups"):
                    if user_group == group.get("group_name"):
                        group.get("users").append(user.get("user_name"))

                    if user_group not in (
                        d.get("group_name") for d in group_list
                    ):  # group in group_list:
                        output.append(
                            f"An exception occurred: Group {user_group} on user {user.get('user_name')} is not valid"
                        )
                        # print(f"An exception occurred: Group {user_group} on user {user['user_name']} is not valid" )

    # print(group_list)
    return group_list


def get_server_groups(server):
    with server.auth.sign_in(tableau_auth):
        all_groups = list(TSC.Pager(server.groups))

    return all_groups


def get_server_group_membership_dep(all_groups):
    server_group_membership = []

    for group in all_groups:
        group_dict = {"group_name": group.name, "users": []}

        for user in group.users:
            group_dict.get("users").append(user.name)

        server_group_membership.append(group_dict)

    # print(server_group_membership)
    return server_group_membership


def get_server_group_membership(server):
    with server.auth.sign_in(tableau_auth):
        all_groups = list(TSC.Pager(server.groups))

        server_group_membership = []

        for group in all_groups:
            server.groups.populate_users(group)

            group_dict = {"group_name": group.name, "users": []}

            for user in group.users:
                group_dict.get("users").append(user.name)

            server_group_membership.append(group_dict)

    # print(server_group_membership)
    return server_group_membership


def get_group_list(group_membership_list):
    group_list = []
    for group in group_membership_list:
        group_list.append(group.get("group_name"))
    # print(group_list)
    return group_list


def get_member_list(group_membership_list, group_name):
    member_list = []
    for group in group_membership_list:
        # print(group['group_name'],group_name)
        if group.get("group_name") == group_name:
            member_list = group.get("users")
    # print(member_list)
    return member_list


def get_list_overlaps(list_a, list_b):
    # print(list_a)
    in_a_and_b = list(set(list_a) & set(list_b))
    in_a_not_b = list(set(list_a) ^ set(in_a_and_b))
    in_b_not_a = list(set(list_b) ^ set(in_a_and_b))
    # print(in_b_not_a)
    return in_a_and_b, in_a_not_b, in_b_not_a


def create_server_group(server, group_name):
    # create a new instance with the group name
    new_group = TSC.GroupItem(group_name)

    # call the create method
    # with server.auth.sign_in(tableau_auth):
    #  server.groups.create(new_group)
    output.append(f"  {new_group.name}")
    # print(f"  {new_group.name}", file=open('output.txt', 'a'))


def remove_server_group(server, group):
    # with server.auth.sign_in(tableau_auth):
    # server.groups.delete(group)
    output.append(f"  {group.name}")
    # print(f"  {group.name}", file=open('output.txt', 'a'))


def get_server_group(server_groups, group_name):
    try:
        group = list(filter(lambda x: x.name == group_name, server_groups))[0]
        # print(group_name, group)
        return group
    except Exception as exc:
        output.append(f"Could not find group: {group_name} on the server")
        # print(f"Could not find group: {group_name} on the server", file=open('output.txt', 'a'))
        logger.debug(exc)


def get_server_group_dep(server, group_name):
    req_options = TSC.RequestOptions()
    req_options.filter.add(
        TSC.Filter(
            TSC.RequestOptions.Field.Name,
            TSC.RequestOptions.Operator.Equals,
            group_name,
        )
    )
    try:
        with server.auth.sign_in(tableau_auth):
            group = server.groups.get(req_options=req_options)[0][0]
        # print(group_name, group)
        return group
    except Exception as exc:
        output.append(f"Could not find group: {group_name} on the server")
        # print(f"Could not find group: {group_name} on the server", file=open('output.txt', 'a'))
        logger.debug(exc)


def get_server_users(server):
    with server.auth.sign_in(tableau_auth):
        all_users = list(TSC.Pager(server.users))
    return all_users


def get_server_user(server_users, user_name):
    try:
        user = list(filter(lambda x: x.name == user_name, server_users))[0]
        return user
    except Exception as exc:
        output.append(f"Could not find user: {user_name} on the server")
        # print(f"Could not find user: {user_name} on the server", file=open('output.txt', 'a'))
        logger.debug(exc)


def get_server_user_dep(server, user_name):
    req_options = TSC.RequestOptions()
    req_options.filter.add(
        TSC.Filter(
            TSC.RequestOptions.Field.Name, TSC.RequestOptions.Operator.Equals, user_name
        )
    )

    with server.auth.sign_in(tableau_auth):
        try:
            user = server.users.get(req_options=req_options)[0][0]
            return user
        except Exception as exc:
            output.append(f"Could not find user: {user_name} on the server")
            # print(f"Could not find user: {user_name} on the server", file=open('output.txt', 'a'))
            logger.debug(exc)
    # print(user)


def add_group_user(server, group, user):
    # with server.auth.sign_in(tableau_auth):
    #  server.groups.add_user(group, user.id)
    output.append(f"  {user.name}")
    # print(f"  {user.name}", file=open('output.txt', 'a'))


def remove_group_user(server, group, user):
    # with server.auth.sign_in(tableau_auth):
    # server.groups.remove_user(group, user.id)
    output.append(f"  {user.name}")
    # print(f"  {user.name}", file=open('output.txt', 'a'))


def provision_groups():
    output.append("****** Users with Groups not in Spec ******")
    spec_group_membership = get_spec_group_membership(SPEC_FILE_PATH)
    server_groups = get_server_groups(server)
    server_group_membership = get_server_group_membership(server)

    server_group_list = get_group_list(server_group_membership)
    spec_group_list = get_group_list(spec_group_membership)

    common, to_delete, to_create = get_list_overlaps(server_group_list, spec_group_list)

    # print(to_create)

    output.append("****** Groups on Server but not in Spec ******")
    # print("****** Groups on Server but not in Spec ******", file=open('output.txt', 'a'))
    for group_name in to_delete:
        group = get_server_group(server_groups, group_name)
        if group is not None:
            remove_server_group(server, group)

    output.append("****** Groups in Spec but not on Server ******")
    # print("****** Groups in Spec but not on Server ******", file=open('output.txt', 'a'))
    for group_name in to_create:
        create_server_group(server, group_name)


def provision_group_memberships():
    spec_group_membership = get_spec_group_membership(SPEC_FILE_PATH)
    server_group_membership = get_server_group_membership(server)
    server_groups = get_server_groups(server)
    server_users = get_server_users(server)

    for spec_group in spec_group_membership:
        group_name = spec_group.get("group_name")
        if group_name != "All Users":
            spec_group_members = get_member_list(spec_group_membership, group_name)
            server_group_members = get_member_list(server_group_membership, group_name)

            common, to_remove, to_add = get_list_overlaps(
                server_group_members, spec_group_members
            )

            output.append(
                f"****** Users on Server but not in Spec in group {group_name} ******"
            )
            # print(f"****** Users on Server but not in Spec in group {group_name} ******", file=open('output.txt', 'a'))
            for user_name in to_remove:
                user = get_server_user(server_users, user_name)
                group = get_server_group(server_groups, group_name)
                if user is not None and group is not None:
                    remove_group_user(server, group, user)

            output.append(
                f"****** Users in Spec but not on Server in group {group_name} ******"
            )
            # print(f"****** Users in Spec but not on Server in group {group_name} ******", file=open('output.txt', 'a'))
            # logging.critical(f"****** Users in Spec but not on Server in group {group_name} ******")
            for user_name in to_add:
                user = get_server_user(server_users, user_name)
                group = get_server_group(server_groups, group_name)
                if user is not None and group is not None:
                    add_group_user(server, group, user)


if __name__ == "__main__":
    print("Provisioning Groups")
    provision_groups()
    print("Provisioning Membership")
    provision_group_memberships()

    with open("output.txt", mode="wt", encoding="utf-8") as output_file:
        output_file.write("\n".join(output))
