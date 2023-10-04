============
TableauConMan
============




.. image:: https://gitlab.com/gitlab-data/tabpy-ConMan/badges/main/pipeline.svg
        :target: https://gitlab.com/gitlab-data/tabpy-ConMan/-/commits/main
        :alt: Pipeline Status

.. image:: https://gitlab.com/gitlab-data/tabpy-ConMan/badges/main/coverage.svg
        :target: https://gitlab.com/gitlab-data/tabpy-ConMan/-/commits/main
        :alt: Coverage report

.. image:: https://gitlab.com/gitlab-data/tabpy-ConMan/-/badges/release.svg
        :target: https://gitlab.com/gitlab-data/tabpy-ConMan/-/releases
        :alt: Latest Release

.. image:: https://gitlab.com/gitlab-data/tabpy-ConMan/-/badges/main/pipeline.svg
        :target: https://gitlab-data.gitlab.io/tabpy-ConMan
        :alt: Documentation



Python project which uses the tableauserverclient package to interact with Tableau, encapsulating operations to configure and manage content on Tableau Server.


* Free software: MIT license

Objectives
----------
The primary objectives of this project are to:

* Provide a way to document and set configurations on Tableau Online using an external file.
* Provide a way to move content (workbooks, datasources, flows) between projects and between Tableau Online sites based on an external file.
* Be structured in a way that allows for orchestration and automation on actions.

The reason for directing the control of these actions to external files is so those files can be a focal point of change control and management.  
Building these actions in a way that can be orchestrated will alow for Tableau Online admins to work more efficiently.

Features
--------

* User Provisioning
    * Add User
    * Set User site role
    * Set User license
* Group Provisioning
    * Add Groups
    * Remove Groups
    * Set Group membership
* Project Provisioning
    * Add Project
    * Remove Project
    * Archive Project
    * Set Content Permissions
    * Set User and Group Permissions
* Workbook Management
    * Archive Workbook
    * Delete Workbook
    * Publish Workbook to Project
    * Copy Workbook to Site
    * Copy Workbook Datasources to Site
    * Update Connection Credentials
* Datasource Management
    * Archive Datasource
    * Delete Datasource
    * Publish Datasource to Project
    * Copy Datasource to Site
    * Update Connection Credentials


Credits
-------

This package was created with Cookiecutter_ and the `gitlab-data/cookiecutter-pypackage`_, which was forked from the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://gitlab.com/audreyr/cookiecutter
.. _gitlab-data/cookiecutter-pypackage: https://gitlab.com/gitlab-data/cookiecutter-pypackage
.. _`audreyr/cookiecutter-pypackage`: https://gitlab.com/audreyr/cookiecutter-pypackage

