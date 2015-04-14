from lending_club import LendingClub

class LendingClubUtil():

	auth=''
	investor_id=''
	logger=''
	lc = ''
	max_notes_per_loan=1
	dollars_to_invest=25


	def __init__(self, auth, investor_id, logger='', max_notes=1,dollars=25):
		self.auth = auth
		self.investor_id = investor_id
		self.max_notes_per_loan=max_notes
		self.dollars_to_invest=dollars

		if logger !='':
			self.logger=logger
		else:
			self.logger = logging.getLogger('LendingClubUtil')
			self.logger.setLevel(logging.DEBUG)
		self.lc = LendingClub(self.auth, self.investor_id, self.logger)

	def filterLoans(self, loans, criteria):
			filtered_loans = []
			for loan in loans:
				for criterion in criteria:
						if loan[criterion] in criteria[criterion]:
							filtered_loans.append(loan)
			return filtered_loans
	def getListedLoans(self):
