from backend import SingletonClass

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

from resources.HelpPageForm import Ui_Form as HelpFormUi

# Update Form Window for modifying beneficiary data 
class HelpForm(QWidget, HelpFormUi, SingletonClass):
	
	def __init__(self):
		super(HelpForm, self).__init__()
		self.setupUi(self)
		self.setWindowIcon(QIcon('./csibale.png'))
		self.setWindowTitle('Help')