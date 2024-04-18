import sqlite3
import names
import string
import random
from datetime import date, timedelta
from PyQt5.QtCore import QDate
from dataListMapping import *
from backend import passwordHashEncode

def generateTestData(numRecords=100):
	defaultUsername = 'admin'
	defaultPassword = 'csibale123'
	defaultExportDir = ''

	dataList = DataListMapping()

	connection = sqlite3.connect('test.db')
	cursor = connection.cursor()

	cursor.execute("DROP TABLE IF EXISTS BENEFICIARY")
	connection.commit()

	createBenfTable = """
		CREATE TABLE IF NOT EXISTS BENEFICIARY (
		benfId INTEGER PRIMARY KEY,
		benfFirstName VARCHAR(25),
		benfLastName VARCHAR(25),
		benfSuffix VARCHAR(25),
		benfAge INT,
		benfAgeGroup VARCHAR(100),
		benfGender VARCHAR(25),
		benfBirthdate TIMESTAMP,
		benfDisabilitySpec VARCHAR(100),
		benfDisabilityDesc TEXT,
		benfFatherName VARCHAR(100),
		benfMotherName VARCHAR(100),
		benfMunc VARCHAR(25),
		benfBrgy VARCHAR(25),
		benfIP VARCHAR(5),
		benfPhilhealth VARCHAR(5),
		benfCCT VARCHAR(5),
		benfEducation VARCHAR(25),
		benfGradeLvl VARCHAR(5),
		benfMedicine VARCHAR(5),
		benfEmployed VARCHAR(5),
		benfOccupation VARCHAR(25),
		benfNumFamMem INT,
		benfAdmissionDate TIMESTAMP,
		benfClosureDate TIMESTAMP,
		benfStatus VARCHAR(25),
		benfClosureReason VARCHAR(100)
	);"""


	createLoginInfoTable = """
			CREATE TABLE IF NOT EXISTS LOGIN_INFO (
			username TEXT,
			password TEXT,
			export_dir TEXT

		);"""

	insertDefaults = """
		INSERT OR REPLACE INTO LOGIN_INFO (
		username,
		password,
		export_dir	
		) VALUES (?, ?, ?);
	"""

	cursor.execute(createBenfTable)
	connection.commit()
	cursor.execute(createLoginInfoTable)
	connection.commit()
	cursor.execute(insertDefaults, [defaultUsername, passwordHashEncode(defaultPassword), defaultExportDir])
	connection.commit()

	del dataList.getMuncBrgyMapping()['']
	statusList = dataList.getStatusList()[1:]
	gradeLvlList = dataList.getGradeLvlList()[1:]
	educationList = dataList.getEducationList()[1:]
	closureReasonList = dataList.getClosureReasonList()[1:]
	disSpecList = dataList.getDisabilitySpecList()[1:]
	genderList = dataList.getGenderList()[1:]
	yesOrNoList = dataList.getYesOrNoList()[1:]



	birthDateLowerBound, birthDateUpperBound = date(1950, 1, 1), date(2022, 1, 1)
	birthDateRange = [birthDateLowerBound]

	while birthDateLowerBound != birthDateUpperBound:
		birthDateLowerBound += timedelta(days=1)
		birthDateRange.append(birthDateLowerBound)


	admissionDateLowerBound, admissionDateUpperBound = random.choice(birthDateRange), date(2022, 1, 1)
	admissionDateRange = [admissionDateLowerBound]

	while admissionDateLowerBound != admissionDateUpperBound:
		admissionDateLowerBound += timedelta(days=1)
		admissionDateRange.append(admissionDateLowerBound)


	closureDateLowerBound, closureDateUpperBound = random.choice(admissionDateRange), date(2022, 1, 1)
	closureDateRange = [closureDateLowerBound]

	while closureDateLowerBound != closureDateUpperBound:
		closureDateLowerBound += timedelta(days=1)
		closureDateRange.append(closureDateLowerBound)


	for i in range(0, numRecords):
		munc = random.choice([k for k,_ in dataList.getMuncBrgyMapping().items()])
		brgy = random.choice([brgy for brgy in dataList.getMuncBrgyMapping()[munc]])


		birthDate = QDate.fromString(str(random.choices(birthDateRange, k=1)[0]), 'yyyy-MM-dd').toPyDate()
		age = int(abs(QDate.currentDate().daysTo(birthDate)/365))

		admissionDate = QDate.fromString(str(random.choices(admissionDateRange, k=1)[0]), 'yyyy-MM-dd').toPyDate()
		
		status = random.choice(statusList)
		if status == 'Ongoing':
			closureReason = ""
			closureDate = ""
		else:
			closureDate = QDate.fromString(str(random.choices(closureDateRange, k=1)[0]), 'yyyy-MM-dd').toPyDate()
			closureReason = random.choice(closureReasonList)

		if (age >=0) and (age<=5):
			ageGroup = '0-5 yrs old'
		elif (age >=6) and (age <=11):
			ageGroup = '6-11 yrs old'
		elif (age >=12) and (age <=17):
			ageGroup = '12-17 yrs old'
		elif (age >=18) and (age <=25):
			ageGroup = '18-25 yrs old'
		else:
			ageGroup = '26 and above'


		employment = random.choice(yesOrNoList)
		if employment == "No":
			occupation = ""
		else:
			occupation = random.choice(['', 'Teacher', 'Factory Worker', 'Cashier'])
		
		dataPayload = {
					'benfId' : i+1,
					'benfFirstName' : names.get_first_name(),
					'benfLastName' : names.get_last_name(),
					'benfSuffix' : random.choice(string.ascii_uppercase),
					'benfAge' : age,
					'benfAgeGroup' : ageGroup,
					'benfGender' : random.choice(genderList),
					'benfBirthdate' : birthDate,
					'benfDisabilitySpec' : random.choice(disSpecList),
					'benfDisabilityDesc' : random.choice(dataList.getDisabilitySpecList()),
					'benfFatherName' : names.get_full_name(),
					'benfMotherName' : names.get_full_name(),
					'benfMunc' : munc,
					'benfBrgy' : brgy,
					'benfIP' : random.choice(yesOrNoList),
					'benfPhilhealth' : random.choice(yesOrNoList),
					'benfCCT' : random.choice(yesOrNoList),
					'benfEducation' : random.choice(educationList),
					'benfGradeLvl' : random.choice(gradeLvlList),
					'benfMedicine' : random.choice(yesOrNoList),
					'benfEmployed' : employment,
					'benfOccupation' : occupation,
					'benfNumFamMem'  : random.randint(3, 10),
					'benfAdmissionDate' : admissionDate,
					'benfClosureDate' : closureDate,
					'benfStatus' : status,
					'benfClosureReason' : closureReason
				}
		
		inputs = [v for _,v in dataPayload.items()]
		
		insert_command = """INSERT INTO BENEFICIARY (
			benfId,
			benfFirstName,
			benfLastName,
			benfSuffix,
			benfAge,
			benfAgeGroup,
			benfGender,
			benfBirthdate,
			benfDisabilitySpec,
			benfDisabilityDesc,
			benfFatherName,
			benfMotherName,
			benfMunc,
			benfBrgy,
			benfIP,
			benfPhilhealth,
			benfCCT,
			benfEducation,
			benfGradeLvl,
			benfMedicine,
			benfEmployed,
			benfOccupation,
			benfNumFamMem,
			benfAdmissionDate,
			benfClosureDate,
			benfStatus,
			benfClosureReason) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
		
		cursor.execute(insert_command, inputs)
		connection.commit()

	connection.close()
	
	print(f"{numRecords} generated successfully.")


###########################################################################

numRecords = input("Enter the number of records: ")
generateTestData(numRecords=int(numRecords))