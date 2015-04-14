import csv
from lc_models import Loan, LoanCashflow
from datetime import datetime, date, timedelta

pmt_file = 'PMTHIST_ALL_20150318.csv'

fields = ['LOAN_ID','PBAL_BEG_PERIOD', 'PRNCP_PAID',
		'INT_PAID', 'FEE_PAID', 'DUE_AMT',
		'RECEIVED_AMT', 'RECEIVED_D', 'PERIOD_END_LSTAT',
		'MONTH', 'PBAL_END_PERIOD', 'MOB',
		'CO', 'COAMT', 'InterestRate',
		'IssuedDate', 'MONTHLYCONTRACTAMT', 'dti',
		'State', 'HomeOwnership', 'MonthlyIncome',
		'EarliestCREDITLine', 'OpenCREDITLines', 'TotalCREDITLines',
		'RevolvingCREDITBalance', 'RevolvingLineUtilization', 'Inquiries6M',
		'DQ2yrs', 'MonthsSinceDQ', 'PublicRec', 'MonthsSinceLastRec',
		'EmploymentLength', 'currentpolicy', 'grade', 'term',
		'APPL_FICO_BAND', 'VINTAGE', 'PCO_RECOVERY', 'PCO_COLLECTION_FEE'
		'policy_code']



		
def _getLoanFromHistoryFile(file):
	loan = ''
	with open(pmt_file, 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			loan = Loan()
			loan.loan_id = row['LOAN_ID']
			loan.last_updated = datetime.now()
			loan.principal_balance = row['PBAL_BEG_PERIOD']
			loan.status = row['PERIOD_END_LSTAT']
			loan.as_of_date = row['MONTH']
			loan.interest_rate = row['InterestRate']
			loan.issue_dt = row['IssuedDate']
			loan.payment_amt = row['DUE_AMT']
			loan.dti = row['dti']
			loan.state = row['State']
			loan.home_ownership = row['HomeOwnership']
			loan.monthly_income = row['MonthlyIncome']
			loan.earliest_credt = row['EarliestCREDITLine']
			loan.open_credit_lines = row['OpenCREDITLines']
			loan.total_credit_lines = row['TotalCREDITLines']
			loan.revolving_bal = row['RevolvingCREDITBalance']
			loan.revolving_util = row['RevolvingLineUtilization']
			loan.inquiries_6m = row['Inquiries6M']
			loan.dq_2_yrs= row['DQ2yrs']
			loan.mths_since_dq = row['MonthsSinceDQ']
			loan.pub_rec = row['PublicRec']
			loan.mts_since_last_rec = row['MonthsSinceLastRec']
			loan.emp_length = row['EmploymentLength']
			loan.current_policy = row['currentpolicy']
			loan.grade = row['grade']
			loan.term = row['term']
			loan.fico_band = row['APPL_FICO_BAND']
			loan.vintage = row['VINTAGE']
			loan.recovery = row['PCO_RECOVERY']
			loan.collection_fee = row['PCO_COLLECTION_FEE']
			loan.policy_code = row['policy_code']
			cashflow = LoanCashflow()
			cashflow.loan_id=row['LOAN_ID']
			cashflow.last_updated=datetime.now()
			cashflow.bop_principal=row['PBAL_BEG_PERIOD']
			cashflow.prin_paid=row['PRNCP_PAID']
			cashflow.int_paid=row['INT_PAID']
			cashflow.fee_paid=row['FEE_PAID']
			cashflow.due_amt=row['DUE_AMT']
			cashflow.rec_amt=row['RECEIVED_AMT']
			cashflow.rec_date=datetime.strptime('%b%d', row['RECEIVED_D'])
			cashflow.due_date=datetime.strptime('%b%y', row['MONTH'])
			cashflow.days_late=(cashflow.due_date - cashflow.rec_date).days
			cashflow.eop_status=row['PERIOD_END_LSTAT']
			cashflow.as_of_date=row['MONTH']
			cashflow.eop_principal=row['PBAL_END_PERIOD']
			csahflow.mob=row['MOB']
			cashflow.co=row['CO']
			cashflow.co_amt=row['CO_AMT']
			yield loan, cashflow