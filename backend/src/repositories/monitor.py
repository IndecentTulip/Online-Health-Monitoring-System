from enum import Enum
from typing import List

from repositories.db_service import DBService

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
@staticmethod
class Monitor:
    def __init__(monitor_id: int, doctor_id: int, test_to_monitor: str, status: Status, patient_id: int):
        self.doctor_id = doctor_id
        self.monitor_id = monitor_id
        self.patient_id = patient_id
        self.test_to_monitor = test_to_monitor
        self.status = status
    @staticmethod
    def create_monitor(self, new_monitor: 'Monitor'):
        """
        Creates a new monitor instance.
        """
        # Implementation for creating a new monitor
        createmonitor = """INSERT INTO smartmonitor( workersid, examtype, smartstatus, healthid) 
        values ( %s, %s, %s, %s)"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(createmonitor, (new_monitor.doctor_id, new_monitor.test_to_monitor, new_monitor.status, new_monitor.patient_id))
        conn.commit
        cursor.close()
        del cursor
        conn.close()

    @staticmethod
    def return_list_of_monitors(doctor_id: int) -> List['Monitor']:
        """
        Returns a list of monitors associated with the given email.
        """
        # Implementation for returning monitors
        listmonitors = ("""SELECT monitorid, workersid, testtype, smartstatus, healthid FROM smartmonitor WHERE doctor_id = %s""")
        
        #search the database. 
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(listmonitors, (doctor_id))
        results = cursor.fetchall
        list_Of_Monitors = []
        for row in results:
            list_monitor = Monitor(row[0], row[1], row[2], row[3], row[4])
            list_Of_Monitors.append(list_monitor)
        #output the results
        cursor.close()
        del cursor
        conn.close()
        return list_Of_Monitors
    @staticmethod
    def modify_monitor(monitor_id: int, new_status: Status, new_test: str, new_patient: int):
        """
        Modifies an existing monitor by its ID.
        """
        # Implementation for modifying a monitor
        modifiyMonitor = """UPDATE smartmonitor SET examtype = %s,
        smartstatus = %s, healtid = %s WHERE monitorid = %s"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(modifiyMonitor, (new_test, new_status, new_patient))
        conn.commit()
        cursor.close()
        del cursor
        conn.close()

    @staticmethod
    def remove_monitor(monitor_id: int):
        """
        Removes a monitor by its ID.
        """
        # Implementation for removing a monitor
        deleteMonitor = """DELETE FROM smartmonitor WHERE monitorid = %s"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(deleteMonitor, (monitor_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def check_monitors():
        listmonitors = ("""SELECT smartmonitor.monitorid, smartmonitor.email
        FROM smartmonitor LEFT JOIN examtable ON smartmonitor.healthid = examtable.healthid
        LEFT JOIN testresults ON (examtable.examid = testresults.examid AND smartmonitor.testtype =  testresults.testtype)
        LEFT JOIN testtypes ON smartmonitor.testtype = testtypes.testtype
        LEFT JOIN workers ON smartmonitor.workersid = workers.workerID
        WHERE smartmonitor.smartstatus = 'not sent'
        AND ((testtypes.lowerbound < testresults.results) AND (testresults.results < testtypes.upperbound ))""")
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(listmonitors)
        tonotify = cursor.fetchall()
        for value in tocheck:
            update_monitor_status("sent", value[0])
            EmailManager.send_notification("alert", value[1])
        conn.commit()
        cursor.close()
        conn.close()
            
    @staticmethod
    def update_monitor_status(new_status: str, monitor_id: int):
        """
        Updates the status of a monitor by its ID.
        """
        # Implementation for updating monitor status
        updateMonitor = """update smartmonitor set smartstatus = %s where monitorid = %s """
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(updateMonitor, (new_status, monitor_id,))
        conn.commit()
        cursor.close()
        conn.close()

