import sqlite3, bcrypt

DATABASE_NAME = 'test_files/test_database_copy/test.db'


# Singleton Class that is inherited by each UI Widget to ensure only one instance is generated
class SingletonClass(object):
	def __new__(cls):
		if not hasattr(cls, 'instance'):
			cls.instance = super(SingletonClass, cls).__new__(cls)
		return cls.instance


class DatabaseConnection(SingletonClass):

	def __init__(self):
		self._conn = sqlite3.connect(DATABASE_NAME)
		self._cursor = self.setCursor()
	
	def getConnection(self):
		return self._conn
	
	def setCursor(self):
		return self.getConnection().cursor()
	
	def getCursor(self):
		return self._cursor
	
	def closeConnection(self):
		self._conn.close()


def selectRowFromBenfId(benfId, dbCon):
	return dbCon.getCursor().execute(f'SELECT * FROM BENEFICIARY WHERE benfId=={benfId}').fetchall()


def returnRowNum(dbCon):
	return dbCon.getCursor().execute('SELECT COUNT(*) FROM BENEFICIARY').fetchall()[0][0]

def returnDataToVisualize(filterResult, dbCon):
	return dbCon.getCursor().execute(f'SELECT {filterResult}, COUNT(*) FROM BENEFICIARY GROUP BY {filterResult};').fetchall()

def returnOldPassword(dbCon):
	return dbCon.getCursor().execute("SELECT password FROM LOGIN_INFO").fetchone()

def returnOldUsername(dbCon):
	return dbCon.getCursor().execute("SELECT username FROM LOGIN_INFO").fetchone()

def updateUsernamePassword(username, passwordHash, result, dbCon):
	dbCon.getCursor().execute("UPDATE LOGIN_INFO SET username = ?, password = ? WHERE password = ?", (username, passwordHash, result))
	dbCon.getConnection().commit()



# Method that creates beneficiary.db database file with BENEFICIARY table
def create_table(dbCon):
	# dbCon.execute("DROP TABLE IF EXISTS BENEFICIARY")
	# dbCon.getCursor().execute("CREATE TABLE IF NOT EXISTS BENEFICIARY")

	defaultUsername = 'admin'
	defaultPassword = 'csibale123'
	defaultExportDir = ''

	createBenfTable = """
		CREATE TABLE IF NOT EXISTS BENEFICIARY (
		benfId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		benfFirstName VARCHAR(25),
		benfLastName VARCHAR(25),
		benfSuffix VARCHAR(25),
		benfAge INTEGER,
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
		benfNumFamMem INTEGER,
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

	# cur.execute(createBenfTable)
	# conn.commit()
	# conn.close()
	dbCon.getCursor().execute(createBenfTable)
	dbCon.getConnection().commit()
	dbCon.getCursor().execute(createLoginInfoTable)
	dbCon.getConnection().commit()
	dbCon.getCursor().execute(insertDefaults, [defaultUsername, passwordHashEncode(defaultPassword), defaultExportDir])
	dbCon.getConnection().commit()

# Helper function that inserts a row of data
def insert_row(dataToInsert, dbCon):
	inputs = [v for _,v in dataToInsert.items()]
	
	insert_command = """INSERT INTO BENEFICIARY (
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
		benfClosureReason) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

	dbCon.getCursor().execute(insert_command, inputs)
	dbCon.getConnection().commit()
	

# Helper function that updates a row of data
def update_row(dataToUpdate, dbCon):
	update_command = f"""UPDATE BENEFICIARY SET
		benfFirstName = \'{dataToUpdate['benfFirstName']}\',
		benfLastName = \'{dataToUpdate['benfLastName']}\',
		benfSuffix = \'{dataToUpdate['benfSuffix']}\',
		benfAge = \'{dataToUpdate['benfAge']}\',
		benfAgeGroup = \'{dataToUpdate['benfAgeGroup']}\',
		benfGender = \'{dataToUpdate['benfGender']}\',
		benfBirthdate = \'{dataToUpdate['benfBirthdate']}\',
		benfDisabilitySpec = \'{dataToUpdate['benfDisabilitySpec']}\',
		benfDisabilityDesc = \'{dataToUpdate['benfDisabilityDesc']}\',
		benfFatherName = \'{dataToUpdate['benfFatherName']}\',
		benfMotherName = \'{dataToUpdate['benfMotherName']}\',
		benfMunc = \'{dataToUpdate['benfMunc']}\',
		benfBrgy = \'{dataToUpdate['benfBrgy']}\',
		benfIP = \'{dataToUpdate['benfIP']}\',
		benfPhilhealth = \'{dataToUpdate['benfPhilhealth']}\',
		benfCCT = \'{dataToUpdate['benfCCT']}\',
		benfEducation = \'{dataToUpdate['benfEducation']}\',
		benfGradeLvl = \'{dataToUpdate['benfGradeLvl']}\',
		benfMedicine = \'{dataToUpdate['benfMedicine']}\',
		benfEmployed = \'{dataToUpdate['benfEmployed']}\',
		benfOccupation = \'{dataToUpdate['benfOccupation']}\',
		benfNumFamMem = \'{dataToUpdate['benfNumFamMem']}\',
		benfAdmissionDate = \'{dataToUpdate['benfAdmissionDate']}\',
		benfClosureDate = \'{dataToUpdate['benfClosureDate']}\',
		benfStatus = \'{dataToUpdate['benfStatus']}\',
		benfClosureReason = \'{dataToUpdate['benfClosureReason']}\' WHERE benfId={dataToUpdate['benfId']};
	"""

	dbCon.getCursor().execute(update_command)
	dbCon.getConnection().commit()
	


def remove_rows(itemIds, dbCon):

	for itemId in itemIds:
		command = f"""DELETE FROM BENEFICIARY WHERE benfId={itemId}"""
		dbCon.getCursor().execute(command)

	dbCon.getConnection().commit()

	

def search(searchString, searchFilter, dbCon):
	if searchFilter == 'muncBrgy':
		searchStringSplit = searchString.split(',')
		if len(searchStringSplit) == 2:
			searchStringMunc = searchStringSplit[0].replace(" ", "")
			searchStringBrgy = searchStringSplit[1].replace(" ", "")
			searchCommand = f"""SELECT * FROM BENEFICIARY WHERE LOWER(benfMunc)=LOWER(\"{searchStringMunc}\") AND LOWER(benfBrgy)=LOWER(\"{searchStringBrgy}\");"""
		else:
			return None, None, "Municipality and Barangay must be separated by comma (,)"
	else:
		searchCommand = f"""SELECT * FROM BENEFICIARY WHERE LOWER({searchFilter})=LOWER(\"{searchString}\");"""

	results = dbCon.getCursor().execute(searchCommand).fetchall()
	rowNum = len(results)
	return results, rowNum, ''


# Helper function that selects all data from BENEFICIARY table from beneficiary.fb
def selectAll(dbCon):
	results = dbCon.getCursor().execute("""SELECT * FROM BENEFICIARY;""")
	return results


def setExportDir(directoryName, dbCon):
	command = f"""UPDATE LOGIN_INFO SET export_dir=\'{directoryName}\';"""
	dbCon.getCursor().execute(command)
	dbCon.getConnection().commit()


def getExportDir(dbCon):
	command = f"""SELECT export_dir FROM LOGIN_INFO"""
	result = dbCon.getCursor().execute(command).fetchall()
	return result[0][0]


def getCardsValue(dbCon):
	commandNum = f"""SELECT COUNT(*) FROM BENEFICIARY;"""
	commandPhilhealthNum = f"""SELECT COUNT(*) FROM BENEFICIARY WHERE benfPhilhealth="Yes";"""
	commandCCTNum = f"""SELECT COUNT(*) FROM BENEFICIARY WHERE benfCCT="Yes";"""
	commands = [commandNum, commandPhilhealthNum, commandCCTNum]

	results = []
	
	for command in commands:
		cursorResult = dbCon.getCursor().execute(command).fetchall()[0][0]
		results.append(cursorResult)

	return results



# Method for password Hashing
def passwordHashEncode(password):
	bytes = password.encode('utf-8')
	salt = bcrypt.gensalt()
	passwordHash =  bcrypt.hashpw(bytes, salt)
	return passwordHash

# Method for hashed password decoding and matching
def passwordDecodeMatch(password, result):
	inputBytes = password.encode('utf-8')
	passwordMatching = bcrypt.checkpw(inputBytes, result)
	return passwordMatching



### Test driver codes - Commented out
# insert_row(benfFirstName = "FirstName2",
# benfLastName = "LastName2",
# benfSuffix = "Suffix1",
# benfAge = 25,
# benfGender = "Male",
# benfBirthdate = '01/25/1997',
# benfDisabilitySpec = "Epilepsy",
# benfDisabilityDesc = "Learning and behavioral problems.",
# benfFatherName = "FatherName1",
# benfMotherName = "MotherName2",
# benfMunc = "Sta. Fe",
# benfBrgy = "Poblacion",
# benfIP = "No",
# benfPhilhealth = "No",
# benfCCT = "Yes",
# benfEducation = "K-12 Curriculum",
# benfGradeLvl = 8,
# benfMedicine = "Yes",
# benfEmployed = "No",
# benfOccupation = "None",
# benfNumFamMem  = 5,
# benfAdmissionDate = '01/25/2020',
# benfClosureDate = '01/25/2021',
# benfStatus  = "Closed",
# benfClosureReason = "Already Employed")

# update_row(benfId = 1,
# benfFirstName = "FirstName2",
# benfLastName = "LastName2",
# benfSuffix = "Suffix1",
# benfAge = 25,
# benfGender = "Male",
# benfBirthdate = '01/25/1997',
# benfDisabilitySpec = "Epilepsy",
# benfDisabilityDesc = "Learning and behavioral problems.",
# benfFatherName = "FatherName1",
# benfMotherName = "MotherName2",
# benfMunc = "Sta. Fe",
# benfBrgy = "Poblacion",
# benfIP = "No",
# benfPhilhealth = "No",
# benfCCT = "Yes",
# benfEducation = "K-12 Curriculum",
# benfGradeLvl = 8,
# benfMedicine = "Yes",
# benfEmployed = "No",
# benfOccupation = "None",
# benfNumFamMem  = 5,
# benfAdmissionDate = '01/25/2020',
# benfClosureDate = '01/25/2021',
# benfStatus  = "Closed",
# benfClosureReason = "Already Employed")

# selectAll()
# create_table()
