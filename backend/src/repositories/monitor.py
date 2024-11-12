from enum import Enum
from typing import List

from backend.src.repositories.db_service import DBService

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Monitor:
    def __init__(self, monitor_id: int, doctor_id: int, test_to_monitor: str, status: Status, patient_id: int):
        self.doctor_id = doctor_id
        self.monitor_id = monitor_id
        self.patient_id = patient_id
        self.test_to_monitor = test_to_monitor
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
        cursor.execute(createmonitor, (new_monitor.doctor_id, new_monitor.test_to_monitor, new_monitor.status, new_monitor.patient_id))
        conn.commit
        cursor.close()
        del cursor
        conn.close()


    def return_list_of_monitors(self, doctor_id: int) -> List['Monitor']:
        """
        Returns a list of monitors associated with the given email.
        """
        # Implementation for returning monitors
        listmonitors = ("""SELECT monitorid, workersid, testtype, smartstatus, healthid FROM smartmonitor WHERE doctor_id = %d""")
        
        #search the database. 
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(listmonitors, (doctor_id))
        results = cursor.fetchall
        list_Of_Monitors = []
        for row in results:
            list_monitor = Monitor(row[1], row[2], row[3], row[4], row[5])
            list_Of_Monitors.append(list_monitor)
        #output the results
        cursor.close()
        del cursor
        conn.close()
        return list_Of_Monitors

    def modify_monitor(self, monitor_id: int, new_status: Status, new_test: str, new_patient: int):
        """
        Modifies an existing monitor by its ID.
        """
        # Implementation for modifying a monitor
        modifiyMonitor = """UPDATE smartmonitor SET examtype = %s,
        smartstatus = %s, healtid = %d WHERE monitorid = %s"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(modifiyMonitor, (new_test, new_status, new_patient))
        conn.commit()
        cursor.close()
        del cursor
        conn.close()


    def remove_monitor(self, monitor_id: int):
        """
        Removes a monitor by its ID.
        """
        # Implementation for removing a monitor
        deleteMonitor = """DELETE FROM smartmonitor WHERE monitorid = %d"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(deleteMonitor, (monitor_id))
        conn.commit()
        cursor.close()
        del cursor
        conn.close()

    #Why is this separate from update method? Not implemented properly
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

