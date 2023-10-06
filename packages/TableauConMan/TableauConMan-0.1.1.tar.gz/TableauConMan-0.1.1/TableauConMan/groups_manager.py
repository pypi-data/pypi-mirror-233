from typing import Optional
from assets_manager import AssetsManager
from specification import Specification
from yaml_connector import YamlConnector
from helpers import utils
import tableauserverclient as TSC
from loguru import logger


class GroupsManager(AssetsManager):
    def __init__(self, plan) -> None:
        """

        :param plan:
        """
        AssetsManager.__init__(self, plan)
        self.target_groups: Optional[list[TSC.GroupItem]] = None
        self.target_groups_list: Optional[list] = None
        self.target_group_memberships_list: Optional[list] = None
        self.reference_groups: Optional[list[TSC.GroupItem]] = None
        self.reference_groups_list: Optional[list] = None
        self.reference_group_memberships_list: Optional[list] = None
        self.target_users: Optional[list] = None
        self.reference_users: Optional[list] = None

    def populate_groups(self):
        """
        Use object properties to get a comparable list of workbooks from the source and reference
        """

        full_target_groups, full_target_groups_list = self.generate_server_list(
            self.plan.target, self.AssetType.Groups
        )

        self.target_groups_list = list(
            filter(lambda x: x != "All Users", full_target_groups_list)
        )

        self.target_groups = list(
            filter(lambda x: x.name != "All Users", full_target_groups)
        )

        group_memberships = list()

        for group in self.target_groups:
            with self.plan.target.connect():
                self.plan.target.server.groups.populate_users(group)

                group_membership_dict = {"group_name": group.name, "users": []}

                for user in group.users:
                    group_membership_dict.get("users").append(user.name)

                group_memberships.append(group_membership_dict)

        self.target_group_memberships_list = group_memberships

        # Load the spec as part of the Plan?
        """plan_reference = self.plan.raw_plan.get("reference")
        spec_file_path = plan_reference.get("file_path")

        raw_spec = YamlConnector(spec_file_path)

        spec = Specification()
        spec.load_spec(raw_spec.get_yaml())"""

        spec = self.plan.reference

        filtered_groups = list(
            filter(lambda x: x.get("group_name") != "All Users", spec.groups)
        )

        self.reference_groups_list = list(x.get("group_name") for x in filtered_groups)

        self.reference_group_memberships_list = filtered_groups.copy()

        for group in self.reference_group_memberships_list:
            group.update({"users": []})
            for user in spec.users:
                if "groups" in user:
                    for user_group in user.get("groups"):
                        if user_group == group.get("group_name"):
                            group.get("users").append(user.get("user_name"))

                        if user_group not in (
                            x.get("group_name")
                            for x in self.reference_group_memberships_list
                        ):
                            logger.warning(
                                f"An exception occurred: Group {user_group} on user {user.get('user_name')} is not valid"
                            )

    def populate_users(self):
        full_target_users, full_target_users_list = self.generate_server_list(
            self.plan.target, self.AssetType.Users
        )

        self.target_users = full_target_users

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

    def get_group_changes(self):
        """

        :return:
        """
        common, to_remove, to_add = self.get_changes(
            self.target_groups_list, self.reference_groups_list
        )

        update_list = list()

        for group_name in common:
            reference_membership, target_membership = self.get_group_memberships(
                group_name
            )

            logger.debug(
                f"Group: {group_name} | Target: {set(target_membership)} | Reference: {set(reference_membership)} | Check: {set(target_membership) != set(reference_membership)}"
            )

            if set(target_membership) != set(reference_membership):
                update_list.append(group_name)

        return to_add, to_remove, update_list

    def get_group_memberships(self, group_name):
        reference_membership_group = utils.get_filtered_dict_list(
            self.reference_group_memberships_list, group_name, "group_name"
        )[0]
        reference_membership = reference_membership_group.get("users")

        try:
            target_membership_group = utils.get_filtered_dict_list(
                self.target_group_memberships_list, group_name, "group_name"
            )[0]

            target_membership = target_membership_group.get("users")
        except:
            target_membership = list()

        logger.debug(
            f"Group: {group_name} | Reference Memberships: {self.reference_group_memberships_list} | Target Memberships: {self.target_group_memberships_list} | Reference Users: {reference_membership} | Target Users: {target_membership} "
        )

        return reference_membership, target_membership

    def delete_group(self, group):
        with self.plan.target.connect():
            self.plan.target.server.groups.delete(group.id)
            logger.info(f"Group {group.name} was removed from the server")

    def create(self, group_name):
        # create a new instance with the group name
        new_group = TSC.GroupItem(group_name)

        with self.plan.target.connect():
            created_group = self.plan.target.server.groups.create(new_group)
            logger.info(f"Group {created_group} was added to the server")

        return created_group

    def add_user(self, group_item, user_item):
        with self.plan.target.connect():
            self.plan.target.server.groups.add_user(group_item, user_item.id)
        logger.info(f"User {user_item.name} was added to group {group_item.name}")

    def remove_user(self, group_item, user_item):
        with self.plan.target.connect():
            self.plan.target.server.groups.remove_user(group_item, user_item.id)
        logger.info(f"User {user_item.name} was removed from group {group_item.name}")

    def update_group_membership(self, group_item):
        group_name = group_item.name
        reference_membership, target_membership = self.get_group_memberships(group_name)

        common, to_remove, to_add = self.get_changes(
            target_membership, reference_membership
        )

        logger.debug(f"Group: {group_name}, Add: {to_add}, Remove: {to_remove}")

        for user in to_add:
            user_item = utils.get_item_from_list(user, self.target_users)
            self.add_user(group_item, user_item)

        for user in to_remove:
            user_item = utils.get_item_from_list(user, self.target_users)
            self.remove_user(group_item, user_item)

        logger.info(f"Added {len(to_add)} users and removed {len(to_remove)} users")

    def add(self, list_to_add: list):
        """ """

        if len(list_to_add) > 0:
            for group_name in list_to_add:
                logger.info(f"Processing the addition of Group: {group_name}")

                created_group = self.create(group_name)

                self.update_group_membership(created_group)

        logger.info(f"Added {len(list_to_add)} Groups")

    def remove(self, remove_list: list):
        """
        Match the workbook from list to reference object
        Delete Workbook
        """
        if len(remove_list) > 0:
            for group_name in remove_list:
                group = self.get_item_from_list(group_name, self.target_groups)
                logger.debug(f"Group to Remove: {group}")

                self.delete_group(group)
        logger.info(f"Removed {len(remove_list)} Groups")

    def update(self, update_list: list):
        """ """
        if len(update_list) > 0:
            for group_name in update_list:
                group_item = self.get_item_from_list(group_name, self.target_groups)

                self.update_group_membership(group_item)
        logger.info(f"Updated {len(update_list)} Groups")
