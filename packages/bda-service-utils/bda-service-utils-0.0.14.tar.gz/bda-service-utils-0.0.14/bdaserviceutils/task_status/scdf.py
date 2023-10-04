from ..utils import packages_are_installed

import logging
if not packages_are_installed(["sqlalchemy"]): 
    message = "Please install sqlalchemy (https://pypi.org/project/?) if you want to use scdf."
    logging.warning(message)
    SCDF = None
else:

    from sqlalchemy import create_engine
    from sqlalchemy.sql import text
    import datetime
    from .task_status import TaskStatus
    from ..task_args import get_task_id, get_db_url
    import os

    class SCDF(TaskStatus):
        """Helper class to help manage Task's status in the SCDF DB. """
        
        task_status_type = os.path.basename(__file__).split('.py')[0]

        def __init__(self):
            self.task_id = get_task_id()
            self.engine = create_engine(get_db_url())
            #self.connection = self.engine.connect()

        def running(self):
            """Set the TASK_EXECUTION's START_TIME """
            now = datetime.datetime.now()
            start_task_statement = text(
                "UPDATE TASK_EXECUTION SET START_TIME=:start_time, EXIT_CODE=null, LAST_UPDATED=:last_updated  "
                "WHERE TASK_EXECUTION_ID=:task_id")
            #self.connection.execute(start_task_statement, start_time=now, last_updated=now, task_id=self.task_id)
            self.engine.execute(start_task_statement, start_time=now, last_updated=now, task_id=self.task_id)

        def completed(self):
            # self.task_id = get_task_id()
            # self.engine = create_engine(get_db_url())
            # self.connection = self.engine.connect()

            """Set the TASK_EXECUTION's END_TIME, EXIST_CODE=0 and EXIST_MESSAGE/ERROR_MESSAGE must be null """
            now = datetime.datetime.now()
            complete_task_statement = text(
                "UPDATE TASK_EXECUTION SET END_TIME=:end_time, EXIT_CODE=0, EXIT_MESSAGE=null, ERROR_MESSAGE=null, "
                "LAST_UPDATED=:last_updated  WHERE TASK_EXECUTION_ID=:task_id")
            #self.connection.execute(complete_task_statement, end_time=now, last_updated=now, task_id=self.task_id)
            self.engine.execute(complete_task_statement,  end_time=now, last_updated=now, task_id=self.task_id)

        def failed(self, exit_code, exit_message, error_message=''):
            """Set the TASK_EXECUTION's END_TIME, EXIST_CODE is the error code and EXIST_MESSAGE/ERROR_MESSAGE describe
            the error """
            now = datetime.datetime.now()
            complete_task_statement = text(
                "UPDATE TASK_EXECUTION SET END_TIME=:end_time, EXIT_CODE=:exit_code, EXIT_MESSAGE=:exit_message, "
                "  ERROR_MESSAGE=:error_message, LAST_UPDATED=:last_updated  "
                "WHERE TASK_EXECUTION_ID=:task_id")
            # self.connection.execute(complete_task_statement, end_time=now, exit_code=exit_code,
            #                         exit_message=exit_message, error_message=error_message, last_updated=now,
            #                         task_id=self.task_id)

            exit_message = (exit_message[:100] + '..') if len(exit_message) > 100 else exit_message

            self.engine.execute(complete_task_statement, end_time=now, exit_code=exit_code,
                                    exit_message=exit_message, error_message=error_message, last_updated=now,
                                    task_id=self.task_id)
