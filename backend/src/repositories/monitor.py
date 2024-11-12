from enum import Enum
from typing import List

from backend.src.repositories.db_service import DBService

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Monitor:
    def __init__(self, monitor_id: int, patient_id: int, parameters: List[str], status: Status):
        self.monitor_id = monitor_id
        self.patient_id = patient_id
        self.parameters = parameters
        self.status = status

    def create_monitor(self, new_monitor: 'Monitor'):
        """
        Creates a new monitor instance.
        """
        # Implementation for creating a new monitor
        createmonitor = """INSERT INTO smartmonitor( workersid, examtype, smartstatus, healthid) 
        values ( %d, %s, %s, %d)"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(createmonitor)
        conn.commit

        pass

    def return_list_of_monitors(self, email: str) -> List['Monitor']:
        """
        Returns a list of monitors associated with the given email.
        """
        # Implementation for returning monitors
        listmonitors = ("""select * from smartmonitor where exist (select email from users where users.email = %s)""")
        
        #search the database. 
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        results = cursor.execute(listmonitors)

        #output the results
        print(results)
        
        pass

    def modify_monitor(self, monitor_id: int):
        """
        Modifies an existing monitor by its ID.
        """
        # Implementation for modifying a monitor
        modifiyMonitor = """update smartmonitor set monitorid =%d, workersid = %d, examtype = %s,
        smartstatus = %s, healtid = %d                  
        where monitorid = %s"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(modifiyMonitor)

        pass

    def remove_monitor(self, monitor_id: int):
        """
        Removes a monitor by its ID.
        """
        # Implementation for removing a monitor
        deleteMonitor = """delete from smartmonitor where monitorid = %d"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(deleteMonitor)
        pass

    def update_monitor_status(self, monitor_id: int):
        """
        Updates the status of a monitor by its ID.
        """
        # Implementation for updating monitor status
        updateMonitor = """update smartmonitor set smartstatus = %s where monitorid = %d """
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(updateMonitor)
        pass

