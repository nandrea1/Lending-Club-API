#from lc_models import Loan
from lending_club import LendingClub
from datetime import datetime
'''
def createSampleLoan():
	loan = Loan()
	loan.last_updated = datetime.now()
	loan.loan_id = 1
	loan.loan_amt = 15000
	loan.term = 36
	loan.interest_rate = .095
	loan.calcPayment(overwrite=True)
	loan.save()
'''	
def getAccountSummary(lc):
	resp = lc.getAccountSummary()
	assert len(resp) > 0
	
def getOwnedNotes(lc):
	resp = lc.getOwnedNotes()
	assert len(resp) >0
	
def getPortfolios(lc):
	resp = lc.getPortfolios()
	assert len(resp) >0
	
def getDetailedOwnedNotes(lc):
	resp = lc.getDetailedOwnedNotes()
	assert len(resp)>0
	
def getPendingTransfers(lc):
	resp = lc.getPendingTransfers()
	assert len(resp) >0
	
def getListedLoans(lc):
	resp = lc.getListedLoans(response_type='csv')
	assert len(resp) >0
	
def createPortfolio(lc):
	portfolio_name = 'Test Automated Portfolio'
	portfolio_description = 'This is a test portfolio created by the python api'
	resp = lc.createPortfolio(portfolio_name=portfolio_name, portfolio_description=portfolio_description)
	
	
