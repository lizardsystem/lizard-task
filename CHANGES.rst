Changelog of lizard-task
===================================================


0.6 (unreleased)
----------------

- Made auto refreshing task execution page conditional on task state.


0.5 (2012-05-09)
----------------

- Added migration, renamed a column. You may need to clear
  TaskExecution before migration.


0.4 (2012-05-09)
----------------

- Fixed DBLoggingHandler when no task_execution is provided.

- Added task execution view with logging and details.


0.3 (2012-05-08)
----------------

- Added task detail view.

- Added migrations for 0.2.


0.2 (2012-05-08)
----------------

Things to do after upgrading:

- Clear the TaskExecution table


Changed:

- Exchanged Periodic Task Ext for SecuredPeriodicTask.

- Import simplejson from django.utils.

- Removed unused fields from TaskExecution model

- Added 'task_uuid' field to TaskExecution model

- Added 'null=True' constraint to 'task' field in TaskExecution model

- Added 'task_uuid' parameter to function get_handler in handler.py

- Added SecuredPeriodicTask model with latest_state function.

- Removed djcelery.PeriodicTask from admin, because
  SecuredPeriodicTask completely replaces it.


0.1 (2012-03-14)
----------------

- Initial library skeleton created by nensskel.  [Alexandr Seleznev]

- Defined admin interface.

- Created logging handler.
