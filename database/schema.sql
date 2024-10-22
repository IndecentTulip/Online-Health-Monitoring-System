-- Database: schema

-- DROP DATABASE IF EXISTS schema;

CREATE DATABASE jlabs;

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
	healthID int(5) primary key auto_increment,
	patientName varchar(50) not null,
	email varchar(50) not null,
	DOB date not null,
	status bool not null,
	doctorID int(5) not null,
	patientPassword varchar(50) not null,
	Foreign key (doctorID)references workers(workersID)
);
desc Patient;
drop table Patient;

-- Create workers table
create table workers( 
	workersID int(5) primary key auto_increment,
	workersName varchar(50) not null,
    email varchar(50) not null,
    phoneNumber int(10) not null, 
    image blob,
    userType varchar(13) not null,
    staffPassword varchar(50) not null
);

desc workers;
drop table workers;

create table ExamTable(
	examId int(5) primary key auto_increment,
    examDate date,
    healthID int(5),
    workersID int(5),
    examType varchar(50),
    foreign key (healthID) references Patient(healthID),
    foreign key (workersID) references workers(workersID),
    foreign key (examType) references examType(examType)
);

desc ExamTable;
drop table ExamTable;

create table examType(
examType varchar(50) primary key
);

desc examType;
drop table examType;

create table testTypes(
	testType varchar(50) primary key,
    lowerBound float(3,1) not null,
    upperBound float(3,1) not null, 
    unit varchar(6) not null,
    examType varchar(50),
    foreign key (examType) references examType(examType)
);

desc table testTypes;
drop table testTypes;

create table testResults(
	testType varchar(50),
    foreign key (testType) references testTypes(testType),
    examId int(5),
    foreign key (examID) references ExamTable(examId),
    results float(4, 4) not null,
    resultDate date not null
);

desc table testResults;
drop table testResults;

create table summaryReport(
	SReportID int(4) primary key auto_increment,
	workersID int(5),
    foreign key (workersID) references workers(workersID),
    monthOrYear enum ('Month','Year') not null,
    summaryDate Date not null,
    timePeriod varchar(40)
);
	desc summaryReport;
    drop table summaryReport;
    
create table summaryReportEntries(
	 SReportID int(4),
     foreign key (SReportID) references summaryReport(SReportID),
     healthID int(5),
     foreign key(healthID) references Patient(healthID),
     noofExams int(2) not null,
     abnormalExams int(2) not null
);
	desc summaryReportEntries;
    drop table summaryReportEntries;
    
	create table predictReports(
    pReportID int(4) primary key auto_increment not null,
    workersID int(5)not null,
    foreign key (workersID) references workers(workersID),
    healthID int(5) not null,
    foreign key (healthID) references Patient(healthID),
    pDate date not null
    );
    
    desc predictReports;
    drop table predictReports;
    
    create table predictReportsEntries(
    pReportID int(4) not null,
    foreign key(pReportID) references predictReports(pReportID),
    examType varchar(50) not null,
    foreign key(examType) references examType(examType),
    concernValue int(3) not null
    );
    
    desc predictReportsEntries;
    drop table predictReportsEntries;
    
    create table smartMonitor(
		monitorID int(5) primary key auto_increment not null,
        workersID int(5) not null,
        foreign key (workersID) references workers(workersID),
        examType varchar(50) default 'On Stand By' not null,
        foreign key (examType) references examType(examType),
        smartStatus enum ('sent', 'not sent') not null,
        healthID int(5) not null,
        foreign key (healthID) references Patient(healthID)
    );
    
	desc smartMonitor;
    drop table smartMonitor;