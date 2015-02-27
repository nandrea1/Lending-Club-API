import requests
import json
import pandas as pd
import datetime
from io import StringIO
import finance
authorization = 'p+rvZIa8G6j2vO5xjjDi8/5BgxA='
investor_id = '1258941'

def getSecondaryLoans(save=False, savepath='secondary_loans.csv'):
	resp = requests.get('https://resources.lendingclub.com/SecondaryMarketAllNotes.csv', verify=False)
	loans = resp.text
	if save:
		f.open(savepath, 'w')
		f.write(loans)
		f.close()

def login(username, password):
	login_url='https://www.lendingclub.com/account/login.action'
	login_string='login_url=&login_email='+username+'&login_password='+password+'&login_remember_me=on&offeredNotListedPromotionFlag='
	headers = {'Host': 'www.lendingclub.com',
	'Connection': 'keep-alive',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Origin': 'https://www.lendingclub.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Referer': 'https://www.lendingclub.com/account/gotoLogin.action',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-US,en;q=0.8'}
	resp = requests.post(url=login_url, data=login_string, headers=headers, verify=False)
	c1 = resp.cookies['www.lendingclub.com-prod_lcui_grp']
	c2 = resp.cookies['JSESSIONID-lcui-prod_nevada']
	print('Cookie 1 is: ' + str(c1))
	print('Cookie 2 is: ' + str(c2))
	return resp.text
	
def getLoanDetail(loan_id):
	url = 'https://www.lendingclub.com/browse/loanDetailFull.action?loan_id='+loan_id+'&previous='

def getPortfolio(format='application/json', save=False, savepath='portfolio.csv'):
		print('Getting Portfolio. Save Status is : ' +str(save))
		url = 'https://api.lendingclub.com/api/investor/v1/accounts/'+investor_id+'/detailednotes'
		resp = __getLCData(url, format=format, save=save, savepath=savepath)
		if resp['format'] == 'application/json':
			ports = json.loads(resp['data'])
			ports = ports['myNotes']
			#port = json.loads(ports)
			df=pd.DataFrame.from_dict(ports)
			df['issueDate'] = pd.to_datetime(df['issueDate'].str[0:10] + df['issueDate'].str[10:19])
			df['lastPaymentDate'] = pd.to_datetime(df['lastPaymentDate'].str[0:10] + df['lastPaymentDate'].str[10:19])
			df['nextPaymentDate'] = pd.to_datetime(df['nextPaymentDate'].str[0:10] + df['nextPaymentDate'].str[10:19])
			df['loanStatusDate'] = pd.to_datetime(df['loanStatusDate'].str[0:10] + df['loanStatusDate'].str[10:19])
			df['orderDate'] = pd.to_datetime(df['orderDate'].str[0:10] + df['orderDate'].str[10:19])
			print('Length of Portfolio data is ' + str(len(df)))
		if save:
			df.to_csv(savepath, index=False)
		return ports

def generateCashFlowSchedule(portfolio, days=60):
	active_loans = portfolio[portfolio['loanStatus'] == 'Current']
	dts = []
	cashflows=pd.DataFrame()
	tdy = datetime.date.today()
	dts.append(tdy)
	for i in range(1,days):
		new_dt = tdy + datetime.timedelta(days=i)
		dts.append(new_dt)
	for loan in active_loans:
		#cashflow={}
		cashflows['loan_id'] = loan['loanId']
		cashflows['loan_amt'] = loan['loanAmount']
		cashflows['apr'] = loan['interestRate']
		for dt in dts:
			cashflow[dt] = ''
			if dt == flow_dt:
				i = float(loan['interestRate'])/100
				amt = float(loan['noteAmount'])
				n = int(loan['loanLength'])
				cashflow[dt] = finance.getPV(n, amt,i)
			cashflows.append(cashflow)
	return cashflows
		
def getLoans(format='application/json', save=False, savepath='loans.csv'):
	req_url = 'https://api.lendingclub.com/api/investor/v1/loans/listing?showAll=true'
	lns = __getLCData(req_url, format=format, save=save, savepath=savepath)
	print('Length of Loan data is ' + str(len(lns)))
	return lns
		
def __getLCData(req_url, format='application/json', save=False, savepath='default_file.csv'):
	headers={'authorization':authorization, 'Accept':format}
	print('Calling LC API. Save Data Status is: ' + str(save))
	resp = requests.get(req_url, headers=headers, verify=False)
	loans = resp.text
	ret = ''
	df=''
	try:
		if format == 'application/json':
			print('Loading JSON Loan Data')
			loans = json.loads(resp.text)
			df=pd.DataFrame.from_dict(loans)
			ret = df
		elif format == 'text/plain':
			#loans = resp.text
			print('Loading CSV Loan Data')
			loans = StringIO(resp.text)
			df = pd.DataFrame.from_csv(loans, indexCol=False)
			ret = df
		elif format == 'application/xml':
			print('Loading XML Loan Data')
			print('Cannot Save XML')
			save = False
			loans = resp.text
			ret = loans
	except Exception as e:
		print('Could not download loans')
		print(str(e))
		loans = str(e)
		ret = loans
	resp_obj={'format':format, 'data':resp.text}
	return resp_obj
	


