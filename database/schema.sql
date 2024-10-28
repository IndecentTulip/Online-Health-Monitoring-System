
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



-- Drop is already exists
DROP DATABASE IF EXISTS  jlabs;
-- Create the database
CREATE DATABASE jlabs WITH ENCODING 'UTF8';
-- Connect to the new database
\c jlabs

DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INT,
  title VARCHAR(255) NOT NULL,
  content VARCHAR(355) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

DROP TABLE IF EXISTS patient;

-- Create patients table
CREATE TABLE patient(
  healthID smallserial primary key,
  patientName varchar(50) not null,
  email varchar(50) not null,
  DOB date not null,
  status bool not null,
  doctorID serial not null,
  patientPassword varchar(50) not null,
  phoneNumber varchar(10);
  Foreign key (doctorID)references workers(workersID)
);

DROP TABLE IF EXISTS workers;

-- Create workers table
CREATE TABLE workers( 
  workersID serial primary key,
  workersName varchar(50) not null,
  email varchar(50) not null,
  phoneNumber numeric(10) not null, 
  image bytea,
  userType varchar(13) not null,
  staffPassword varchar(50) not null
);

DROP TABLE IF EXISTS examTable;

CREATE TABLE examTable(
  examId serial primary key ,
  examDate date not null,
  healthID serial not null,
  workersID serial not null,
  examType varchar(50) not null,
  foreign key (healthID) references Patient(healthID),
  foreign key (workersID) references workers(workersID),
  foreign key (examType) references examType(examType)
);

DROP TABLE IF EXISTS examType;

CREATE TABLE examType(
  examType varchar(50) primary key
);

DROP TABLE IF EXISTS testTypes;

CREATE TABLE testTypes(
  testType varchar(50) primary key,
  lowerBound numeric(4,1) not null,
  upperBound numeric(4,1) not null, 
  unit varchar(6) not null,
  examType varchar(50),
  foreign key (examType) references examType(examType)
);

DROP TABLE IF EXISTS testResults;

create table testResults(
  testType varchar(50),
  foreign key (testType) references testTypes(testType),
  examId serial,
  foreign key (examId) references ExamTable(examId),
  results numeric(7, 4) not null,
  resultDate date not null
);

DROP TABLE IF EXISTS summaryReport;

CREATE TABLE summaryReport(
  SReportID numeric(4) primary key,
  workersID serial not null,
  foreign key (workersID) references workers(workersID),
  monthOrYear VARCHAR(5) CHECK (monthOrYear IN ('Month','Year')) NOT NULL,
  summaryDate Date not null,
  timePeriod varchar(40)
);
    
DROP TABLE IF EXISTS summaryReportEntries;

CREATE TABLE summaryReportEntries(
  SReportID numeric(4),
  foreign key (SReportID) references summaryReport(SReportID),
  healthID smallserial,
  foreign key(healthID) references Patient(healthID),
  noofExams numeric(2) not null,
  abnormalExams numeric(2) not null
);

DROP TABLE IF EXISTS predictReports;
    
CREATE TABLE predictReports(
  pReportID numeric(4) primary key not null,
  workersID serial not null,
  foreign key (workersID) references workers(workersID),
  healthID smallserial not null,
  foreign key (healthID) references Patient(healthID),
  pDate date not null
);

DROP TABLE IF EXISTS predictReportsEntries;
    
CREATE TABLE predictReportsEntries(
  pReportID numeric(4) primary key,
  foreign key(pReportID) references predictReports(pReportID),
  examType varchar(50) not null,
  foreign key(examType) references examType(examType),
  concernValue numeric(3) not null
);

DROP TABLE IF EXISTS smartMonitor;

CREATE TABLE smartMonitor(
  monitorID serial primary key not null,
  workersID serial not null,
  foreign key (workersID) references workers(workersID),
  examType varchar(50) default 'On Stand By' not null,
  foreign key (examType) references examType(examType),
  smartStatus  VARCHAR(10) CHECK (smartStatus IN ('sent','not sent')) NOT NULL,
  healthID smallserial not null,
  foreign key (healthID) references Patient(healthID)
);
