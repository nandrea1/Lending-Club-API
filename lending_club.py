import requests
import settings
import json
import logging

class LendingClub():

	auth=''
	investor_id=''
	logger=''
	lc_accounts_url = settings.lc_accounts_url
	lc_loans_url = settings.lc_loans_url
	header_map = {'json':'application/json', 'csv':'text/plain', 'xml':'application/xml'}
	headers = {'Authorization':''}
	
	def __init__(self,authorization, investor_id, logger=''):
		self.auth = authorization
		self.investor_id = investor_id
		self.headers['Authorization'] = self.auth
		if logger != '':
			self.logger = logging.getLogger(logger)
		else:
			self.logger = logging.getLogger('LendingClub')
			self.logger.setLevel(logging.DEBUG)
	
	def _submitLCRequest(self, path, response_type='json'):
		url = self.lc_accounts_url + self.investor_id + path
		self.logger.debug('Request URL is ' + url)
		self.headers['Content-Type'] = self.header_map[response_type]
		headers = self.headers
		self.logger.debug('Headers Are: ' + str(headers))
		resp = requests.get(url, headers=headers, verify=False)
		self.logger.debug('Lending Club Response is: ' + str(resp.text))
		return resp
		
	def _postLCRequest(self, path, data, response_type='json'):
		url = self.lc_accounts_url + self.investor_id + path
		self.logger.debug('Request URL is ' + url)
		self.headers['Content-Type'] = self.header_map[response_type]
		headers = self.headers
		self.logger.debug('Headers Are: ' + str(headers))
		self.logger.debug('Data is: ' + str(data))
		resp = requests.post(url, data=data, headers=headers, verify=False)
		self.logger.debug('Lending Club Response is: ' + str(resp.text))
		return resp
		
	### Simple GET Requests Used to Retrieve Various Lending Club Data Assocaited with the Specified Investor ID ###
	
	def getAccountSummary(self, response_type='json'):
		self.logger.debug('Getting Account Summary')
		resp = self._submitLCRequest('/summary', response_type)
		resp_obj = resp.json()
		return resp_obj
		
	def getOwnedNotes(self, response_type='json'):
		self.logger.debug('Getting Owned Notes')
		resp = self._submitLCRequest('/notes', response_type)
		resp_obj = resp.json()
		return resp_obj
		
	def getDetailedOwnedNotes(self, response_type='json'):
		self.logger.debug('Getting Detailed Notes')
		resp = self._submitLCRequest('/detailednotes', response_type)
		resp_obj = resp.json()
		return resp_obj
		
	def getPortfolios(self, response_type='json'):
		self.logger.debug('Getting Portfolios')
		resp = self._submitLCRequest('/portfolios', response_type)
		resp_obj = resp.json()
		return resp_obj
		
	def getPendingTransfers(self, response_type='json'):
		self.logger.debug('Getting Pending Transfers')
		resp = self._submitLCRequest('/funds/pending', response_type)
		resp_obj = resp.json()
		return resp_obj
		
	def getListedLoans(self, response_type='json'):
		self.logger.debug('Getting Listed Loans')
		url = self.lc_loans_url + 'listing'
		self.logger.debug('Request URL is ' + url)
		self.headers['Content-Type'] = self.header_map[response_type]
		headers = self.headers
		self.logger.debug('Headers Are: ' + str(headers))
		resp = requests.get(url, headers=headers, verify=False)
		self.logger.debug('Lending Club Response is: ' + str(resp.text))
		return resp.json()
		
		
	### POST Requests used to take action on Lendng Club Platform. Be careful with these as they can allocate real dollars to loans ###
	
	def createPortfolio(self, portfolio_name, portfolio_description='', response_type='json'):
		self.logger.debug('Creating Portfolio with name %s' %(portfolio_name))
		req = {}
		req['aid'] = self.investor_id
		req['portfolioName'] = portfolio_name
		req['portfolioDescription'] = portfolio_description
		resp = self._postLCRequest('/portfolios', req)
		resp_obj = resp.json()
		return resp_obj
		