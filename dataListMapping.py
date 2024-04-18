class DataListMapping:
    # List of Disability Specififications to add to a QComboBox Widget
    _disabilitySpecList = [
        '',
        'Epilepsy',
        'Celebral Palsy',
        'Club Feet',
        'Hearing Impairment/Deaf',
        'Intellectual/Learning Disability',
        'Polio',
        'Down Syndrome',
        'ASD',
        'Vision Impairement/Blind',
        'Hydrocephalus',
        'Cleft Lip/Palate',
        'Amputated',
        'Knock/Bow Knee',
        'Orthopedic Disability',
        'Neuromuscular Disorder',
        'Others'
    ]

    # List of Gender Data to add to a QComboBox Widget
    _genderList = [
        '',
        'Male',
        'Female',
        'Prefer not to say'
    ]

    # List of Yes or No Data to add to a QComboBox Widget
    _yesOrNo = [
        '',
        'Yes',
        'No'
    ]

    # List of Status Data to add to a QComboBox Widget
    _statusList = [
        '',
        'Ongoing',
        'For Closure',
        'Closed'
    ]

    # List of Closure Reasons to add to a QComboBox Widget
    _closureReasonList = [
        '',
        'Inactive',
        'Already Employed',
        'Died',
        'Out of Town',
        'Over Age',
        'Forfeited',
        'No Information'
    ]

    # List of Education List to add to a QComboBox Widget
    _educationList = [
        '',
        'Home Program',
        'Daycare',
        'K-12 Curriculum'
    ]

    # List of Grade Levels to add to a QComboBox Widget
    _gradeLvlList = [
        '',
        '1','2','3','4','5','6','7','8','9','10','11','12',
        'Elementary - unspecified',
        'High School - unspecified',
        'SPED'
    ]

    # Mapping of Region and Barangays to have a dynamic QCombo Widget
    _muncBrgyMapping = {
        '' : [],
        'Alcantara' : ['Bonlao','Calagonsao','Camili','Comod-om','Madalag','Poblacion','San Isidro','Tugdan','Bagsik','Gui-ob','Lawan','San Roque'],
        'Banton' : ['Balogo','Banice','Hambi-an','Lagang','Libtong','Mainit','Nabalay','Nasunogan','Poblacion','Sibay','Tan-Ag','Toctoc','Togbongan','Togong','Tungonan','Tumalum','Yabawon'],
        'Cajidiocan' : ['Alibagon','Cambajao','Cambalo','Cambijang','Cantagda','Danao','Gutivan','Lico','Lumbang Este','Lumbang Weste','Marigondon','Poblacion','Sugod','Taguilos'],
        'Calatrava' : ['Balogo','Linao','Poblacion','Pagsangahan','Pangulo','San Roque','Talisay'],
        'Concepcion' : ['Bakhawan','Calabasahan','Dalajican','Masudsud','Poblacion','Sampong','San Pedro/Agbatang','San Vicente','Masadya'],
        'Corcuera' : ['Alegria','Ambulong','Colongcolong','Gobon','Guintiguiban','Ilijan','Labnig','Mabini','Mahaba','Mangansag','Poblacion','San Agustin','San Roque','San Vicente','Tacasan'],
        'Ferrol' : ['Agnonoc','Bunsoran','Claro M. Recto','Poblacion','Hinaguman','Tubigon'],
        'Looc' : ['Agojo','Balatucan','Buenavista','Camandag','Guinhaya-an','Limon Norte','Limon Sur','Manhac','Pili','Poblacion','Punta','Tuguis'],
        'Magdiwang' : ['Agsao','Agutay','Ambulong','Dulangan','Ipil','Jao-asan','Poblacion','Silum','Tampayan'],
        'Odiongan' : ['Amatong','Anahao','Bangon','Batiano','Budiong','Canduyong','Dapawan (Poblacion)','Gabawan','Libertad','Ligaya (Poblacion)','Liwanag (Poblacion)','Liwayway (Poblacion)','Manlilico','Mayha','Panique','Pato-o','Poctoy','Progreso Este','Progreso Weste','Rizal','Tabing Dagat (Poblacion)','Tabobo-an','Tuburan','Tumingad','Tulay'],
        'Romblon' : ['Agbaluto','Agpanabat','Agbudia','Agnaga','Agnay','Agnipa','Agtongo','Alad (island barangay)','Bagacay','Cajimos','Calabogo','Capaclan','Ginablan','Guimpingan','Ilauran','Lamao','Li-o','Logbon (island barangay)','Lunas','Lonos','Macalas','Mapula','Cobrador (Naguso)','Palje','Barangay I (Poblacion)','Barangay II (Poblacion)','Barangay III (Poblacion)','Barangay IV (Poblacion)','Sablayan','Sawang','Tambac'],
        'San Agustin' : ['Bakhawan','Binongaan','Buli','Cabolutan','Cagboaya','Camantaya','Carmen','Cawayan','Doña Juana','Dubduban','Hinugusan','Lusong','Mahabangbaybay','Poblacion','Sugod'],
        'San Andres' : ['Agpudlos','Calunacon','Doña Trinidad Roxas','Linawan','Mabini','Marigondon Norte','Marigondon Sur','Matutuna','Pag-Alad','Poblacion','Tan-Agan','Victoria','Juncarlo'],
        'San Fernando' : ['Agtiwa','Azagra','Campalingo','Canjalon','España','Mabini','Mabulo','Otod','Panangcalan','Pili','Poblacion','Taclobo'],
        'San Jose' : ['Busay','Combot','Lanas','Pinamihagan','Poblacion (Agcogon)'],
        'Santa Fe' : ['Agmanic','Canyayo','Danao Norte','Danao Sur','Guinbirayan','Guintigbasan','Magsaysay','Mat-i','Pandan','Poblacion','Tabugon'],
        'Santa Maria' : ['Bonga','Concepcion Norte (Poblacion)','Concepcion Sur','Paroyhog','Santo Niño','San Isidro']
    }


    # Mapping of widgets with corresponding column display name
    _colNameMapping = {
        'idLine' : 'Beneficiary ID',
        'firstNameLine': 'First Name', 
        'lastNameLine': 'Last Name',
        'suffixLine' : 'Suffix', 
        'ageLine': 'Age',
        'ageGroupLine': 'Age Group', 
        'genderLine': 'Gender',
        'birthDateLine': 'Birthdate', 
        'disSpecLine': 'Disability Specification', 
        'disDescLine': 'Disability Description', 
        'fatherNameLine': 'Name of Father', 
        'motherNameLine': 'Name of Mother', 
        'muncLine': 'Municipality', 
        'brgyLine': 'Barangay', 
        'ipLine': 'Indigent Person', 
        'philhealthLine': 'Philhealth Member', 
        'cctLine': 'CCT Member', 
        'educationLine': 'Education', 
        'gradeLvlLine': 'Grade Level', 
        'medicineLine': 'Medicine', 
        'employedLine': 'Employed', 
        'occupationLine': 'Occupation', 
        'numFamLine': 'Number of Family Members',
        'admissionDateLine': 'Admission Date',
        'closureDateLine': 'Closure Date', 
        'statusLine': 'Status', 
        'reasonClosureLine': 'Reason of Closure'
    }


    # Mapping of column names (from colNameMapping) to a specific range of values (0-25) - Used for sorting items in QTableWidget
    _colNametoSequentialVal = dict(zip([v for _,v in _colNameMapping.items()],[x for x in range(26)]))


    # Mapping of column database name with corresponding column display name
    _colNameDbMapping = {
        '' : '',
        'benfId' : 'Beneficiary ID',
        'benfFirstName' : 'First Name', 
        'benfLastName' : 'Last Name',
        'benfSuffix': 'Suffix', 
        'benfAge': 'Age',
        # 'benfAgeGroup' : 'Age Group',
        'benfGender': 'Gender',
        'benfBirthdate': 'Birthdate', 
        'benfDisabilitySpec' : 'Disability Specification', 
        'benfDisabilityDesc' : 'Disability Description', 
        'benfFatherName' : 'Name of Father', 
        'benfMotherName' : 'Name of Mother', 
        'benfMunc' : 'Municipality', 
        'benfBrgy' : 'Barangay',
        'muncBrgy' : 'Municipality,Barangay', 
        'benfIP' : 'Indigent Person', 
        'benfPhilhealth' : 'Philhealth Member', 
        'benfCCT' : 'CCT Member', 
        'benfEducation' : 'Education', 
        'benfGradeLvl' : 'Grade Level',
        'benfMedicine' : 'Medicine', 
        'benfEmployed' : 'Employed', 
        'benfOccupation' : 'Occupation',
        'benfNumFamMem' : 'Number of Family Members',
        'benfAdmissionDate' : 'Admission Date',
        'benfClosureDate' : 'Closure Date',
        'benfStatus' : 'Status', 
        'benfClosureReason' : 'Reason of Closure'
    }


    _categoricalColsMapping = {
        '':'',
        'benfAgeGroup' : 'Age Group',
        'benfGender' : 'Gender',
        'benfDisabilitySpec' : 'Disability Specification',
        'benfMunc': 'Municipality',
        'benfBrgy': 'Barangay',
        'benfIP': 'Indigenous Person',
        'benfPhilhealth': 'Philhealth Member',
        'benfCCT': 'CCT Member',
        'benfEducation': 'Education',
        'benfGradeLvl': 'Grade Level',
        'benfMedicine': 'Medicine',
        'benfEmployed': 'Employed',
        'benfStatus': 'Status'
    }

    def getDisabilitySpecList(self):
        return self._disabilitySpecList

    
    def getGenderList(self):
        return self._genderList
    
    def getYesOrNoList(self):
        return self._yesOrNo
    
    def getClosureReasonList(self):
        return self._closureReasonList
    
    def getEducationList(self):
        return self._educationList
    
    def getGradeLvlList(self):
        return self._gradeLvlList

    def getStatusList(self):
        return self._statusList    

    def getMuncBrgyMapping(self):
        return self._muncBrgyMapping
    
    def getColNameMapping(self):
        return self._colNameMapping
    
    def getColNameToSequentialVal(self):
        return self._colNametoSequentialVal
    
    def getColNameDbMapping(self):
        return self._colNameDbMapping

    def getCategoricalColsMapping(self):
        return self._categoricalColsMapping