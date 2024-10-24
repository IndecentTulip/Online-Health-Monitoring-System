-- Database: schema

-- DROP DATABASE IF EXISTS schema;

CREATE DATABASE schema
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_Canada.1252'
    LC_CTYPE = 'English_Canada.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
drop database schema;

	-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from users;
drop table users;

-- Create posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INT,
    title VARCHAR(255) NOT NULL,
    content VARCHAR(355) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
select * from posts;
drop table posts;

-- Create patients table
Create table Patient(
	healthID smallserial primary key,
	patientName varchar(50) not null,
	email varchar(50) not null,
	DOB date not null,
	status bool not null,
	doctorID serial not null,
	patientPassword varchar(50) not null,
	Foreign key (doctorID)references workers(workersID)
);
select * from Patient;
drop table Patient;

-- Create workers table
create table workers( 
	workersID serial primary key,
	workersName varchar(50) not null,
    email varchar(50) not null,
    phoneNumber numeric(10) not null, 
    image bytea,
    userType varchar(13) not null,
    staffPassword varchar(50) not null
);

select * from workers;
drop table workers;

create table ExamTable(
	examId serial primary key ,
    examDate date not null,
    healthID serial not null,
    workersID serial not null,
    examType varchar(50) not null,
    foreign key (healthID) references Patient(healthID),
    foreign key (workersID) references workers(workersID),
    foreign key (examType) references examType(examType)
);

select * from ExamTable;
drop table ExamTable;

create table examType(
examType varchar(50) primary key
);

select * from examType;
drop table examType;

create table testTypes(
	testType varchar(50) primary key,
    lowerBound numeric(3,1) not null,
    upperBound numeric(3,1) not null, 
    unit varchar(6) not null,
    examType varchar(50),
    foreign key (examType) references examType(examType)
);

select * from testTypes;
drop table testTypes;

create table testResults(
	testType varchar(50),
    foreign key (testType) references testTypes(testType),
    examId serial,
    foreign key (examID) references ExamTable(examId),
    results numeric(4, 4) not null,
    resultDate date not null
);

select * from testResults;
drop table testResults;

create table summaryReport(
	SReportID numeric(4) primary key,
	workersID serial not null,
    foreign key (workersID) references workers(workersID),
    monthOrYear VARCHAR(5) CHECK (monthOrYear IN ('Month','Year')) NOT NULL,
    summaryDate Date not null,
    timePeriod varchar(40)
);
	select * from summaryReport;
    drop table summaryReport;
    
create table summaryReportEntries(
	 SReportID numeric(4),
     foreign key (SReportID) references summaryReport(SReportID),
      healthID smallserial,
     foreign key(healthID) references Patient(healthID),
     noofExams numeric(2) not null,
     abnormalExams numeric(2) not null
	);
	select * from summaryReportEntries;
    drop table summaryReportEntries;
    
	create table predictReports(
    pReportID numeric(4) primary key not null,
    workersID serial not null,
    foreign key (workersID) references workers(workersID),
    healthID smallserial not null,
    foreign key (healthID) references Patient(healthID),
    pDate date not null
    );
    
    select * from predictReports;
    drop table predictReports;
    
    create table predictReportsEntries(
    pReportID numeric(4) primary key,
    foreign key(pReportID) references predictReports(pReportID),
    examType varchar(50) not null,
    foreign key(examType) references examType(examType),
    concernValue numeric(3) not null
    );
    
    select * from predictReportsEntries;
    drop table predictReportsEntries;
    
    create table smartMonitor(
		monitorID serial primary key not null,
        workersID serial not null,
        foreign key (workersID) references workers(workersID),
        examType varchar(50) default 'On Stand By' not null,
        foreign key (examType) references examType(examType),
        smartStatus  VARCHAR(5) CHECK (smartStatus IN ('sent','not sent')) NOT NULL,
        healthID smallserial not null,
        foreign key (healthID) references Patient(healthID)
    );
    
	select * from smartMonitor;
    drop table smartMonitor;