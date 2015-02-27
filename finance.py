
def getCashflows(issue_dt, mat_dat, principal, rate, freq, type='loan'):
	if type == 'loan':
		cashflows = []
		

def getPV(n, amt, i='', pmt=''):
	resp = ''
	if n=='' and (i== '' or amt == '' or pmt ==''):
		print('Error: n and another variable are blank')
		print('Can only solve for one unknown variable')
	
	elif pmt == '':
		resp = (i*amt)/(1-(1+i)^-n)
	return resp
		
		