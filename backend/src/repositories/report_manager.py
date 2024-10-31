from enum import Enum
import datetime
import db_service
class ReportType(Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"
    PREDICTION = "prediction"

class ReportManager:
    def __init__(self, report_id: int, report_type: ReportType, date_created: str, content: str):
        self.report_id = report_id
        self.report_type = report_type
        self.date_created = date_created
        self.content = content

    def return_list_of_reports(self, email: str) -> list:
        """
        Returns a list of reports associated with the given email.
        """
        # Implementation for returning reports

        pass

    def generate_summary_report(self, year: int, month: int, userID: int):
        """
        Generates a new report.
        """
         # Implementation for generating a report
        patientIDList = []
        patientTestList = []
        patientAbTestList = []
        today = datetime.date

        conn = db_service.get_db_connection
        cursor = conn.cursor()
       
        #query to get all patients
        patientQry = "SELECT HealthID FROM patient"
        # queries to count tests for patient within given timeframe.
        resultQryY = "SELECT * FROM testresults WHERE healthID = ? AND YEAR (date) = ?"
        resultQryM = "SELECT * FROM testresults WHERE healthID = ? AND MONTH(date) = ? AND YEAR (date) = ?"
        # queries to count abnormal tests for patient within given timeframe
        countQryY2 = """SELECT COUNT(results) FROM testresults 
                        LEFT JOIN testtypes ON testresults.testtype = testtypes.testtype 
                        LEFT JOIN examtable ON testresults.examid = examtable.examid
                        WHERE examtable.healthid = ? AND YEAR (testresults.resultdate) = ?
                        AND NOT (testtypes.lowerbound < testresults.results < testtypes.upperbound )"""
        
        countQryM2 = """SELECT COUNT(results)
                        FROM testresults 
                        LEFT JOIN testtypes ON testresults.testtype = testtypes.testtype 
                        LEFT JOIN examtable ON testresults.examid = examtable.examid
                        WHERE examtable.healthid =? AND YEAR (testresults.resultdate) =? AND MONTH(testresults.resultdate) =?
                        AND NOT (testtypes.lowerbound < testresults.results < testtypes.upperbound )"""
        MakeReportQry     = """INSERT into summaryreport (workersid, monthoryear, summarydate, timeperiod)
                            VALUES (?, ?, ?, ?);"""
        PreMakeReportQry = "SELECT Auto_increment FROM information_schema.tables WHERE table_name='predictreports';"
        MakeReportEntryQry  = "INSERT INTO summaryreportentries (healthid, noofexams, abnormalexams) VALUES(?, ?, ?);"
       
        if month == 0:
            mOrY = "year"
            timeperiod = "{year}"
        else:
            mOrY = "month"
            timeperiod = "{month}-{year}"

        #Fetch report number of new report, store it, then make report
        cursor.execute(PreMakeReportQry)
        reportID: int = cursor.fetchone()
        cursor.execute(MakeReportQry, (userID, mOrY, today, timeperiod))

        #Fetch all patients in Database, place in list
        cursor.execute(patientQry)
        results = cursor.fetchall()
        for row in results:
            patientIDList.append
        # Count tests per patient, place count in separate list
        if month == 0:
             for val in patientIDList:
                 cursor.execute(resultQryY, (val, year))
                 patientTestList.append = cursor.fetchone()
        else:
            for val in patientIDList:
                 cursor.execute(resultQryM, (val, month, year))
                 patientTestList.append = cursor.fetchone()
        # Count unusual tests per patient, place in list
        if month == 0:
             for val in patientIDList:
                 cursor.execute(countQryY2, (val, year, month))
                 patientAbTestList.append = cursor.fetchone()
        else:
            for val in patientIDList:
                 cursor.execute(countQryM2, (val, year, month))
                 patientAbTestList.append = cursor.fetchone()
        #Now make individual report entries
        i = 0
        for val in patientIDList:
            cursor.execute(MakeReportEntryQry(val,patientTestList[i], patientAbTestList[i] ))
            i + 1

        

    def remove_report(self, report_id: int):
        """
        Removes a report by its ID.
        """
        # Implementation for removing a report
        pass

    def send_report(self, receiver_email: str):
        """
        Sends the report to the specified email address.
        """
        # Implementation for sending the report
        pass

    def download_report(self):
        """
        Downloads the report.
        """
        # Implementation for downloading the report
        pass

