
-- CREATE DATABASE jlabs
--   WITH
--   OWNER = postgres
--   ENCODING = 'UTF8'
--   LC_COLLATE = 'English_Canada.1252'
--   LC_CTYPE = 'English_Canada.1252'
--   LOCALE_PROVIDER = 'libc'
--   TABLESPACE = pg_default
--   CONNECTION LIMIT = -1
--   IS_TEMPLATE = False;

-- Drop if exists
DROP DATABASE IF EXISTS jlabs;

-- Create the database
CREATE DATABASE jlabs WITH ENCODING 'UTF8';

-- Connect to the new database
\c jlabs;

-- Create the workers table first since it is referenced in other tables
CREATE TABLE workers ( 
  workersID SERIAL PRIMARY KEY,
  workersName VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  phoneNumber VARCHAR(10) NOT NULL, 
  image BYTEA,
  userType VARCHAR(13) NOT NULL,
  staffPassword VARCHAR(50) NOT NULL
);

-- Create the examType table first since it is referenced in other tables
CREATE TABLE examType (
  examType VARCHAR(50) PRIMARY KEY
);

-- Create the users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the patient table
CREATE TABLE patient (
  healthID SMALLSERIAL PRIMARY KEY,
  patientName VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  DOB DATE NOT NULL,
  status BOOLEAN NOT NULL,
  doctorID INT NOT NULL,
  patientPassword VARCHAR(50) NOT NULL,
  phoneNumber VARCHAR(10),
  FOREIGN KEY (doctorID) REFERENCES workers(workersID)
);

-- Create the posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INT,
  title VARCHAR(255) NOT NULL,
  content VARCHAR(355) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the examTable
CREATE TABLE examTable (
  examId SERIAL PRIMARY KEY,
  examDate DATE NOT NULL,
  healthID SMALLINT NOT NULL,  -- Ensure this matches the patient table
  workersID SERIAL NOT NULL,
  examType VARCHAR(50) NOT NULL,
  FOREIGN KEY (healthID) REFERENCES patient(healthID),
  FOREIGN KEY (workersID) REFERENCES workers(workersID),
  FOREIGN KEY (examType) REFERENCES examType(examType)
);

-- Create the testTypes table
CREATE TABLE testTypes (
  testType VARCHAR(50) PRIMARY KEY,
  lowerBound NUMERIC(4, 1) NOT NULL,
  upperBound NUMERIC(4, 1) NOT NULL, 
  unit VARCHAR(6) NOT NULL,
  examType VARCHAR(50),
  FOREIGN KEY (examType) REFERENCES examType(examType)
);

-- Create the testResults table
CREATE TABLE testResults (
  testType VARCHAR(50),
  FOREIGN KEY (testType) REFERENCES testTypes(testType),
  examId SERIAL,
  FOREIGN KEY (examId) REFERENCES examTable(examId),
  results NUMERIC(7, 4) NOT NULL,
  resultDate DATE NOT NULL
);

-- Create the summaryReport table
CREATE TABLE summaryReport (
  SReportID NUMERIC(4) PRIMARY KEY,
  workersID SERIAL NOT NULL,
  FOREIGN KEY (workersID) REFERENCES workers(workersID),
  monthOrYear VARCHAR(5) CHECK (monthOrYear IN ('Month', 'Year')) NOT NULL,
  summaryDate DATE NOT NULL,
  timePeriod VARCHAR(40)
);

-- Create the summaryReportEntries table
CREATE TABLE summaryReportEntries (
  SReportID NUMERIC(4),
  FOREIGN KEY (SReportID) REFERENCES summaryReport(SReportID),
  healthID SMALLSERIAL,
  FOREIGN KEY (healthID) REFERENCES patient(healthID),
  noofExams NUMERIC(2) NOT NULL,
  abnormalExams NUMERIC(2) NOT NULL
);

-- Create the predictReports table
CREATE TABLE predictReports (
  pReportID NUMERIC(4) PRIMARY KEY NOT NULL,
  workersID SERIAL NOT NULL,
  FOREIGN KEY (workersID) REFERENCES workers(workersID),
  healthID SMALLSERIAL NOT NULL,
  FOREIGN KEY (healthID) REFERENCES patient(healthID),
  pDate DATE NOT NULL
);

-- Create the predictReportsEntries table
CREATE TABLE predictReportsEntries (
  pReportID NUMERIC(4) PRIMARY KEY,
  FOREIGN KEY (pReportID) REFERENCES predictReports(pReportID),
  examType VARCHAR(50) NOT NULL,
  FOREIGN KEY (examType) REFERENCES examType(examType),
  concernValue NUMERIC(3) NOT NULL
);

-- Create the smartMonitor table
CREATE TABLE smartMonitor (
  monitorID SERIAL PRIMARY KEY NOT NULL,
  workersID SERIAL NOT NULL,
  FOREIGN KEY (workersID) REFERENCES workers(workersID),
  examType VARCHAR(50) DEFAULT 'On Stand By' NOT NULL,
  FOREIGN KEY (examType) REFERENCES examType(examType),
  smartStatus VARCHAR(10) CHECK (smartStatus IN ('sent', 'not sent')) NOT NULL,
  healthID SMALLSERIAL NOT NULL,
  FOREIGN KEY (healthID) REFERENCES patient(healthID)
);

