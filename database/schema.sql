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
alter table Patient add phoneNumber varchar(10);

--Patient table insert
INSERT INTO Patient (healthID, patientName, email, phoneNumber, DOB, status, doctorID, patientPassword) VALUES
(10031, 'Bob Ricky', 'Bobby13@hotmail.com', '1239654321', '1952-05-06', TRUE, 21002, '******a'),
(10032, 'Jenny Kim', 'Kim.jenn14@yahoo.com', '1235246352', '1999-12-20', FALSE, 21001, '******'),
(10033, 'Joe Gary', 'Jojo.g@outlook.com', '1236243846', '2000-10-18', TRUE, 21001, '******'),
(10034, 'Lisa John', 'Lisa_00@gamil.com', '1236243369', '2002-02-16', TRUE, 21002, '******'),
(10035, 'Barry Han', 'Han.barry50@icloud.com', '1230025282', '1978-08-11', FALSE, 21001, '******'),
(10036, 'Sean Curry', 'Seancurry_8@gamil.com', '1239452361', '2003-01-19', FALSE, 21003, '******'),
(10037, 'Bella Jay', 'Jay.jayb@hotmail.com', '1237779056', '2005-11-09', TRUE, 21001, '******');
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
--workers values to insert
INSERT INTO workers (workersID, workersName, email, phoneNumber, image, userType, staffPassword) VALUES
(21001, 'Molly Hue', 'Molly.Hue@jlabemail.com', '7893364852', NULL, 'Staff', '******'),
(21002, 'Karen Smith', 'Karen.Smith@jlabemail.com', '7895284465', NULL, 'Administrator', '******'),
(21003, 'Jayne Samer', 'Jayne.Samer@jlabemail.com', '7893217894', NULL, 'Staff', '***********'),
(21004, 'Lopez Dean', 'Lopez.Dean@jlabemail.com', '7890009000', NULL, 'Doctor', '*****'),
(21005, 'Derrick Juan', 'Derrick.Juan@jlabemail.com', '7899874356', NULL, 'Staff', '*****'),
(21006, 'Emily Zhang', 'Emily.Zhang@jlabemail.com', '7891760986', NULL, 'Staff', '*****'),
(21007, 'Shelly Birch', 'Shelly.Birch@jlabemail.com', '7899235981', NULL, 'Staff', '*****');

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
-- insert to ExamTable
INSERT INTO ExamTable (examId, examDate, healthID, workersID, examType) VALUES
(33025, '2024-10-18', 10031, 21004, 'Blood'),
(33026, '2024-08-01', 10031, 21001, 'ECG'),
(33027, '2023-11-02', 10032, 21004, 'Ultrasound'),
(33028, '2023-05-19', 10033, 21004, 'X-Ray'),
(33029, '2024-08-12', 10034, 21001, 'CT-Scan'),
(33030, '2023-03-26', 10035, 21004, 'MRI'),
(33031, '2024-02-09', 10036, 21004, 'Urine Test'),
(33032, '2024-10-10', 10037, 21003, 'Ultrasound');


select * from ExamTable;
drop table ExamTable;

create table examType(
examType varchar(50) primary key
);

--Insert values examType.
INSERT INTO examType(examType) values
('Blood'),
('ECG'),
('Ultrasound'),
('X-Ray'),
('CT-Scan'),
('MRI'),
('Urine Test');
select * from examType;
drop table examType;

create table testTypes(
	testType varchar(50) primary key,
    lowerBound numeric(4,1) not null,
    upperBound numeric(4,1) not null, 
    unit varchar(6) not null,
    examType varchar(50),
    foreign key (examType) references examType(examType)
);

--Insert values testType.
insert into testTypes(testType, lowerBound, upperBound, unit, examType) values
('Blood Test Iron', 0.5, 1.1, 'mg/dl', 'Blood'),
('Blood Test WCC', 100, 160, 'mg/dl', 'Blood'),
('Ultrasound D', 30, 140, 'U/L', 'Ultrasound'),
('X-Ray X', 7, 20, 'mmHG', 'X-Ray'),
('CT-Scan C', 90, 100, '%', 'CT-Scan'),
('MRI', 7, 55, 'U/L', 'MRI'),
('Urine Test', 11, 44, 'ng/mL', 'Urine Test'),
('Ultrasound', 7, 55, 'U/L', 'MRI');

select * from testTypes;
drop table testTypes;

create table testResults(
	testType varchar(50),
    foreign key (testType) references testTypes(testType),
    examId serial,
    foreign key (examId) references ExamTable(examId),
    results numeric(7, 4) not null,
    resultDate date not null
);
--insert test result values.
insert into testResults (testType, examId, results, resultDate) values 
('Blood Test Iron', 33025, 120, '2024-10-20'),
('Blood Test WCC', 33025, 12.1313, '2023-11-30'),
('MRI', 33027, 0.009, '2023-11-18'),
('Urine Test', 33028, 0.0005, '2023-05-22'), 
('Urine Test', 33029, 5.5, '2024-08-13');

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
	--inserts for summary report table
	insert into summaryReport (SReportID, workersID, monthOrYear, summaryDate, timePeriod) values
	(5508, 21002, 'Month', '2024-10-20', 'April 2024'),
	(5509, 21002, 'Month', '2023-11-30', 'March 2022'),
	(5510, 21002, 'Year', '2023-06-01', '2015'),
	(5511, 21002, 'Year', '2024-08-25', '2024'),
	(5512, 21003, 'Month', '2023-03-28', 'January 2024'),
	(5513, 21001, 'Year', '2024-02-28', '2023'), 
	(5514, 21002, 'Year', '2024-11-23', '2022');
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

	--insert values for summary report entries.
	insert into summaryReportEntries(SReportID, healthID, noofExams, abnormalExams) values
	(5508, 10031, 5, 5),
	(5509, 10032, 9, 5),
	(5510, 10033, 0, 0),
	(5511, 10034, 2, 1),
	(5512, 10035, 3, 0),
	(5513, 10036, 3, 3),
	(5514, 10037, 1, 1);
	
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

	--insert ino predict report values
	insert into predictReports(pReportID, workersID, healthID, pDate) values
	(5508, 21002, 10031, '2024-10-20'),
	(5509, 21003, 10032, '2023-11-30'),
	(5510, 21004, 10033, '2023-06-01'),
	(5511, 21005, 10034, '2024-08-25'),
	(5512, 21006, 10035, '2023-03-28'),
	(5513, 21001, 10036, '2024-02-28'),
	(5514, 21007, 10037, '2024-11-23');
    select * from predictReports;
    drop table predictReports;
    
    create table predictReportsEntries(
    pReportID numeric(4) primary key,
    foreign key(pReportID) references predictReports(pReportID),
    examType varchar(50) not null,
    foreign key(examType) references examType(examType),
    concernValue numeric(3) not null
    );
	
	--insert into predictReportEntries
    insert into predictReportsEntries(pReportID, examType, concernValue) values
	(5508, 'Blood', 100 ),
	(5509, 'Ultrasound', 150 ),
	(5510, 'Urine Test', 25),
	(5511, 'Urine Test', 200),
	(5512, 'Blood', 50),
	(5513, 'Ultrasound', 75),
	(5514, 'Blood', 120);
	
    select * from predictReportsEntries;
    drop table predictReportsEntries;
    
    create table smartMonitor(
		monitorID serial primary key not null,
        workersID serial not null,
        foreign key (workersID) references workers(workersID),
        examType varchar(50) default 'On Stand By' not null,
        foreign key (examType) references examType(examType),
        smartStatus  VARCHAR(10) CHECK (smartStatus IN ('sent','not sent')) NOT NULL,
        healthID smallserial not null,
        foreign key (healthID) references Patient(healthID)
    );

	INSERT INTO smartMonitor (monitorID, workersID, examType, smartStatus, healthID) VALUES
(60001, 21004, 'Blood', 'sent', 10031),
(60002, 21007, 'Urine Test', 'not sent', 10032),
(60003, 21004, 'CT-Scan', 'not sent', 10033),
(60004, 21004, 'CT-Scan', 'sent', 10034),
(60005, 21005, 'Blood', 'sent', 10035),
(60006, 21004, 'X-Ray', 'sent', 10036),
(60007, 21004, 'ECG', 'not sent', 10037),
(60008, 21003, 'MRI', 'not sent', 10031);
    
	select * from smartMonitor;
    drop table smartMonitor;