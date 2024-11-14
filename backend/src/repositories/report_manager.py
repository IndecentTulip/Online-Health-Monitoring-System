from enum import Enum
from datetime import date, datetime
from repositories.db_service import DBService

import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class ReportType(Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"
    PREDICTION = "prediction"

class PredictEntry:
    def __init__(self, concern: int, type: str):
        self.concern = int(concern)
        self.type = type
class SumEntry:
    pass
class ReportManager:
    def __init__(self, report_id: int, report_type: ReportType, date_created: str, content: str):
        self.report_id = report_id
        self.report_type = report_type
        self.date_created = date_created
        self.content = content
    #returns list of report id's for indicated type. type=0 is summary, type=1 is predict
    @staticmethod
    def return_list_of_reports(type: int):
        """
        Returns a list of reports of given type
        """
        # Implementation for returning list of reports to admin
        getReports = ""
        if type == 0:
            #getReports = "SELECT * FROM summaryreport"
            getReports = "SELECT sreportid, workersid, monthoryear, summarydate, timeperiod FROM summaryreport"
        elif type == 1:
            getReports = "SELECT preportid FROM predictreports"
        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
        cursor.execute(getReports)
        listofstuff = cursor.fetchall()
        results = [{
                'sreportid': row[0],
                'workersid': row[1],
                'monthoryear': row[2],
                'summarydate': row[3],
                'timeperiod': row[4]
            } for row in listofstuff]
        cursor.close()
        del cursor
        return results
    #doctors can only view predict reports and only for patients assigned to them, this gives a list of reports a given doctor can access
    @staticmethod
    def return_list_of_reports_doctor(doctorid: int) -> list:
        getReports = """SELECT preportid FROM predictreports LEFT JOIN patient ON predictreports.healthid = patient.healthid
                    WHERE patient.doctorid = %d"""

        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
        cursor.execute(getReports, (doctorid,))
        listofstuff = cursor.fetchall()
        cursor.close()
        del cursor
        return listofstuff
    #This returns a list of tuples based on report ID and type. Each tuple is just the datas stored in the respective report entries table
    #Front-end will need to display the contents appropriately
    @staticmethod
    def return_report( type: int, reportID: int) -> list:
        """
        Returns a list of report entries based on type and reportID
        """
        # Implementation for returning reports, 0 is summary 1 is prediction
        getEntries = ""
        if type == 0:
            getEntries = "SELECT healthid, noofexams, abnormalexams FROM summaryreportentries WHERE sreportid = %s"
        elif type ==1:
            getEntries = "SELECT * FROM predictreportsentries WHERE preportid = %s"
        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
        cursor.execute(getEntries, (reportID,))
        listofstuff = cursor.fetchall()

        if type == 0:
                returnlist = [{
                'healthid': row[0],
                'noofexams': row[1],
                'abnormalexams': row[2]
            } for row in listofstuff]
        conn.commit()
        cursor.close()
        conn.close()
        return returnlist
    #Method to generate a prediction report. patient ID and year are needed as arguments.
    @staticmethod
    def generate_predict_report (self, patient: int, year: int):

        findTestTypes = """SELECT DISTINCT testypes FROM testresults LEFT JOIN testtypes ON testresults.testtype = testtypes.testtype
                            LEFT JOIN examtable ON testresults.examid = examtable.examid
                            WHERE examtable.healthid = %s AND NOT (testtypes.lowerbound < testresulsts.results < testtypes.upperbound) AND YEAR (testresults.resultdate) =%s"""
        getTestResults = """"SELECT results, upperbound, lowerbound FROM testresults LEFT JOIN examtable ON testresults.examid = examtable.examid
                             WHERE examtable.healthid = %s AND YEAR (testresults.resultdate) =%s ORDER BY testresults.resultdate DESC"""
        preMakeReportQry = "SELECT Auto_increment FROM information_schema.tables WHERE table_name='predictreports';"
        makeReportQry     = """INSERT into predictreports (workersid, healthid, pdate)
                            VALUES (%s, %s, %s);"""
        makeReportEntry = """INSERT INTO predictreportsentries (preportid, testtype, convernvalue) 
                            VALUES (%d, %s, %d)"""
        
        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
        cursor.execute (findTestTypes, (patient, year))
        testtypes = cursor.fetchall()
        entryList = []
        cursor.execute(preMakeReportQry)
        reportID: int
        result = cursor.fetchone()
        if result:
            reportID: int = result[0]
        
        #This is not checking if report exists, this is checking what id will be given to the new report
        cursor.execute(makeReportQry, (0, patient, date.today()))
        for value in testtypes:
            entry = PredictEntry(0, '0')
            multiplier = 1.0
            entry.concern = 100
            #won't this return the first letter of the string? Doesn't seem right but I'll leave it for now
            entry.type = value
            cursor.execute(getTestResults, (patient, year))
            results = cursor.fetchall()
            if len(results) == 1:
                continue
            if (results[0][0] < results[0][1] < results[0][2]):
                for row in results:
                    if not (row[0] < row[1] < row[2]):
                        entry.concern += round(25 * multiplier)
                    else:
                        entry.concern -= 25
                        multiplier = (multiplier / 2)
            elif not results[0][0] < results[0][1] < results[0][2]:
                x = 0
                for row in results:
                    if x == 0:
                        x += 1
                        continue
                    if not (row[0] < row[1] < row[2]):
                        entry.concern +- round(25 * multiplier)
                    else:
                        multiplier = multiplier/2
            entryList.append(entry)
        for obj in entryList:
            cursor.execute(makeReportEntry, (reportID, obj.type, obj.concern))
        conn.commit()
        cursor.close()
        conn.close()
    #method to generate a summary report. Year, month, and id of admin used as arguments.
    #For month, 0 means it is a yearly report.
    #Otherwise 1 indicates January, 2 February, and so on.
    @staticmethod
    def generate_summary_report(year: int, month: int, userID: int):
        """
        Generates a new report.
        """
         # Implementation for generating a report
        patientIDList: int = []
        patientTestList: int = []
        patientAbTestList: int = []
        today = datetime.date.today()

        db = DBService()
        conn = db.get_db_connection()

        cursor = conn.cursor()
       
        #query to get all patients
        patientQry = "SELECT HealthID FROM patient"
        # queries to count tests for patient within given timeframe.
        resultQryY = """SELECT COUNT(results) FROM testresults LEFT JOIN examtable ON testresults.examid = examtable.examid
                         WHERE examtable.healthID = %s AND DATE_PART('year', examtable.examdate) = %s"""
        resultQryM = """SELECT COUNT(results) FROM testresults WHERE healthID = %s AND MONTH(date) = %s AND YEAR (date) = %s"""
        # queries to count abnormal tests for patient within given timeframe
        countQryY2 = """SELECT COUNT(results) FROM testresults 
                        LEFT JOIN testtypes ON testresults.testtype = testtypes.testtype 
                        LEFT JOIN examtable ON testresults.examid = examtable.examid
                        WHERE examtable.healthid = %s AND DATE_PART ('year', examtable.examdate) = %s
                        AND NOT ((testtypes.lowerbound < testresults.results) AND (testresults.results < testtypes.upperbound ))"""
        
        countQryM2 = """SELECT COUNT(results)
                        FROM testresults 
                        LEFT JOIN testtypes ON testresults.testtype = testtypes.testtype 
                        LEFT JOIN examtable ON testresults.examid = examtable.examid
                        WHERE examtable.healthid =%s AND YEAR (testresults.resultdate) =%s AND MONTH(testresults.resultdate) =%s
                        AND NOT (testtypes.lowerbound < testresults.results < testtypes.upperbound )"""
        MakeReportQry     = """INSERT into summaryreport (sreportid, workersid, monthoryear, summarydate, timeperiod)
                            VALUES (%s, %s, %s, %s, %s);"""
        PreMakeReportQry = "        Select nextval(pg_get_serial_sequence('summaryreport', 'sreportid')) as new_id;"

        MakeReportEntryQry  = "INSERT INTO summaryreportentries (sreportid, healthid, noofexams, abnormalexams) VALUES(%s, %s, %s, %s);"
       
        if month == 0:
            mOrY = "year"
            timeperiod = f"{year}"
        else:
            mOrY = "month"
            timeperiod = f"{month}-{year}"

        #Fetch report number of new report, store it, then make report
        cursor.execute(PreMakeReportQry)
        reportID: int
        result = cursor.fetchone()
        if result:
            reportID: int = result[0]
        cursor.execute(MakeReportQry, (reportID, userID, mOrY, today, timeperiod))

        #Fetch all patients in Database, place in list
        cursor.execute(patientQry)
        results = cursor.fetchall()
        for row in results:
            patientIDList.append(row)
        # Count tests per patient, place count in separate list
        if month == 0:
             for val in patientIDList:
                 cursor.execute(resultQryY, (val, year))
                 count = cursor.fetchone
                 if count:
                    patientTestList.append(count)
        else:
            for val in patientIDList:
                 cursor.execute(resultQryM, (val, month, year))
                 count = cursor.fetchone
                 if count:
                     patientTestList.append(count)
        # Count unusual tests per patient, place in list
        if month == 0:
             for val in patientIDList:
                 cursor.execute(countQryY2, (val, year))
                 abcount = cursor.fetchone()
                 if abcount:
                     patientAbTestList.append(abcount)
        else:
            for val in patientIDList:
                 cursor.execute(countQryM2, (val, year, month))
                 abcount = cursor.fetchone()
                 if abcount:
                    patientAbTestList.append(abcount)
        #Now make individual report entries
        i = 0
        for val in patientIDList:
            testcount: int = patientTestList[i]
            abtestcount: int = patientAbTestList[i]
            value: int = val
            cursor.execute(MakeReportEntryQry, (reportID, value, 9, 9))
            i += 1
        conn.commit()
        cursor.close()
        conn.close()
        
    #Like before, delete report based on ID. type 0 = summary, type 1 = predict
    @staticmethod
    def remove_report(report_id: int, report_type: int):

        #deleteEnt = ''
        deleteRep = ''
        if report_type == 0:
            deleteRep = "DELETE FROM summaryreport WHERE sreportid = %s"
        elif report_type == 1:
            deleteRep = "DELETE FROM predictreports WHERE sreportid = %s"

        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute(deleteRep, (report_id,))
        conn.commit()
        cursor.close()
        conn.close()

      

# <><><><><><><><><><><><> EMAIL RELATED <><><><><><><><><><><><> 
    @staticmethod
    def send_report( receiver_email: str):
        # Email credentials and settings
        sender_email = "jlabs2519@gmail.com"  # Replace with your email
        receiver_email = "trashtesttoseestuff04@gmail.com"  # Replace with the receiver's email
        password = "uxnc zgiv vxwn moaa "  # Replace with your email password (or app-specific password)
        
        # Set up the SMTP server and port (for Gmail)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # Port for TLS
 
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Test Email from Jlabs"
        
        # Body of the email
        body = "Hello, this is a test message!"
        
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            # Connect to the Gmail SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Start TLS encryption
            server.login(sender_email, password)  # Log in with the sender's credentials
        
            # Send the email
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
        
            print("Email sent successfully!")
        
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            # Quit the SMTP server connection
            server.quit()

    @staticmethod
    def download_report(self):
        """
        Downloads the report.
        """
        # Implementation for downloading the report
        pass

