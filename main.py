import sys, os, xlsxwriter, re
from backend import *
from datetime import datetime
from dataListMapping import DataListMapping

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QSystemTrayIcon, QMenu
from PyQt5.QtCore import QPropertyAnimation, QDate, QObject
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon

from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries

from resources.mainUi import Ui_MainWindow
from updateForm import UpdateForm
from helpPageWindow import HelpForm


dataListMap = DataListMapping()
dbInstance = DatabaseConnection()
dbInstance.setCursor()

class TableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return super().__lt__(other)
		

# Main Window of the Application
class MainWindow(SingletonClass, QMainWindow, Ui_MainWindow):

	def __init__(self):	
		super(MainWindow, self).__init__()
		create_table(dbCon=dbInstance)
		self.setupUi(self)
		self.initUI()
	
	# Window Icon
		self.setWindowIcon(QIcon('./resources/main_img_resources/csibale.png'))
		self.setWindowTitle('CSIBALE - Data Storage')

		

	def initUI(self):
		self.tableResults = selectAll(dbCon=dbInstance).fetchall()
		self.chartContent = None
		self.summary = ''
		self.rowNum = -1
		self.allCheckedFlag = False
		self.loadData()

		#Initialize higlight on Home button
		self.pushButton.setStyleSheet("padding: 5px; text-align: left; border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; hover; background-color : #f0faef")
		self.cardValues = getCardsValue(dbCon=dbInstance)

		self.totalNumLabel.setText(str(self.cardValues[0]))
		self.philHealthNumLabel.setText(str(self.cardValues[1]))
		self.cctNumLabel.setText(str(self.cardValues[2]))

		self.searchStringLine.textChanged.connect(self.searchBeneficiaryData)

		self.searchFilterLine.addItems([v for _,v in dataListMap.getColNameDbMapping().items()])
		
		self.searchFilterLine.currentTextChanged.connect(self.searchFilterLineChange)

		self.sortByLine.addItems([v for _,v in dataListMap.getColNameDbMapping().items()])
		
		self.menuBtn.clicked.connect(lambda: self.slideLeftMenu())
		self.menuBtn2.clicked.connect(lambda: self.slideLeftMenu())
		self.menuBtn3.clicked.connect(lambda: self.slideLeftMenu())
		self.menuBtn4.clicked.connect(lambda: self.slideLeftMenu())


		#For Help button
		self.pushButton_10.clicked.connect(self.displayHelpPage)
	
		self.pushButton_2.clicked.connect(self.showUserSettingsWidget)
		self.pushButton.clicked.connect(self.showHomeWidget)
		self.goBackHomeBtn.clicked.connect(self.showHomeWidget)
		self.chooseFileBtn.clicked.connect(self.chooseDirectoryLocation)
		self.addBtn.clicked.connect(self.goToAddBeneficiaryWidget)
		self.confirmAddBtn.clicked.connect(self.insertBeneficiaryData)
		self.confirmAddBtn.clicked.connect(self.ageCalculation)
		self.deleteBtn.clicked.connect(self.removeBeneficiaryData)
		self.searchBtn.clicked.connect(self.searchBeneficiaryData)
		self.searchFilterLine.currentIndexChanged.connect(self.searchBeneficiaryData)

		self.pushButton.setCheckable(True)
		self.pushButton_2.setCheckable(True)
		self.pushButton_3.setCheckable(True)
		self.pushButton_4.setCheckable(True)
		self.pushButton.clicked.connect(self.togglePushButton)
		self.pushButton_2.clicked.connect(self.togglePushButton_2)
		self.pushButton_3.clicked.connect(self.togglePushButton_3)
		self.pushButton_4.clicked.connect(self.togglePushButton_4)

		self.sortAscendingBtn.setCheckable(True)
		self.sortDescendingBtn.setCheckable(True)
		self.sortAscendingBtn.clicked.connect(self.toggleSortAscendingButton)
		self.sortDescendingBtn.clicked.connect(self.toggleSortDescendingButton)

		self.exportBtn.clicked.connect(self.exportAndSaveTableContents)
		self.confirmExportDirBtn.clicked.connect(self.saveExportDir)
		self.confirmBtn.clicked.connect(self.userSettings)
		self.pushButton_4.clicked.connect(self.showDataVisualizationWidget)
		self.visualizeBtn.clicked.connect(self.generateBarGraph)

		self.setExportDirLine()
		

		self.tableWidget.viewport().installEventFilter(self)
		

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

		self.pushButton_3.clicked.connect(self.exitMainWindow) # Exit

		self.ageLine.textChanged.connect(self.autoFillAgeGroup)
		self.birthDateLine.dateChanged.connect(self.ageCalculation)

		self.selectAllBtn.setCheckable(True)
		self.selectAllBtn.clicked.connect(self.toggleSelectAllButton)
		self.sortByLine.currentIndexChanged.connect(self.detectSortByLineChange)

		self.pushButton_9.clicked.connect(self.showAboutPage)

		self.resetExportDirBtn.clicked.connect(self.resetExportDir)

	def displayHelpPage(self):
		self.h = HelpForm()
		self.h.show()


	def closeEvent(self, event, title='Confirm - Close', message='Are you sure you want to exit?'):
		ret = QMessageBox.question(self, title, message,
										 QMessageBox.Yes | QMessageBox.No,
										 QMessageBox.Yes)
		self.setWindowIcon(QIcon('./resources/main_img_resources/csibale'))
		if ret == QMessageBox.Yes:
			dbInstance.closeConnection()
			QMainWindow.closeEvent(self, event)
		else:
			event.ignore()
	

	
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

	def detectSortByLineChange(self):
		if self.sortAscendingBtn.isChecked():
			self.toggleSortAscendingButton()
		else:
			self.toggleSortDescendingButton()

	
	def toggleSelectAllButton(self):
		if self.selectAllBtn.isChecked():
			self.allCheckedFlag = True
			self.selectAllBtn.setStyleSheet("hover; background-color : #2d9272")
			self.searchBeneficiaryData()
		else:
			self.selectAllBtn.setStyleSheet("hover; background-color : #2d9272")
			self.allCheckedFlag = False
			self.searchBeneficiaryData()

	def togglePushButton(self):
		if self.pushButton.isChecked(): 
			self.pushButton.setChecked(True)

			self.pushButton_2.setChecked(False)
			self.pushButton_3.setChecked(False)
			self.pushButton_4.setChecked(False)
			self.pushButton_2.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton_3.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton_4.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton.setStyleSheet("padding: 5px; text-align: left; border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; hover; background-color : #f0faef")
		else:
			self.pushButton.setChecked(False)
	
	def togglePushButton_2(self):
		if self.pushButton_2.isChecked(): 
			self.pushButton_2.setChecked(True)
			
			self.pushButton.setChecked(False)
			self.pushButton_3.setChecked(False)
			self.pushButton_4.setChecked(False)
			self.pushButton.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton_3.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton_4.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton_2.setStyleSheet("padding: 5px; text-align: left; border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; hover; background-color : #f0faef")
		else:
			self.pushButton_2.setChecked(False)
	
	def togglePushButton_3(self):
		if self.pushButton_3.isChecked(): 
			self.pushButton_3.setChecked(True)

			self.pushButton.setChecked(False)
			self.pushButton_2.setChecked(False)
			self.pushButton_4.setChecked(False)
			self.pushButton.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton_2.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton_4.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton_3.setStyleSheet("hover; padding: 5px; text-align: left; border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; background-color : #f0faef")
		else:
			self.pushButton_3.setChecked(False)
	
	def togglePushButton_4(self):
		if self.pushButton_4.isChecked(): 
			self.pushButton_4.setChecked(True)
			
			self.pushButton.setChecked(False)
			self.pushButton_2.setChecked(False)
			self.pushButton_3.setChecked(False)
			self.pushButton.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton_2.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton_3.setStyleSheet("hover; background-color : #9bc7a8")
			self.pushButton_4.setStyleSheet("padding: 5px; text-align: left; border-top-left-radius: 10px; border-top-right-radius: 10px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; hover; background-color : #f0faef")
		else:
			self.pushButton_4.setChecked(False)

	def toggleSortAscendingButton(self):
		 # if button is checked
		if self.sortAscendingBtn.isChecked():
			
			self.sortDescendingBtn.setStyleSheet("background-color : #f0faef")
			self.sortDescendingBtn.setChecked(False)

			self.sortAscendingBtn.setChecked(True)
			self.sortAscendingBtn.setStyleSheet("background-color: #9bc7a8; border-top-left-radius: 8px; border-top-right-radius: 8px; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px")
			self.sortAscending()
  
		# if it is unchecked
		else:
			
			self.sortAscendingBtn.setStyleSheet("background-color : #f0faef")
			self.searchBeneficiaryData()
			
	
	def toggleSortDescendingButton(self):
		 # if button is checked
		if self.sortDescendingBtn.isChecked():
			
			self.sortAscendingBtn.setStyleSheet("background-color : #f0faef")
			self.sortAscendingBtn.setChecked(False)

			self.sortDescendingBtn.setChecked(True)
			self.sortDescendingBtn.setStyleSheet("background-color: #9bc7a8; border-top-left-radius: 8px; border-top-right-radius: 8px; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px")
			self.sortDescending()
  
		# if it is unchecked
		else:
			
			self.sortDescendingBtn.setStyleSheet("background-color : #f0faef")
			self.searchBeneficiaryData()

	
	def exportAndSaveTableContents(self):
		path = self.exportDirectoryLine.text()

		if path == '':
			self.msg = QMessageBox()
			self.msg.setWindowTitle("Error - Export Directory")
			self.msg.setWindowIcon(QIcon('./resources/main_img_resources/Error'))
			self.msg.setText("Please set a path first by selecting a directory in User Settings.")
			self.msg.setIcon(QMessageBox.Critical)
			self.msg.exec()

		else:
			currentDateTime = str(datetime.now().strftime("%m_%d_%Y,%H_%M_%S"))
			self.fileName = f'beneficiaryData_{currentDateTime}.xlsx'
			path = os.path.join(path, 'beneficiaryData').replace('/','\\')

			if not os.path.exists(path):
				os.makedirs(path)

			pathFileNameJoin = os.path.join(path, self.fileName).replace('/','\\')

			columns = range(self.tableWidget.columnCount())
			header = [self.tableWidget.horizontalHeaderItem(column).text() for column in columns]


			workbook = xlsxwriter.Workbook(rf'{pathFileNameJoin}')
			worksheet = workbook.add_worksheet()

			regexNum = '^[0-9]+$'

			
			for i in range(len(header)):
				row = 0
				worksheet.write(row, i, header[i])

			for row in range(self.tableWidget.rowCount()):
				for column in columns:
					if re.match(regexNum, self.tableWidget.item(row, column).text()):
						worksheet.write(row+1, column, int(self.tableWidget.item(row, column).text()))
					else:
						worksheet.write(row+1, column, self.tableWidget.item(row, column).text())

			workbook.close()
				

			self.msg = QMessageBox()
			self.msg.setWindowTitle("Success - Data Exportation")
			self.msg.setIcon(QMessageBox.Information)
			self.msg.setWindowIcon(QIcon('./resources/main_img_resources/success'))
			self.msg.setText(f"Exported to {pathFileNameJoin} successfully")
			self.msg.exec()
	

	def setExportDirLine(self):
		exportDirLineValue = getExportDir(dbCon=dbInstance)
		self.exportDirectoryLine.setText(exportDirLineValue)

	def resetExportDir(self):
		self.exportDirectoryLine.setText("")
		self.saveExportDir()

	def saveExportDir(self):
		setExportDir(self.exportDirectoryLine.text(), dbCon=dbInstance)
		if len(self.exportDirectoryLine.text())==0:
			self.changeExportDirPrompt.setStyleSheet("color: rgb(255, 0, 0);")
			self.changeExportDirPrompt.setText("Directory Reset.")
		else:
			self.changeExportDirPrompt.setStyleSheet("color: rgb(0, 255, 0);")
			self.changeExportDirPrompt.setText("Directory Changed Successfully.")
		

	# Method that sorts QTableWidget items in ascending order based on the current value of sortByLine QComboBox
	def sortAscending(self):
		if self.sortByLine.currentText() != '':
			self.tableWidget.sortByColumn(dataListMap.getColNameToSequentialVal()[self.sortByLine.currentText()], QtCore.Qt.AscendingOrder)
		

	# Method that sorts QTableWidget items in descending order based on the current value of sortByLine QComboBox
	def sortDescending(self):
		if self.sortByLine.currentText() != '':
			self.tableWidget.sortByColumn(dataListMap.getColNameToSequentialVal()[self.sortByLine.currentText()], QtCore.Qt.DescendingOrder)
	

	# Method that changes the displayed placeholder text of searchStringLine based on the current text of searchFilterLine QComboBox
	def searchFilterLineChange(self):
		self.searchStringLine.setPlaceholderText(f"Enter {str(self.searchFilterLine.currentText())}")


	# Method that detects row clicks and returns the row data depending on the click 
	def eventFilter(self, source, event):

		if self.tableWidget.selectedIndexes() != []:
			
			if event.type() == QtCore.QEvent.MouseButtonDblClick:
				if event.button() == QtCore.Qt.LeftButton:
					row = self.tableWidget.currentRow()
					benfId = self.tableWidget.item(row, 0).text()
					results = selectRowFromBenfId(benfId=benfId, dbCon=dbInstance)
					# results = cur.execute(f'SELECT * FROM BENEFICIARY WHERE benfId=={benfId}').fetchall()
					self.showUpdateRow(results)
				# elif event.button() == QtCore.Qt.RightButton:
				# 	row = self.tableWidget.currentRow()
				# 	benfId = self.tableWidget.item(row, 0).text()
				# 	results = selectRowFromBenfId(self, benfId=benfId, dbCon=dbInstance)
				# 	# results = cur.execute(f'SELECT * FROM BENEFICIARY WHERE benfId=={benfId}').fetchall()
				# 	self.showUpdateRow(results)

	   
		return QObject.event(source, event)
	

	# Method that enables the user to search for beneficiary data
	def searchBeneficiaryData(self):

		# Returns all beneficiary data if the searchStringLine is empty
		if (self.searchStringLine.text() == ""):
			self.tableResults = selectAll(dbCon=dbInstance).fetchall() # Retrieve all results from the cursor
			self.rowNum = -1 # Set rowNum == -1 meaning that the current number of rows in the database must be the value of rowNum
			self.loadData(allChecked=self.allCheckedFlag)
		else:
			if self.searchFilterLine.currentText() != "":
				dbColumnName = [i for i in dataListMap.getColNameDbMapping() if dataListMap.getColNameDbMapping()[i]==self.searchFilterLine.currentText()][0] # Finds the column database name based on the provided column display name
				results, rowNum, message = search(searchString=self.searchStringLine.text(), searchFilter=dbColumnName, dbCon=dbInstance) # Retrieves the results, rowNum, and message (if there are errors)
				if message == '': # If there are no results, set the items and row number of the table to the query results and rowNum returned
					self.tableResults = results
					self.rowNum = rowNum
					self.loadData(allChecked=self.allCheckedFlag)
				else: # Display a QMessageBox() indicating the error
					self.msg = QMessageBox()
					self.msg.setText(message)
					self.msg.setIcon(QMessageBox.Critical)
					self.msg.setWindowIcon(QIcon('./resources/main_img_resources/Error'))
					self.msg.exec()
	

	# Method that opens the Update Beneficiary Data Form
	def showUpdateRow(self, results):
		self.w = UpdateForm(results, self)
		self.w.show()

		
	# Method that loads all data
	def loadData(self, allChecked=False):
		
		self.cardValues = getCardsValue(dbCon=dbInstance)

		self.totalNumLabel.setText(str(self.cardValues[0]))
		self.philHealthNumLabel.setText(str(self.cardValues[1]))
		self.cctNumLabel.setText(str(self.cardValues[2]))

		if self.rowNum == -1: # Sets the rowNum to the total row numbers of the database when all data are displayed in the table
			# self.rowNum = len(cur.execute("SELECT * FROM BENEFICIARY;").fetchall())
			self.rowNum = returnRowNum(dbCon=dbInstance)
		
		self.tableWidget.setRowCount(self.rowNum)
		self.tableWidget.verticalHeader().setVisible(False)
		self.tableWidget.setColumnCount(27)
		self.tableWidget.setHorizontalHeaderLabels([v for _,v in dataListMap.getColNameMapping().items()])
		tableRow = 0 # Set initial tableRow to 0 because accessing rows in table are zero-indexed


		# Iteration for each row in current results stored
		for row in self.tableResults:
			for idx,item in zip(range(27), row):
				if idx % 27 == 0: # Sets the checkboxes on the first column only (or first element of each row only) with the data values
					tableWidgetItem = TableWidgetItem(str(item))
					tableWidgetItem.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
					if allChecked:
						tableWidgetItem.setCheckState(QtCore.Qt.CheckState.Checked)
					else:
						tableWidgetItem.setCheckState(QtCore.Qt.CheckState.Unchecked)
					self.tableWidget.setItem(tableRow, idx, tableWidgetItem)
				else:
					# For other cells that does not have a checkbox
					tableWidgetItem = TableWidgetItem(str(item))
					self.tableWidget.setItem(tableRow, idx, tableWidgetItem)


			tableRow += 1 # Increment tableRow by 1 to display the next result to the next row of the tableWidget
		
	
	# Checks which row checkboxes in the table are checked
	def getTableCheckedBoxes(self):

		checkedItems = [] # Initialize an empty list that stores the items of checked rows

		# Iterates each row and checks if the elements (or cells) with checkboxes are checked.
		# If checked, add the row along with its items to checkedItems
		for row in range(self.tableWidget.rowCount()):
			if self.tableWidget.item(row, 0).checkState() == QtCore.Qt.CheckState.Checked:
				checkedItems.append([self.tableWidget.item(row, col).text() for col in range(0,1)][0])
		
		return checkedItems # Return the list that stores the items of checked rows
	

	# Removes the selected (or checked) items (or rows)
	def removeBeneficiaryData(self):
		itemsToRemove = self.getTableCheckedBoxes()

		if itemsToRemove == []:
			self.msg = QMessageBox()
			self.msg.setIcon(QMessageBox.Critical)
			self.msg.setText("No row(s) selected.")
			self.msg.setWindowTitle("Error - Delete")
			self.msg.setWindowIcon(QIcon('./resources/main_img_resources/Error'))
			self.msg.setStandardButtons(QMessageBox.Ok)
			self.msg.exec_()
		else:
			self.msg = QMessageBox()
			self.msg.setIcon(QMessageBox.Information)

			self.msg.setText("Are you sure you want to delete these data? This action cannot be undone.")
			self.msg.setWindowTitle("Warning - Delete")
			self.msg.setWindowIcon(QIcon('./resources/main_img_resources/Error2'))
			self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
			retval = self.msg.exec_()

			if retval == 1024:
				
				remove_rows(itemIds=itemsToRemove, dbCon=dbInstance)
				self.searchBeneficiaryData() # Ensures that loadData() updates in the table also works for filtered items displayed when removal(s) or deletion(s) are performed
				self.msg = QMessageBox()
				self.msg.setWindowTitle("Success - Remove Beneficiary")
				self.msg.setText("Beneficiary Data(s) was/were successfully removed!")
				self.msg.setIcon(QMessageBox.Information)
				self.msg.exec()

	
	# Method that inserts beneficiary data - triggered by confirmAddBtn
	def insertBeneficiaryData(self):

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
			self.msg.setWindowIcon(QIcon('./resources/main_img_resources/Error'))
			self.msg.exec()
		else:   # Adds beneficiary data if there are no errors
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
	

			self.birthDateLine.dateChanged.connect(self.ageCalculation)

			if self.statusLine.currentText() == "Ongoing":
				closureDateToStore = ""
			else:
				closureDateToStore = self.closureDateLine.date().toPyDate()

			if self.employedLine.currentText() == 'No':
				occupation = ""
			else:
				occupation = self.occupationLine.text().title()
				

			dataPayload = {
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
				'benfOccupation' : occupation,
				'benfNumFamMem'  : int(self.numFamLine.text()),
				'benfAdmissionDate' : self.admissionDateLine.date().toPyDate(),
				'benfClosureDate' : closureDateToStore,
				'benfStatus' : self.statusLine.currentText(),
				'benfClosureReason' : self.reasonClosureLine.currentText()
			}

			insert_row(dataToInsert=dataPayload, dbCon=dbInstance)

			self.loadData()

			self.msg = QMessageBox()
			self.msg.setWindowTitle("Success - Add Beneficiary")
			self.msg.setText("Beneficiary Data was successfully added!")
			self.msg.setIcon(QMessageBox.Information)
			self.msg.exec()
			
	# Helper Method that validates the content of the fields (i.e. QLineEdit, QComboBox, QDateEdit)
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
			self.muncLine,
			self.brgyLine,
			self.ipLine,
			self.philhealthLine,
			self.cctLine,
			self.medicineLine,
			self.employedLine,
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

		
		for field in fieldsMustNotBeEmpty:
			if isinstance(field, QtWidgets.QLineEdit):
				if field.text() == '':
					field.setPlaceholderText("Required")
					isEmpty = True
			elif isinstance(field, QtWidgets.QComboBox):
				if field.currentText() == '':
					field.setPlaceholderText("Required")
					isEmpty = True
			elif isinstance(field, QtWidgets.QDateEdit):
				if str(field.date().toPyDate()) == '':
					isEmpty = True
		
		
		for field in fieldsMustBeInt:
			if isinstance(field, QtWidgets.QLineEdit):
				if not(field.text().isnumeric()):
					field.setText("")
					field.setPlaceholderText("Must be a number")
					nonIntError = True
				print(nonIntError)
		
		for field in fieldsMustBeAlpha:
			if isinstance(field, QtWidgets.QLineEdit):
				if any(char.isdigit() for char in field.text()):
					field.setText("")
					field.setPlaceholderText("Must not contain a number")
					nonAlphaError = True
		
		return (isEmpty, nonIntError, nonAlphaError)

	# Method that redirects the user to the "Home" Page
	def showHomeWidget(self):
		self.stackedWidget.setCurrentWidget(self.homeWidget)
		self.searchBeneficiaryData()
		self.changeExportDirPrompt.setText("")
		self.changeUsernamePwdPrompt.setText("")

	# Method that redirects the user to the "User (Admin) Settings" Page
	def showUserSettingsWidget(self):
		self.stackedWidget.setCurrentWidget(self.userSettingsWidget)
	
	# Method that opens file dialog box to choose a directory path for file exportation
	def chooseDirectoryLocation(self):
		dirName = QFileDialog.getExistingDirectory(self, 'Select Folder')
		self.exportDirectoryLine.setText(dirName)
	
	# Method that redirects the user to the "Add Beneficiary" Page
	def goToAddBeneficiaryWidget(self):

		self.stackedWidget.setCurrentWidget(self.addBeneficiaryWidget)


		self.firstNameLine.clear()
		self.lastNameLine.clear()
		self.suffixLine.clear()
		self.ageCalculation()
		self.genderLine.setCurrentIndex(0)

		self.disSpecLine.setCurrentIndex(0)
		self.disDescLine.clear()
		self.fatherNameLine.clear()
		self.motherNameLine.clear()
		self.muncLine.setCurrentIndex(0)
		# self.brgyLine.setCurrentIndex(0)
		self.ipLine.setCurrentIndex(0)
		self.philhealthLine.setCurrentIndex(0)
		self.cctLine.setCurrentIndex(0)
		self.educationLine.setCurrentIndex(0)
		self.gradeLvlLine.setCurrentIndex(0)
		self.medicineLine.setCurrentIndex(0)
		self.employedLine.setCurrentIndex(0)
		self.occupationLine.clear()
		self.numFamLine.clear()
		
		self.admissionDateLine.setDate(QDate.currentDate())

		self.educationLine.setCurrentIndex(0)
		self.statusLine.setCurrentIndex(0)
		self.reasonClosureLine.setCurrentIndex(0)


		if (self.educationLine.currentText() == "") or (self.educationLine.currentText() == "Daycare"):
			self.gradeLvlLine.setCurrentIndex(0)
			self.gradeLvlLine.setEnabled(False)


		if (self.employedLine.currentText() == "No") or (self.employedLine.currentText() == ""):
			self.occupationLine.setText("")
			self.occupationLine.setEnabled(False)
		

		if (self.statusLine.currentText() == "Ongoing") or (self.statusLine.currentText() == ""):
			self.reasonClosureLine.setEnabled(False)
			self.closureDateLine.setEnabled(False)
			self.reasonClosureLine.setCurrentIndex(0)
		
		self.educationLine.currentIndexChanged.connect(self.detectChangeEducationLine)
		self.employedLine.currentIndexChanged.connect(self.detectChangeEmployedLine)
		self.statusLine.currentIndexChanged.connect(self.detectChangeClosureLines)
		self.birthDateLine.dateChanged.connect(self.ageCalculation)
		
		self.admissionDateLine.setDateRange(self.birthDateLine.date(), QDate.currentDate())
		self.closureDateLine.setDateRange(self.admissionDateLine.date(), QDate.currentDate())
		self.birthDateLine.dateChanged.connect(lambda: self.admissionDateLine.setDateRange(self.birthDateLine.date(), QDate.currentDate()))
		self.admissionDateLine.dateChanged.connect(lambda: self.closureDateLine.setDateRange(self.admissionDateLine.date(), QDate.currentDate()))
		
	
	def ageCalculation(self):
		correctAge = int(abs(QDate.currentDate().daysTo(self.birthDateLine.date())/365))
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
			self.reasonClosureLine.setCurrentIndex(0)
		else:
			self.reasonClosureLine.setEnabled(True)
			self.closureDateLine.setEnabled(True)
	
	# Helper method that updates the content of QComboBox of Barangay depending on the selected Municipality
	def updateBrgyCombo(self, index):
		self.brgyLine.clear()
		brgys = self.muncLine.itemData(index)
		if brgys:
			self.brgyLine.addItems(brgys)

	# Method that enables side menu bar animation
	def slideLeftMenu(self):
		width = self.leftMenu.width()

		if width == 55:
			newWidth = 220
		else:
			newWidth = 55
		
		self.animation = QPropertyAnimation(self.leftMenu, b"minimumWidth")
		self.animation.setDuration(50)
		self.animation.setStartValue(width)
		self.animation.setEndValue(newWidth)
		self.animation.start()


	# Method that updates user log in settings
	def userSettings(self):

		username = self.lineEdit_2.text()
		oldpassword = self.lineEdit_3.text()
		newpassword = self.lineEdit_4.text()
		passwordHash = passwordHashEncode(password=newpassword)
		
		# Method that Determines if there are blank lines
		if len(username)==0 or len(oldpassword)==0 or len(newpassword)==0:
			self.changeUsernamePwdPrompt.setStyleSheet("color: rgb(255, 0, 0);")
			self.changeUsernamePwdPrompt.setText("Please fill in all required fields.")

		else:
			self.msg = QMessageBox()
			self.msg.setIcon(QMessageBox.Warning)
			self.msg.setWindowTitle("Warning")
			self.msg.setWindowIcon(QIcon('./resources/main_img_resources/Error2'))
			self.msg.setText("Please ensure that you remember your New Password because this action is irreversible.")
			self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
			retval = self.msg.exec_()

			if retval == 1024:

				result, = returnOldPassword(dbInstance)
				
				passwordMatching = passwordDecodeMatch(password=oldpassword, result=result)

				# Method that Updates the login credentials in the database
				# Will only update when old password matches in the database
				if (passwordMatching == True):

					updateUsernamePassword(username=username, passwordHash=passwordHash, result=result, dbCon=dbInstance)
					
					self.changeUsernamePwdPrompt.setStyleSheet("color: rgb(0, 255, 0);")
					self.changeUsernamePwdPrompt.setText("Changed Successfully!")

					# Resets the values
					self.lineEdit_2.setText("") 
					self.lineEdit_3.setText("")
					self.lineEdit_4.setText("")
					
				else:
					self.changeUsernamePwdPrompt.setStyleSheet("color: rgb(255, 0, 0);")
					self.changeUsernamePwdPrompt.setText("Incorrect password, change unsuccessful.")

					# Resets the values
					self.lineEdit_2.setText("") 
					self.lineEdit_3.setText("")
					self.lineEdit_4.setText("")


	def showDataVisualizationWidget(self):
		self.stackedWidget.setCurrentWidget(self.dataVisualizationWidget)

		filter1LineItems = [v for _,v in dataListMap.getCategoricalColsMapping().items()]
		filter2LineItems = [v for _,v in dataListMap.getCategoricalColsMapping().items()]
		filter3LineItems = [v for _,v in dataListMap.getCategoricalColsMapping().items()]


		if (self.filter1Line.count() <= 0):
			self.filter1Line.addItems(filter1LineItems)

		if (self.filter2Line.count() <= 0):
			self.filter2Line.addItems(filter2LineItems)

		if (self.filter3Line.count() <= 0):
			self.filter3Line.addItems(filter3LineItems)
	

	def showAboutPage(self):
		self.stackedWidget.setCurrentWidget(self.about)
		

	def generateBarGraph(self):
		filter1 = [i for i in dataListMap.getCategoricalColsMapping() if dataListMap.getCategoricalColsMapping()[i]==self.filter1Line.currentText()][0]
		filter2 = [i for i in dataListMap.getCategoricalColsMapping() if dataListMap.getCategoricalColsMapping()[i]==self.filter2Line.currentText()][0]
		filter3 = [i for i in dataListMap.getCategoricalColsMapping() if dataListMap.getCategoricalColsMapping()[i]==self.filter3Line.currentText()][0]

		filterList = [filter1, filter2, filter3]

		if '' in filterList:
			filterList = [x for x in filterList if x.strip()]
			
		
		if filterList == []:
			self.msg = QMessageBox()
			self.msg.setWindowTitle("Error - Filter")
			self.msg.setText("At least one filter must be fill!")
			self.msg.setIcon(QMessageBox.Critical)
			self.msg.setWindowIcon(QIcon('./resources/main_img_resources/Error'))
			self.msg.exec()

		else:
			if len(filterList) != len(set(filterList)):
				self.xLabels = None
				self.yValues = None
				self.msg = QMessageBox()
				self.msg.setWindowTitle("Error - Filter")
				self.msg.setText("Filters must be unique!")
				self.msg.setIcon(QMessageBox.Critical)
				self.msg.setWindowIcon(QIcon('./resources/main_img_resources/Error'))
				self.msg.exec()
			else:
				filterResult = ','.join(filterList)
				results = returnDataToVisualize(filterResult=filterResult, dbCon=dbInstance)

				if results == []:
					self.msg = QMessageBox()
					self.msg.setWindowTitle("Error - Filter")
					self.msg.setText("No data to visualize!")
					self.msg.setIcon(QMessageBox.Critical)
					self.msg.setWindowIcon(QIcon('./resources/main_img_resources/Error'))
					self.msg.exec()
				
				else:
					xLabels = []
					yValues = []

					summary = ''

					for result in results:
						xAxisLabelResult = ';'.join(result[0:len(result)-1])
						summary += xAxisLabelResult + ' = ' + str(result[-1]) + '\n'
						xLabels.append(xAxisLabelResult)
						yValues.append(result[-1])

					set0 = QBarSet('Result')


					set0.append(yValues)


					series = QBarSeries()
					series.append(set0)

					chart = QChart()
					chart.addSeries(series)
					chart.setTitle('Bar Chart ({})'.format(', '.join([dataListMap.getCategoricalColsMapping()[x] for x in filterResult.split(',')])))
					chart.setAnimationOptions(QChart.SeriesAnimations)

					months = xLabels

					axisX = QBarCategoryAxis()
					axisX.append(months)

					axisY = QValueAxis()
					axisY.setRange(0, max(yValues))

					chart.addAxis(axisX, QtCore.Qt.AlignBottom)
					chart.addAxis(axisY, QtCore.Qt.AlignLeft)

					chart.legend().setVisible(True)
					chart.legend().setAlignment(QtCore.Qt.AlignBottom)

					chartView = QChartView(chart)

					if self.chartContent == None:
						self.chartContent = chartView
						self.summary = summary
						self.verticalLayout_26.addWidget(chartView)
						self.label_29.setText(summary)

						
					else:
						currentContent = self.chartContent
						self.verticalLayout_26.removeWidget(currentContent)
						self.chartContent  = chartView
						self.summary = summary
						self.verticalLayout_26.addWidget(self.chartContent)
						self.label_29.setText(summary)


	def exitMainWindow(self):
		ret = self.close()
		if ret == True:
			dbInstance.closeConnection()
	
	# Method to be able to see the show and hide in tray icon
	def show_hide_tray(self):
		if self.isVisible():
			action_show_hide.setText("Show Window")
			self.hide()
		else:
			action_show_hide.setText("Hide Window")
			self.showNormal()

	def handle_entered(self):
		self.label.setText("Wassup yall?")
		
	def handle_leaved(self):
		self.label.setText("Initial Text")	
		
		

if __name__ == '__main__':
	app = QApplication(sys.argv)

	s1 = MainWindow()
	s1.show()

	#Setting up Tray Icon
	trayIcon = QSystemTrayIcon(QIcon('./resources/main_img_resources/csibale3.png'))
	menu = QMenu()
	trayIcon.setToolTip('CSIBALE Data Storage')

	#Setting up Show and Hide
	action_show_hide = QtWidgets.QAction("Hide Window")
	action_show_hide.triggered.connect(lambda: s1.show_hide_tray())
	menu.addAction(action_show_hide)

	#Setting up Menu Exit
	exitAction = menu.addAction('Exit')
	exitAction.triggered.connect(app.quit)

	#Triggering the Tray Icon
	trayIcon.setContextMenu(menu)
	trayIcon.show()

	sys.exit(app.exec())