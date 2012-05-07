Changelog of lizard-task
===================================================


0.2 (unreleased)
----------------

- Periodic Tasks Ext is clickable again in admin.

- Import simplejson from django.utils.

- Removed unused fields from TaskExecution model

- Added 'task_uuid' field to TaskExecution model

- Added 'null=True' constraint to 'task' field in TaskExecution model

- Added 'task_uuid' parameter to function get_handler in handler.py

- Added function to PeriodicTaskExt model to retrieve the latest state.


0.1 (2012-03-14)
----------------

- Initial library skeleton created by nensskel.  [Alexandr Seleznev]

- Defined admin interface.

- Created logging handler.
