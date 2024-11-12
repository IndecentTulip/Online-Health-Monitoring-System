
-- Ensure your tables are created with appropriate data types (e.g., changing examId to INTEGER if needed)

-- Insert into workers first
INSERT INTO workers (workersID, workersName, email, phoneNumber, image, userType, staffPassword) VALUES
  (21001, 'Molly Hue', 'Molly.Hue@jlabemail.com', '7893364852', NULL, 'Staff', '******'),
  (21002, 'Karen Smith', 'Karen.Smith@jlabemail.com', '7895284465', NULL, 'Administrator', '******'),
  (21003, 'Jayne Samer', 'Jayne.Samer@jlabemail.com', '7893217894', NULL, 'Staff', '***********'),
  (21004, 'Lopez Dean', 'Lopez.Dean@jlabemail.com', '7890009000', NULL, 'Doctor', '*****'),
  (21005, 'Derrick Juan', 'Derrick.Juan@jlabemail.com', '7899874356', NULL, 'Staff', '*****'),
  (21006, 'Emily Zhang', 'Emily.Zhang@jlabemail.com', '7891760986', NULL, 'Staff', '*****'),
  (21007, 'Shelly Birch', 'Shelly.Birch@jlabemail.com', '7899235981', NULL, 'Staff', '*****'),
  (21008, 'Totaly Read Doctor', 'Total.real@jlabemail.com', '7890009777', NULL, 'Doctor', '*****');

-- Insert into patients
INSERT INTO patient (healthID, patientName, email, phoneNumber, DOB, status, doctorID, patientPassword) VALUES
  (10031, 'Bob Ricky', 'Bobby13@hotmail.com', '1239654321', '1952-05-06', TRUE, 21004, '******a'),
  (10032, 'Jenny Kim', 'Kim.jenn14@yahoo.com', '1235246352', '1999-12-20', FALSE, 21008, '******'),
  (10033, 'Joe Gary', 'Jojo.g@outlook.com', '1236243846', '2000-10-18', TRUE, 21004, '******'),
  (10034, 'Lisa John', 'Lisa_00@gamil.com', '1236243369', '2002-02-16', TRUE, 21008, '******'),
  (10035, 'Barry Han', 'Han.barry50@icloud.com', '1230025282', '1978-08-11', FALSE, 21004, '******'),
  (10036, 'Sean Curry', 'Seancurry_8@gamil.com', '1239452361', '2003-01-19', FALSE, 21008, '******'),
  (10037, 'Bella Jay', 'Jay.jayb@hotmail.com', '1237779056', '2005-11-09', TRUE, 21004, '******');

-- Insert into examType first
INSERT INTO examType(examType) VALUES
  ('Blood'),
  ('ECG'),
  ('Ultrasound'),
  ('X-Ray'),
  ('CT-Scan'),
  ('MRI'),
  ('Urine Test');
  

-- Insert into examTable after examType
INSERT INTO examTable (examId, examDate, healthID, workersID, examType) VALUES
  (33025, '2024-10-18', 10031, 21004, 'Blood'),
  (33026, '2024-08-01', 10031, 21001, 'Blood'),
  (33027, '2023-11-02', 10032, 21004, 'Ultrasound'),
  (33028, '2023-05-19', 10033, 21004, 'CT-Scan'),
  (33029, '2024-08-12', 10034, 21001, 'Urine Test');

-- Insert into testTypes
INSERT INTO testTypes(testType, lowerBound, upperBound, unit, examType) VALUES
  ('Blood Test Iron', 0.5, 1.1, 'mg/dl', 'Blood'),
  ('Blood Test WCC', 100, 160, 'mg/dl', 'Blood'),
  ('Ultrasound', 30, 140, 'U/L', 'Ultrasound'),
  ('X-Ray', 7, 20, 'mmHG', 'X-Ray'),
  ('CT-Scan', 90, 100, '%', 'CT-Scan'),
  ('MRI', 7, 55, 'U/L', 'MRI'),
  ('Urine Test', 11, 44, 'ng/mL', 'Urine Test'),
  ('Routine Hematology', 0.9, 1.2, 'mg/dl', 'Blood'),
  ('Coagulation', 130, 180, 'mg/dl', 'Blood'),
  ('Routine Chemistry', 20, 60, 'mg/dl', 'Blood'),
  ('Renal Function', 30, 150, 'mg/dl', 'Blood'),
  ('Liver Function', 25, 90, 'mg/dl', 'Blood'),
  ('Pancreas Function', 50, 100, 'mg/dl', 'Blood'),
  ('Endocrinology', 90, 170, 'mg/dl', 'Blood'),
  ('Tumor Markers', 50, 100, 'mg/dl','Blood'),
  ('ECG', 10, 200, 'wh/dl', 'ECG');

-- Insert into prescribed test (Ensure these examIds exist in examTable)
INSERT INTO presecribedTest (examId, testtype) VALUES
  (33025, 'Blood Test Iron'),
  (33025, 'Blood Test WCC'),
  (33026, 'Blood Test Iron'),
  (33027, 'Ultrasound'),
  (33028, 'CT-Scan'),
  (33029, 'Urine Test');

INSERT INTO testresults (testresultsid, testtype, examid, results, resultdate) VALUES
 (1, 'Blood Test Iron', 33025, 4.0000, '2024-11-12');



-- Insert into summaryReport
INSERT INTO summaryReport (SReportID, workersID, monthOrYear, summaryDate, timePeriod) VALUES
  (5508, 21002, 'month', '2024-10-20', 'April 2024'),
  (5509, 21002, 'month', '2023-11-30', 'March 2022'),
  (5510, 21002, 'year', '2023-06-01', '2015'),
  (5511, 21002, 'year', '2024-08-25', '2024'),
  (5512, 21003, 'month', '2023-03-28', 'January 2024'),
  (5513, 21001, 'year', '2024-02-28', '2023'), 
  (5514, 21002, 'year', '2024-11-23', '2022');

-- Insert into summaryReportEntries
INSERT INTO summaryReportEntries(SReportID, healthID, noofExams, abnormalExams) VALUES
  (5508, 10031, 5, 5),
  (5509, 10032, 9, 5),
  (5510, 10033, 0, 0),
  (5511, 10034, 2, 1),
  (5512, 10035, 3, 0),
  (5513, 10036, 3, 3),
  (5514, 10037, 1, 1);

-- Insert into predictReports
INSERT INTO predictReports(pReportID, workersID, healthID, pDate) VALUES
  (5508, 21002, 10031, '2024-10-20'),
  (5509, 21003, 10032, '2023-11-30'),
  (5510, 21004, 10033, '2023-06-01'),
  (5511, 21005, 10034, '2024-08-25'),
  (5512, 21006, 10035, '2023-03-28'),
  (5513, 21001, 10036, '2024-02-28'),
  (5514, 21007, 10037, '2024-11-23');

-- Insert into predictReportsEntries
INSERT INTO predictReportsEntries(pReportID, testtype, concernValue) VALUES
  (5508, 'Blood Test Iron', 100),
  (5509, 'Ultrasound', 150),
  (5510, 'Urine Test', 25),
  (5511, 'Urine Test', 200),
  (5512, 'Blood Test Iron', 50),
  (5513, 'Ultrasound', 75),
  (5514, 'Blood Test Iron', 120);

-- Insert into smartMonitor
INSERT INTO smartMonitor (monitorID, workersID, testtype, smartStatus, healthID) VALUES
  (60001, 21004, 'Blood Test Iron', 'sent', 10031),
  (60002, 21007, 'Urine Test', 'not sent', 10032),
  (60003, 21004, 'CT-Scan', 'not sent', 10033),
  (60004, 21004, 'CT-Scan', 'sent', 10034),
  (60005, 21005, 'Blood Test Iron', 'sent', 10035),
  (60006, 21004, 'X-Ray', 'sent', 10036),
  (60007, 21004, 'ECG', 'not sent', 10037),
  (60008, 21003, 'MRI', 'not sent', 10031);

