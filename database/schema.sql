-- create the workers table first since it is referenced in other tables
create table workers ( 
  workersid SERIAL primary key,
  workersname varchar(50) not null,
  email varchar(50) not null UNIQUE,
  phonenumber varchar(10) not null, 
  image bytea,
  usertype varchar(13) not null,
  staffpassword varchar(50) not null
);

-- create the examtype table first since it is referenced in other tables
create table examtype (
  examtype varchar(50) primary key
);

-- create the users table
create table users (
  id SERIAL primary key,
  username varchar(50) not null unique,
  email varchar(100) not null unique,
  password varchar(255) not null,
  created_at timestamp default current_timestamp
);

-- create the patient table
create table patient (
  healthid SERIAL primary key,
  patientname varchar(50) not null,
  email varchar(50) not null UNIQUE,
  dob date not null,
  status boolean not null,
  doctorid int not null,
  patientpassword varchar(250) not null,
  phonenumber varchar(10),
  foreign key (doctorid) references workers(workersid)
);

-- create the posts table
create table posts (
  id SERIAL primary key,
  user_id int,
  title varchar(255) not null,
  content varchar(355) not null,
  created_at timestamp default current_timestamp,
  foreign key (user_id) references users(id)
);

-- Modify examTable definition to use SERIAL instead of INTEGER for examId
create table examtable (
  examid SERIAL primary key,  -- Changed to INTEGER
  examdate date not null,
  healthid int not null,  -- ensure this matches the patient table
  workersid INT not null,
  examtype varchar(50) not null,
  foreign key (healthid) references patient(healthid),
  foreign key (workersid) references workers(workersid),
  foreign key (examtype) references examtype(examtype)
);

-- create the testtypes table
create table testtypes (
  testtype varchar(50) primary key,
  lowerbound numeric(4, 1) not null,
  upperbound numeric(4, 1) not null, 
  unit varchar(6) not null,
  examtype varchar(50),
  foreign key (examtype) references examtype(examtype)
);

-- create the prescribed test.
create table presecribedTest(
  examId SERIAL,
  foreign key (examid) references examtable(examid),
  testtype varchar(50),
  foreign key (testtype) references testtypes(testtype)
);
-- create the testresults table
create table testresults (
  testtype varchar(50),
  foreign key (testtype) references testtypes(testtype),
  examid SERIAL,
  foreign key (examid) references examtable(examid),
  results numeric(7, 4) not null,
  resultdate date not null
);

-- create the summaryreport table
create table summaryreport (
  sreportid numeric(4) primary key,
  workersid SERIAL not null,
  foreign key (workersid) references workers(workersid),
  monthoryear varchar(5) check (monthoryear in ('month', 'year')) not null,
  summarydate date not null,
  timeperiod varchar(40)
);

-- create the summaryreportentries table
create table summaryreportentries (
  sreportid numeric(4),
  foreign key (sreportid) references summaryreport(sreportid),
  healthid SERIAL,
  foreign key (healthid) references patient(healthid),
  noofexams numeric(2) not null,
  abnormalexams numeric(2) not null
);

-- create the predictreports table
create table predictreports (
  preportid numeric(4) primary key not null,
  workersid SERIAL not null,
  foreign key (workersid) references workers(workersid),
  healthid SERIAL not null,
  foreign key (healthid) references patient(healthid),
  pdate date not null
);

-- create the predictreportsentries table
create table predictreportsentries (
  preportid numeric(4) primary key,
  foreign key (preportid) references predictreports(preportid),
  examtype varchar(50) not null,
  foreign key (examtype) references examtype(examtype),
  concernvalue numeric(3) not null
);

-- create the smartmonitor table
create table smartmonitor (
  monitorid SERIAL primary key not null,
  workersid SERIAL not null,
  foreign key (workersid) references workers(workersid),
  examtype varchar(50) default 'on stand by' not null,
  foreign key (examtype) references examtype(examtype),
  smartstatus varchar(10) check (smartstatus in ('sent', 'not sent')) not null,
  healthid SERIAL not null,
  foreign key (healthid) references patient(healthid)
);
