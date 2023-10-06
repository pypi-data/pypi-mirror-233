"""
This file describes the expected schema for a spec file.
These schemas are used to both parse and validate spec files.
"""


SPEC_SCHEMA = """
    version:
        type: string
        required: False

    site:
        type: dict
        required: False
        keyschema:
            type: string


    projects:
        type: list
        schema:
            type: dict
            keyschema:
                type: string
            valuesrules:
                anyof:
                  - type: string
                  - type: list

    permission_templates:
        type: list
        schema:
            type: dict
            keyschema:
                type: string
            valuesrules:
                anyof:
                  - type: string
                  - type: list
                  - type: dict
    groups:
        type: list
        schema:
            type: dict
            keyschema:
                type: string
            valuesrules:
                type: string
    users:
        type: list
        schema:
            type: dict
            keyschema:
                type: string
            valuesrules:
                anyof:
                  - type: string
                  - type: list

"""

SPEC_PROJECTS_SCHEMA = """
    project_name:
        type: string

    description:
        type: string

    content_permissions:
        type: string

    project_path:
        type: string

    permission_set:
        type: list
        schema:
            type: dict
            allowed:
                - group_name
                - permission_rule
            keyschema:
                type: string
            valuesrules:
                type: string
            
"""

SPEC_PERMISSION_TEMPLATES_SCHEMA = """
    name:
      type: string

    workbook:
      type: dict
      allowed:
          - Read
          - Filter
          - ViewComments
          - AddComment
          - ExportImage
          - ExportData
          - ShareView
          - ViewUnderlyingData
          - WebAuthoring
          - RunExplainData
          - ExportXml
          - Write
          - CreateRefreshMetrics
          - ChangeHierarchy
          - ChangePermissions
          - Delete
      keyschema:
          type: string
      valuesrules:
          type: string
          allowed:
              - Allow
              - Deny

    project:
      type: dict
      allowed:
          - Read
          - Write
          - ProjectLeader
      keyschema:
          type: string
      valuesrules:
          type: string
          allowed:
              - Allow
              - Deny

    datasource:
        type: dict
        allowed:
            - Read
            - Connect
            - ExportXml
            - Write
            - SaveAs
            - ChangeHierarchy
            - ChangePermissions
            - Delete
        keyschema:
          type: string
        valuesrules:
            type: string
            allowed:
                - Allow
                - Deny

    flow:
        type: dict
        allowed:
            - Read
            - ExportXml
            - Execute
            - Write
            - WebAuthoringForFlows
            - ChangeHierarchy
            - ChangePermissions
            - Delete
        keyschema:
          type: string
        valuesrules:
            type: string
            allowed:
                - Allow
                - Deny

    datarole:
        type: dict
        allowed:
            - Read
            - Write
            - ChangeHierarchy
            - ChangePermissions
            - Delete
        keyschema:
          type: string
        valuesrules:
            type: string
            allowed:
                - Allow
                - Deny

    lens:
        type: dict
        allowed:
            - Read
            - Write
            - ChangeHierarchy
            - ChangePermissions
            - Delete
        keyschema:
          type: string
        valuesrules:
            type: string
            allowed:
                - Allow
                - Deny

    metric:
        type: dict
        allowed:
            - Read
            - Write
            - ChangeHierarchy
            - ChangePermissions
            - Delete
        keyschema:
          type: string
        valuesrules:
            type: string
            allowed:
                - Allow
                - Deny

    virtual_connection:
        type: dict
        allowed:
            - Read
            - Connect
            - Write
            - ChangeHierarchy
            - ChangePermissions
            - Delete
        keyschema:
          type: string
        valuesrules:
            type: string
            allowed:
                - Allow
                - Deny

    database:
        type: dict
        allowed:
            - Read
            - Write
            - ChangeHierarchy
            - ChangePermissions
        keyschema:
          type: string
        valuesrules:
            type: string
            allowed:
                - Allow
                - Deny

    table:
        type: dict
        allowed:
            - Read
            - Write
            - ChangeHierarchy
            - ChangePermissions
        keyschema:
          type: string
        valuesrules:
            type: string
            allowed:
                - Allow
                - Deny



"""

SPEC_GROUPS_SCHEMA = """

    group_name:
        type: string
"""

SPEC_USERS_SCHEMA = """

    user_name: 
        type: string

    site_role:
        type: string
        allowed:
            - SiteAdministratorCreator
            - Creator
            - SiteAdministratorExplorer
            - ExplorerCanPublish
            - Explorer
            - Viewer
            - Unlicensed
    
    auth_setting:
        type: string
        allowed:
            - SAML
            - TableauIDWithMFA

    groups:
        type: list
"""
