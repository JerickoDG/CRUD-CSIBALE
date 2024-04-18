import re
from backend import *

from dataListMapping import DataListMapping

from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt5.QtCore import QDate
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

# from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries

from resources.updateDataWidgetUi import Ui_Form as UpdateFormUi


dataListMap = DataListMapping()
dbInstance = DatabaseConnection()
dbInstance.setCursor()

# Update Form Window for modifying beneficiary data 
class UpdateForm(QWidget, UpdateFormUi, SingletonClass):

	def __init__(self, results, mainWindowInstance):
		super(UpdateForm, self).__init__()
		self.setupUi(self)
		self.results = results
		self.mainWindowInstance = mainWindowInstance

		self.setWindowIcon(QIcon('./csibale.png'))
		self.setWindowTitle('Update Beneficiary Data')

		# Setting the options for Dropdown QComboBoxes
		for k,v in dataListMap.getMuncBrgyMapping().items():
			self.muncLine.addItem(k, v)
			self.muncLine.currentIndexChanged.connect(self.updateBrgyCombo)
			self.updateBrgyCombo(self.muncLine.currentIndex())
	
		self.disSpecLine.addItems(dataListMap.getDisabilitySpecList())
		self.genderLine.addItems(dataListMap.getGenderList())
		self.ipLine.addItems(dataListMap.getYesOrNoList())
		self.philhealthLine.addItems(dataListMap.getYesOrNoList())
		self.cctLine.addItems(dataListMap.getYesOrNoList())
		self.medicineLine.addItems(dataListMap.getYesOrNoList())
		self.employedLine.addItems(dataListMap.getYesOrNoList())
		self.statusLine.addItems(dataListMap.getStatusList())
		self.reasonClosureLine.addItems(dataListMap.getClosureReasonList())
		self.educationLine.addItems(dataListMap.getEducationList())
		self.gradeLvlLine.addItems(dataListMap.getGradeLvlList())


		# Setting the current value of each field as the presented value
		self.idLine.setText(str(results[0][0]))
		self.firstNameLine.setText(results[0][1])
		self.lastNameLine.setText(results[0][2])
		self.suffixLine.setText(results[0][3])
		self.ageLine.setText(str(results[0][4]))
		self.ageGroupLine.setText(str(results[0][5]))
		self.genderLine.setCurrentText(results[0][6])
		birthDateSplit = results[0][7].split('-')
		birthDate = QDate(int(birthDateSplit[0]), int(birthDateSplit[1]), int(birthDateSplit[2]))
		self.birthDateLine.setDate(birthDate)
		self.disSpecLine.setCurrentText(results[0][8])
		self.disDescLine.setText(results[0][9])
		self.fatherNameLine.setText(results[0][10])
		self.motherNameLine.setText(results[0][11])
		self.muncLine.setCurrentText(results[0][12])
		self.brgyLine.setCurrentText(results[0][13])
		self.ipLine.setCurrentText(results[0][14])
		self.philhealthLine.setCurrentText(results[0][15])
		self.cctLine.setCurrentText(results[0][16])
		self.educationLine.setCurrentText(results[0][17])
		self.gradeLvlLine.setCurrentText(results[0][18])
		self.medicineLine.setCurrentText(results[0][19])
		self.employedLine.setCurrentText(results[0][20])
		self.occupationLine.setText(results[0][21])
		self.numFamLine.setText(str(results[0][22]))
		admissionDateSplit = results[0][23].split('-')
		admissionDate = QDate(int(admissionDateSplit[0]), int(admissionDateSplit[1]), int(admissionDateSplit[2]))
		self.admissionDateLine.setDate(admissionDate)
		if results[0][24] != "":
			closureDateSplit = results[0][24].split('-')
			closureDate = QDate(int(closureDateSplit[0]), int(closureDateSplit[1]), int(closureDateSplit[2]))
			self.closureDateLine.setDate(closureDate)
		self.statusLine.setCurrentText(results[0][25])
		self.reasonClosureLine.setCurrentText(results[0][26])

		self.ageLine.textChanged.connect(self.autoFillAgeGroup)
		self.confirmModifyBtn.clicked.connect(self.updateBeneficiaryData)


		if (self.educationLine.currentText() == "") or (self.educationLine.currentText() == "Daycare"):
			self.gradeLvlLine.setCurrentIndex(0)
			self.gradeLvlLine.setEnabled(False)


		if (self.employedLine.currentText() == "No") or (self.employedLine.currentText() == ""):
			self.occupationLine.setText("")
			self.occupationLine.setEnabled(False)

		if self.statusLine.currentText() == "Ongoing":
			self.reasonClosureLine.setEnabled(False)
			self.closureDateLine.setEnabled(False)
			# self.closureDateLine.setMinimumDate(QDate(1900,1,1))
			# self.closureDateLine.setSpecialValueText(" ")
			self.reasonClosureLine.setCurrentIndex(0)
		

		self.educationLine.currentIndexChanged.connect(self.detectChangeEducationLine)
		self.employedLine.currentIndexChanged.connect(self.detectChangeEmployedLine)
		self.statusLine.currentIndexChanged.connect(self.detectChangeClosureLines)
		self.birthDateLine.dateChanged.connect(self.ageCalculation)
		
		self.admissionDateLine.setDateRange(self.birthDateLine.date(), QDate.currentDate())
		self.closureDateLine.setDateRange(self.admissionDateLine.date(), QDate.currentDate())
		self.birthDateLine.dateChanged.connect(lambda: self.admissionDateLine.setDateRange(self.birthDateLine.date(), QDate.currentDate()))
		self.admissionDateLine.dateChanged.connect(lambda: self.closureDateLine.setDateRange(self.admissionDateLine.date(), QDate.currentDate()))
		self.ageCalculation()

	def ageCalculation(self):
		# if self.ageLine.text() != "":
		correctAge = int(abs(QDate.currentDate().daysTo(self.birthDateLine.date())/365))
			# if self.ageLine.text() != str(correctAge):
				# msg = QMessageBox()
				# msg.setIcon(QMessageBox.Information)
				# msg.setText(f"Age will be set to {str(correctAge)}")
				# msg.setDetailedText(f"Set birthdate ({str(self.birthDateLine.date().toPyDate())}) and set age ({self.ageLine.text()}) does not match.")
				# msg.setWindowTitle("Information - Age Correction")
				# msg.exec_()
		self.ageLine.setText(str(correctAge))
		QApplication.processEvents()
	

	def detectChangeEducationLine(self):
		if (self.educationLine.currentText() == "") or (self.educationLine.currentText() == "Daycare"):
			self.gradeLvlLine.setCurrentIndex(0)
			self.gradeLvlLine.setEnabled(False)
		else:
			self.gradeLvlLine.setEnabled(True)

	
	def detectChangeEmployedLine(self):
		if (self.employedLine.currentText() == "No") or (self.employedLine.currentText() == ""):
			self.occupationLine.setText("")
			self.occupationLine.setEnabled(False)
		else:
			self.occupationLine.setEnabled(True)

	
	def detectChangeClosureLines(self):
		if (self.statusLine.currentText() == "Ongoing") or (self.statusLine.currentText() == ""):
			self.reasonClosureLine.setEnabled(False)
			self.closureDateLine.setEnabled(False)
			# self.closureDateLine.clear()
			# self.closureDateLine.setMinimumDate(QDate(2000,1,1))
			# self.closureDateLine.setSpecialValueText(" ")
			self.reasonClosureLine.setCurrentIndex(0)
		else:
			self.reasonClosureLine.setEnabled(True)
			self.closureDateLine.setEnabled(True)
			

	# Method that updates the selected beneficiary data
	def updateBeneficiaryData(self):
		validateInputResult = self.validateInputs()

		# If fields are incomplete and there are fields requiring numeric values
		if ((validateInputResult[0]) or (validateInputResult[1]) or (validateInputResult[2])):
			self.msg = QMessageBox()
			text = ""
			if validateInputResult[0]:
				text += "Data Incomplete\n"
			if validateInputResult[1]:
				text += "Some fields are required to be a number\n"
			if validateInputResult[2]:
				text += "Some fields does not allow numbers in the input\n"
			self.msg.setText(text)
			self.msg.setWindowTitle("Error - Input of the fields")
			self.msg.setIcon(QMessageBox.Critical)
			self.msg.setWindowIcon(QIcon('Error'))
			self.msg.exec()
		else:
			intCastedAge = int(self.ageLine.text())
			if (intCastedAge >=0) and (intCastedAge <=5):
				benfAgeGroup = '0-5 yrs old'
			elif (intCastedAge >=6) and (intCastedAge <=11):
				benfAgeGroup = '6-11 yrs old'
			elif (intCastedAge >=12) and (intCastedAge <=17):
				benfAgeGroup = '12-17 yrs old'
			elif (intCastedAge >=18) and (intCastedAge <=25):
				benfAgeGroup = '18-25 yrs old'
			else:
				benfAgeGroup = '26 and above'
				  
			# update_row(benfId = int(self.idLine.text()),
			# 	benfFirstName = self.firstNameLine.text(),
			# 	benfLastName = self.lastNameLine.text(),
			# 	benfSuffix = self.suffixLine.text(),
			# 	benfAge = intCastedAge,
			# 	benfAgeGroup = benfAgeGroup,
			# 	benfGender = self.genderLine.currentText(),
			# 	benfBirthdate = self.birthDateLine.date().toPyDate(),
			# 	benfDisabilitySpec = self.disSpecLine.currentText(),
			# 	benfDisabilityDesc = self.disDescLine.text(),
			# 	benfFatherName = self.fatherNameLine.text(),
			# 	benfMotherName = self.motherNameLine.text(),
			# 	benfMunc = self.muncLine.currentText(),
			# 	benfBrgy = self.brgyLine.currentText(),
			# 	benfIP = self.ipLine.currentText(),
			# 	benfPhilhealth = self.philhealthLine.currentText(),
			# 	benfCCT = self.cctLine.currentText(),
			# 	benfEducation = self.educationLine.currentText(),
			# 	benfGradeLvl = self.gradeLvlLine.currentText(),
			# 	benfMedicine = self.medicineLine.currentText(),
			# 	benfEmployed = self.employedLine.currentText(),
			# 	benfOccupation = self.occupationLine.text(),
			# 	benfNumFamMem  = int(self.numFamLine.text()),
			# 	benfAdmissionDate = self.admissionDateLine.date().toPyDate(),
			# 	benfClosureDate = self.closureDateLine.date().toPyDate(),
			# 	benfStatus  = self.statusLine.currentText(),
			# 	benfClosureReason = self.reasonClosureLine.currentText())

			self.birthDateLine.dateChanged.connect(self.ageCalculation)

			if self.statusLine.currentText() == "Ongoing":
				closureDateToStore = ""
			else:
				closureDateToStore = self.closureDateLine.date().toPyDate()
			
			dataPayload = {
				'benfId': self.idLine.text(), 
				'benfFirstName' : self.firstNameLine.text().title(),
				'benfLastName' : self.lastNameLine.text().title(),
				'benfSuffix' : self.suffixLine.text().title(),
				'benfAge' : intCastedAge,
				'benfAgeGroup' : benfAgeGroup,
				'benfGender' : self.genderLine.currentText(),
				'benfBirthdate' : self.birthDateLine.date().toPyDate(),
				'benfDisabilitySpec' : self.disSpecLine.currentText(),
				'benfDisabilityDesc' : self.disDescLine.text(),
				'benfFatherName' : self.fatherNameLine.text().title(),
				'benfMotherName' : self.motherNameLine.text().title(),
				'benfMunc' : self.muncLine.currentText(),
				'benfBrgy' : self.brgyLine.currentText(),
				'benfIP' : self.ipLine.currentText(),
				'benfPhilhealth' : self.philhealthLine.currentText(),
				'benfCCT' : self.cctLine.currentText(),
				'benfEducation' : self.educationLine.currentText(),
				'benfGradeLvl' : self.gradeLvlLine.currentText(),
				'benfMedicine' : self.medicineLine.currentText(),
				'benfEmployed' : self.employedLine.currentText(),
				'benfOccupation' : self.occupationLine.text().title(),
				'benfNumFamMem'  : int(self.numFamLine.text()),
				'benfAdmissionDate' : self.admissionDateLine.date().toPyDate(),
				'benfClosureDate' : closureDateToStore,
				'benfStatus' : self.statusLine.currentText(),
				'benfClosureReason' : self.reasonClosureLine.currentText()
			}

			update_row(dataToUpdate=dataPayload, dbCon=dbInstance)

			# Refresh the contents of the QTableWidget from the Main Window
			self.ageGroupLine.setText(benfAgeGroup)
			self.mainWindowInstance.searchBeneficiaryData()

			self.msg = QMessageBox()
			self.msg.setWindowTitle("Success - Update Beneficiary")
			self.msg.setText("Beneficiary Data was successfully updated!")
			self.msg.setIcon(QMessageBox.Information)
			self.msg.exec()


	# Helper method for validating input data
	def validateInputs(self):

		isEmpty = False
		nonIntError = False
		nonAlphaError = False

		fieldsMustNotBeEmpty = [
			self.firstNameLine,
			self.lastNameLine,
			self.ageLine,
			self.genderLine,
			self.birthDateLine,
			self.disSpecLine,
			# self.disDescLine,
			# self.fatherNameLine,
			# self.motherNameLine,
			self.muncLine,
			self.brgyLine,
			self.ipLine,
			self.philhealthLine,
			self.cctLine,
			# self.educationLine,
			# self.gradeLvlLine,
			self.medicineLine,
			self.employedLine,
			# self.occupationLine,
			self.numFamLine,
			self.admissionDateLine,
			self.statusLine
		]


		fieldsMustBeInt = [
			self.ageLine,
			self.numFamLine
		]

		fieldsMustBeAlpha = [
			self.firstNameLine,
			self.lastNameLine,
			self.suffixLine,
			self.fatherNameLine,
			self.motherNameLine
		]


		if self.statusLine.currentText() != "Ongoing":
			fieldsMustNotBeEmpty.extend((self.closureDateLine, self.reasonClosureLine))
		else:
			if (self.closureDateLine in fieldsMustNotBeEmpty) and (self.reasonClosureLine in fieldsMustNotBeEmpty):
				fieldsMustNotBeEmpty.remove(self.closureDateLine)
				fieldsMustNotBeEmpty.remove(self.reasonClosureLine)
		
		
		if self.employedLine.currentText() == "Yes":
			fieldsMustNotBeEmpty.append(self.occupationLine)
		else:
			if self.occupationLine in fieldsMustNotBeEmpty:
				fieldsMustNotBeEmpty.remove(self.occupationLine)
		
		
		for field in fieldsMustBeInt:
			if isinstance(field, QtWidgets.QLineEdit):
				if not(field.text().isnumeric()):
					# emptyFieldsList.append(field.objectName()) # adds the field to emptyFieldsList
					field.setText("")
					field.setPlaceholderText("Must be a number")
					nonIntError = True
		
		for field in fieldsMustBeAlpha:
			if isinstance(field, QtWidgets.QLineEdit):
				# if not(field.text().isalpha() ):
				# if not re.match(regex_names, field.text()):
				# if (field.text().isdigit()):
				if any(char.isdigit() for char in field.text()):
					# emptyFieldsList.append(field.objectName()) # adds the field to emptyFieldsList
					field.setText("")
					field.setPlaceholderText("Must not contain a number")
					nonAlphaError = True
		
		for field in fieldsMustNotBeEmpty:
			if isinstance(field, QtWidgets.QLineEdit):
				if field.text() == '':
					# emptyFieldsList.append(field.objectName()) # adds the field to emptyFieldsList
					# print(f'{field} is empty!')
					# field.setText("")
					field.setPlaceholderText("Required")
					isEmpty = True
			elif isinstance(field, QtWidgets.QComboBox):
				if field.currentText() == '':
					#emptyFieldsList.append(field.objectName()) # adds the field to emptyFieldsList
					field.setPlaceholderText("Required")
					isEmpty = True
			elif isinstance(field, QtWidgets.QDateEdit):
				if str(field.date().toPyDate()) == '':
					#emptyFieldsList.append(field.objectName()) # adds the field to emptyFieldsList
					isEmpty = True
		
		return (isEmpty, nonIntError, nonAlphaError)
		


	# Helper method that updates the content of QComboBox of Barangay depending on the selected Municipality
	def updateBrgyCombo(self, index):
		self.brgyLine.clear()
		brgys = self.muncLine.itemData(index)
		if brgys:
			self.brgyLine.addItems(brgys)
	
	def autoFillAgeGroup(self):
		regex = '^[0-9]+$'

		if re.match(regex, self.ageLine.text()): 
			intCastedAge = int(self.ageLine.text())

			if (intCastedAge >=0) and (intCastedAge <=5):
				benfAgeGroup = '0-5 yrs old'
			elif (intCastedAge >=6) and (intCastedAge <=11):
				benfAgeGroup = '6-11 yrs old'
			elif (intCastedAge >=12) and (intCastedAge <=17):
				benfAgeGroup = '12-17 yrs old'
			elif (intCastedAge >=18) and (intCastedAge <=25):
				benfAgeGroup = '18-25 yrs old'
			else:
				benfAgeGroup = '26 and above'
			
			self.ageGroupLine.setText(benfAgeGroup)
			
		else:
			self.ageGroupLine.setText('')