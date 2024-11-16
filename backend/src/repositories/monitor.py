from enum import Enum
from typing import List

from repositories.db_service import DBService
from repositories.email_manager import EmailManager
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
    @staticmethod
    def create_monitor(doctor_id: int, test_to_monitor: str, status: str, patient_id: int):
        """
        Creates a new monitor instance.
        """
        # Implementation for creating a new monitor
        createmonitor = """INSERT INTO smartmonitor(workersid, testtype, smartstatus, healthid) 
        values ( %s, %s, %s, %s)"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(createmonitor, (doctor_id, test_to_monitor, status, patient_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def return_list_of_monitors(doctor_id: int) -> List['Monitor']:
        """
        Returns a list of monitors associated with the given email.
        """
        # Implementation for returning monitors
        listmonitors = ("""SELECT monitorid, workersid, testtype, smartstatus, healthid FROM smartmonitor WHERE workersID = %s""")
        
        #search the database. 
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(listmonitors, (doctor_id,))
        results = cursor.fetchall()
        list_Of_Monitors = []

        list_Of_Monitors = [{
            'monitorid': row[0],
            'workersid': row[1],
            'testtype': row[2],
            'smartstatus': row[3],
            'healthid': row [4]
         } for row in results] 
        #output the results
        cursor.close()
        del cursor
        conn.close()
        return list_Of_Monitors
    @staticmethod
    def modify_monitor(monitor_id: int, new_status: str, new_test: str, new_patient: int):
        """
        Modifies an existing monitor by its ID.
        """
        # Implementation for modifying a monitor
        modifiyMonitor = """UPDATE smartmonitor SET testtype = %s,
        smartstatus = %s, healthid = %s WHERE monitorid = %s"""
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(modifiyMonitor, (new_test, new_status, new_patient, monitor_id))
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
        listmonitors = ("""SELECT smartmonitor.monitorid, workers.email
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
        tocheck = cursor.fetchall()
        for value in tocheck:
            Monitor.update_monitor_status("sent", value[0])
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

