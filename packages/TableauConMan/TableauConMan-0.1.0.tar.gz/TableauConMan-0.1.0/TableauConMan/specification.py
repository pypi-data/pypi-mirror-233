"""Module for managing provided specification files"""
from typing import Dict, List
import cerberus
import yaml

from schemas import spec as sch

VALIDATION_ERR_MSG = 'Spec error: {} "{}", field "{}": {}'


class Specification:
    """Class for loading and validating the format of the provided specification"""

    def __init__(self):
        self.site: dict = None
        self.projects: list = None
        self.permission_templates: list = None
        self.groups: list = None
        self.users: list = None
        self.raw_spec: dict = None

    def load_spec(self, raw_spec: dict) -> None:
        """

        :param raw_plan:
        """
        if not isinstance(raw_spec, dict):
            raise TypeError("The raw spec must be a dictionary")

        error_messages = self.ensure_valid_schema(raw_spec)
        if error_messages:
            raise ValueError("\n".join(error_messages))

        self.site = raw_spec.get("site")
        self.projects = raw_spec.get("projects")
        self.permission_templates = raw_spec.get("permission_templates")
        self.groups = raw_spec.get("groups")
        self.users = raw_spec.get("users")
        self.raw_spec = raw_spec

    @staticmethod
    def ensure_valid_schema(self, spec: Dict) -> List[str]:
        """
        Ensure that the provided spec has no schema errors.

        Returns a list with all the errors found.
        """
        error_messages = []

        validator = cerberus.Validator(yaml.safe_load(sch.SPEC_SCHEMA))
        validator.validate(spec)
        for entity_type, err_msg in validator.errors.items():
            if isinstance(err_msg[0], str):
                error_messages.append(f"Spec error: {entity_type}: {err_msg[0]}")
                continue

            for error in err_msg[0].values():
                error_messages.append(f"Spec error: {entity_type}: {error[0]}")
        if error_messages:
            return error_messages

        schema = {
            "projects": yaml.safe_load(sch.SPEC_PROJECTS_SCHEMA),
            "permission_templates": yaml.safe_load(
                sch.SPEC_PERMISSION_TEMPLATES_SCHEMA
            ),
            "groups": yaml.safe_load(sch.SPEC_GROUPS_SCHEMA),
            "users": yaml.safe_load(sch.SPEC_USERS_SCHEMA),
        }

        validators = {
            "projects": cerberus.Validator(schema.get("projects")),
            "permission_templates": cerberus.Validator(
                schema.get("permission_templates")
            ),
            "groups": cerberus.Validator(schema.get("groups")),
            "users": cerberus.Validator(schema.get("users")),
        }

        entities_by_type = []
        for entity_type, entities in spec.items():
            if entities and entity_type in [
                "projects",
                "permission_templates",
                "groups",
                "users",
            ]:
                entities_by_type.append((entity_type, entities))

        for entity_type, entities in entities_by_type:
            for entity_dict in entities:
                validators[entity_type].validate(entity_dict)
                for field, err_msg in validators[entity_type].errors.items():
                    error_messages.append(
                        VALIDATION_ERR_MSG.format(
                            entity_type, entity_dict.get("name"), field, err_msg[0]
                        )
                    )

        return error_messages
