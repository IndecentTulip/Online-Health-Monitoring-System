from enum import Enum
import datetime
from repositories.db_service import DBService

class ReportType(Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"
    PREDICTION = "prediction"
class PredictEntry:
    pass
class SumEntry:
    pass
class ReportManager:
    def __init__(self, report_id: int, report_type: ReportType, date_created: str, content: str):
        self.report_id = report_id
        self.report_type = report_type
        self.date_created = date_created
        self.content = content

    def return_list_of_reports(self, type: int) -> list:
        """
        Returns a list of reports of given type
        """
        # Implementation for returning reports
        if type == 0:
            getReports = "SELECT * FROM summaryreport"
        elif type ==1:
            getReports = "SELECT preportid FROM predictreports"
        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
        cursor.execute(getReports)
        listofstuff = cursor.fetchall
        cursor.close()
        del cursor
        return listofstuff
    def generate_predict_report (self, patient: int, year: int):

        findTestTypes = """SELECT UNIQUE testypes FROM testresults LEFT JOIN testtypes ON testresults.testtype = testtypes.testtype
                            LEFT JOIN examtable ON testresults.examid = examtable.examid
                            WHERE examtable.healthid = %s AND NOT (testtypes.lowerbound < testresulsts.results < testtypes.upperbound) AND YEAR (testresults.resultdate) =%s"""
        getTestResults = """"SELECT results, upperbound, lowerbound () AS abnormal FROM testresults LEFT JOIN examtable ON testresults.examid = examtable.examid
                             WHERE examtable.healthid = %s AND YEAR (testresults.resultdate) =%s ORDER BY testresults.resultdate DESC"""
        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
        cursor.execute (findTestTypes, (patient, year))
        testtypes = cursor.fetachall

        cursor.close()
        del cursor
    def generate_summary_report(self, year: int, month: int, userID: int):
        """
        Generates a new report.
        """
         # Implementation for generating a report
        patientIDList = []
        patientTestList = []
        patientAbTestList = []
        today = datetime.date

        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
       
        #query to get all patients
        patientQry = "SELECT HealthID FROM patient"
        # queries to count tests for patient within given timeframe.
        resultQryY = "SELECT COUNT(results) FROM testresults WHERE healthID = %s AND YEAR (date) = %s"
        resultQryM = "SELECT COUNT(results) FROM testresults WHERE healthID = %s AND MONTH(date) = %s AND YEAR (date) = %s"
        # queries to count abnormal tests for patient within given timeframe
        countQryY2 = """SELECT COUNT(results) FROM testresults 
                        LEFT JOIN testtypes ON testresults.testtype = testtypes.testtype 
                        LEFT JOIN examtable ON testresults.examid = examtable.examid
                        WHERE examtable.healthid = %s AND YEAR (testresults.resultdate) = %s
                        AND NOT (testtypes.lowerbound < testresults.results < testtypes.upperbound )"""
        
        countQryM2 = """SELECT COUNT(results)
                        FROM testresults 
                        LEFT JOIN testtypes ON testresults.testtype = testtypes.testtype 
                        LEFT JOIN examtable ON testresults.examid = examtable.examid
                        WHERE examtable.healthid =%s AND YEAR (testresults.resultdate) =%s AND MONTH(testresults.resultdate) =%s
                        AND NOT (testtypes.lowerbound < testresults.results < testtypes.upperbound )"""
        MakeReportQry     = """INSERT into summaryreport (workersid, monthoryear, summarydate, timeperiod)
                            VALUES (%s, %s, %s, %s);"""
        PreMakeReportQry = "SELECT Auto_increment FROM information_schema.tables WHERE table_name='predictreports';"
        MakeReportEntryQry  = "INSERT INTO summaryreportentries (sreportid, healthid, noofexams, abnormalexams) VALUES(%s, %s, %s, %s);"
       
        if month == 0:
            mOrY = "year"
            timeperiod = f"{year}"
        else:
            mOrY = "month"
            timeperiod = f"{month}-{year}"

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
            cursor.execute(MakeReportEntryQry, (reportID, val,patientTestList[i], patientAbTestList[i] ))
            i += 1
            
        cursor.close()
        del cursor
        

    def remove_report(self, report_id: int, report_type: int):
        """
        Removes a report by its ID.
        """
        # Implementation for removing a report
        # 0 Means summary, 1 means predict
        deleteEnt = ''
        deleteRep = ''
        if report_type == 0:
            deleteEnt = "DELETE FROM summaryreportentries WHERE sreportid = %s"
            deleteRep = "DELETE FROM summaryreport WHERE sreportid = %s"
        else:
            if report_type == 1:
                deleteEnt = "DELETE FROM predictreportsentries WHERE sreportid = %s"
                deleteRep = "DELETE FROM predictreports WHERE sreportid = %s"

        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(deleteEnt, (report_id))
        cursor.execute(deleteRep, (report_id))

        cursor.close()
        del cursor
        
      

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

