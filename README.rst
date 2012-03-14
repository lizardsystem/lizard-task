Running cellery tasks from admin interface with lizard-task
===========================================================


What lizard-task does
-------------------------

- Lizard-task provides the possability to run periodic tasks from
  admin interface
- Lizard-task provides the possability to view loggings of executed
  tasks
- Lizard-task provides the possability to filter task and logging 
  using lizard-security
- lizard-task provides the logging handler to save logging messages
  into database


Usage in our project
--------------------


Usage loggin handler
---------------------
To use logging handler of lizard-task set 
- Create handler for each task

  from lizard_task.handler import get_handler
  handler = get_handler('<<task_name>>', '<<username>>')

- Add handler to your logging logger
  
  logger.addHandler(handler)

- Depends on logging 



