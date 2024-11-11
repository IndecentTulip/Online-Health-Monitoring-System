create table workers ( 
  workersid SERIAL primary key,
  workersname varchar(50) not null,
  email varchar(50) not null UNIQUE,
  phonenumber varchar(10) not null, 
  image bytea,
  usertype varchar(13) not null,
  staffpassword varchar(250) not null
);

create table examtype (
  examtype varchar(50) primary key
);

create table users (
  id SERIAL primary key,
  username varchar(50) not null unique,
  email varchar(100) not null unique,
  password varchar(255) not null,
  created_at timestamp default current_timestamp
);

create table patient (
  healthid SERIAL primary key,
  patientname varchar(50) not null,
  email varchar(50) not null UNIQUE,
  dob date not null,
  status boolean not null,
  doctorid int not null,
  patientpassword varchar(250) not null,
  phonenumber varchar(10),
  foreign key (doctorid) references workers(workersid) ON DELETE CASCADE ON UPDATE CASCADE
);

create table examtable (
  examid SERIAL primary key,
  examdate date not null,
  healthid int not null,
  workersid INT not null,
  examtype varchar(50) not null,
  notes varchar(300),
  foreign key (healthid) references patient(healthid) ON DELETE CASCADE ON UPDATE CASCADE,
  foreign key (workersid) references workers(workersid) ON DELETE CASCADE ON UPDATE CASCADE,
  foreign key (examtype) references examtype(examtype) ON DELETE CASCADE ON UPDATE CASCADE
);

create table testtypes (
  testtype varchar(50) primary key,
  lowerbound numeric(4, 1) not null,
  upperbound numeric(4, 1) not null, 
  unit varchar(6) not null,
  examtype varchar(50),
  foreign key (examtype) references examtype(examtype) ON DELETE CASCADE ON UPDATE CASCADE
);

create table presecribedTest (
  examId INT,
  foreign key (examid) references examtable(examid) ON DELETE CASCADE ON UPDATE CASCADE,
  testtype varchar(50),
  foreign key (testtype) references testtypes(testtype) ON DELETE CASCADE ON UPDATE CASCADE
);

create table testresults (
  testresultsid SERIAL primary key,
  testtype varchar(50),
  foreign key (testtype) references testtypes(testtype) ON DELETE CASCADE ON UPDATE CASCADE,
  examid INT,
  foreign key (examid) references examtable(examid) ON DELETE CASCADE ON UPDATE CASCADE,
  results numeric(7, 4) not null,
  resultdate date not null
);

create table summaryreport (
  sreportid SERIAL primary key,
  workersid INT not null,
  foreign key (workersid) references workers(workersid) ON DELETE CASCADE ON UPDATE CASCADE,
  monthoryear varchar(5) check (monthoryear in ('month', 'year')) not null,
  summarydate date not null,
  timeperiod varchar(40)
);

create table summaryreportentries (
  sreportid INT,
  foreign key (sreportid) references summaryreport(sreportid) ON DELETE CASCADE ON UPDATE CASCADE,
  healthid INT,
  foreign key (healthid) references patient(healthid) ON DELETE CASCADE ON UPDATE CASCADE,
  noofexams INT not null,
  abnormalexams INT not null
);

create table predictreports (
  preportid SERIAL primary key not null,
  workersid INT not null,
  foreign key (workersid) references workers(workersid) ON DELETE CASCADE ON UPDATE CASCADE,
  healthid INT not null,
  foreign key (healthid) references patient(healthid) ON DELETE CASCADE ON UPDATE CASCADE,
  pdate date not null
);

create table predictreportsentries (
  preportid INT primary key,
  foreign key (preportid) references predictreports(preportid) ON DELETE CASCADE ON UPDATE CASCADE,
  testtype varchar(50) not null,
  foreign key (testtype) references testtypes(testtype) ON DELETE CASCADE ON UPDATE CASCADE,
  concernvalue INT not null
);

create table smartmonitor (
  monitorid SERIAL primary key not null,
  workersid INT not null,
  foreign key (workersid) references workers(workersid) ON DELETE CASCADE ON UPDATE CASCADE,
  testtype varchar(50) default 'on stand by' not null,
  foreign key (testtype) references testtypes(testtype) ON DELETE CASCADE ON UPDATE CASCADE,
  smartstatus varchar(10) check (smartstatus in ('sent', 'not sent')) not null,
  healthid INT not null,
  foreign key (healthid) references patient(healthid) ON DELETE CASCADE ON UPDATE CASCADE
);

