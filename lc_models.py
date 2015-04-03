import math
import settings
from peewee import *
from playhouse.db_url import connect
import date_util
import logging
logger = logging.getLogger('peewee')
logger.setLevel(settings.log_level)
logger.addHandler(logging.StreamHandler())

env_string = 'dev'
env = settings.env[env_string]
db_type = env['db_type']
#db_string = env['db_connect_string']
db_host = env['db_host']
db_port = env['db_port']
db_user = env['db_user']
db_pword = env['db_pword']
db_name = env['db_name']



db=''

class BaseModel(Model):
	class Meta:
		database = db


class Loan(BaseModel):
	last_updated = DateTimeField()
	loan_id = IntegerField()
	principal_balance = FloatField(null=True)
	### Additional Fields Not in Payment File###
	loan_amt=FloatField(null=True)
	borrower_id=IntegerField(null=True)
	######
	status = CharField(null=True)
	as_of_date=DateField(null=True)
	interest_rate = FloatField(null=True)
	issue_dt = DateField(null=True)
	payment_amt = FloatField(null=True)
	dti = FloatField(null=True)
	state = CharField(null=True)
	home_ownership = CharField(null=True)
	monthly_income=FloatField(null=True)
	earliest_credt = DateField(null=True)
	open_credit_lines=IntegerField(null=True)
	total_credit_lines=IntegerField(null=True)
	revolving_bal=FloatField(null=True)
	revolving_util = FloatField(null=True)
	inquiries_6m=IntegerField(null=True)
	dq_2_yrs=IntegerField(null=True)
	mths_since_dq = IntegerField(null=True)
	pub_rec = IntegerField(null=True)
	mths_since_last_rec=IntegerField(null=True)
	emp_length=IntegerField(null=True)
	current_policy=IntegerField(null=True)
	grade=CharField(null=True)
	term=IntegerField(null=True)
	fico_band=CharField(null=True)
	vintage=CharField(null=True)
	recovery=FloatField(null=True)
	collection_fee=FloatField(null=True)
	policy_code=IntegerField(null=True)
	
	
	def calcPayment(self, overwrite=False):
		a = self.loan_amt
		n = self.term
		i = self.interest_rate/12
		pmt = a*((i*(1+i)**n)/(((1+i)**n)-1))
		if overwrite:
			self.payment_amt = pmt
		return pmt
		
	def generateCashflows(self):
		flows = []
		last_prin = self.loan_amt
		pmt = self.payment_amt
		rt = self.interest_rate/12
		for i in range(0, self.term):
			flow = LoanCashFlow()
			flow.loan_id = self.loan_id
			flow.bop_principal = last_prin
			flow.int_paid = rt*last_prin
			flow.prin_paid = pmt-flow.int_paid
			flow.fee_paid=0
			flow.due_amt = pmt
			flow.rec_amt=pmt
			flow.rec_date = date_util.getSettleDate(date_util.addMonths(self.issue_dt, i))
			flow.days_late=0
			flow.eop_status='Current'
			flow.eop_principal = flow.bop_principal - flow.prin_paid
			mob = i
			co=0
			co_amt=0
			last_prin = flow.eop_principal
			flows.append(flow)
		return flows
		
	def order(self, amt, portfolio=''):
		order = {}
		order['loanId'] = self.loan_id
		order['requestedAmount'] = amt
		order['portfolioId'] = portfolio
		return order
			


class LoanCashflow(BaseModel):
	loan_id = IntegerField()
	last_updated = DateTimeField()
	bop_principal=FloatField()
	prin_paid = FloatField()
	int_paid=FloatField()
	fee_paid=FloatField()
	due_amt=FloatField()
	rec_amt=FloatField()
	rec_date=DateField()
	days_late=IntegerField()
	eop_status=CharField()
	as_of_date=DateField()
	eop_principal=FloatField()
	mob=IntegerField()
	co=FloatField()
	co_amt=FloatField()
	

if db_type == 'mysql':	
	logging.debug('Connecting to MySQL DB ' + db_name + ' on host ' + str(db_host) + ' and port ' + str(db_port) + '. Username is ' + db_user + ' Password is ' + db_pword)
	db = MySQLDatabase(db_name, host=db_host, port=db_port, user=db_user, passwd=db_pword)
else:
	logging.exception('Database Type of ' + str(db_type) + ' Not Configured!')
	#raise Exception
try:
	db.create_tables([Loan, LoanCashflow])
except:
	print('Cannot Create Tables')
	
	pass