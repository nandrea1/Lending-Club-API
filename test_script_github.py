import test_cases as test
import traceback
from lending_club import LendingClub

authorization = 'Dummy Code'
investor_id = 'Dummy ID'
lc = LendingClub(authorization, investor_id)

execute_cases =['getAccountSummary', 'getPortfolios', 'getOwnedNotes', 'getDetailedOwnedNotes', 'getPendingTransfers', 'getListedLoans', 'createPortfolio']

passed_cases = []
failed_cases =[]

fail_count = 0
pass_count = 0
run_count = len(execute_cases)

print('Executing %s Test Cases' % (len(execute_cases)))

for case in execute_cases:
	print('Executing %s Test Case' % (case))
	func = getattr(test, case)
	try:
		func(lc)
		print('Case Passed!')
		pass_count += 1
		passed_cases.append(case)
	except Exception as e:
		print('ERROR: Case Failed!')
		print(traceback.format_exc())
		fail_count +=1
		failed_cases.append(case)
		
print('%s Test Cases Run. %s Passed and %s Failed'% (run_count, pass_count, fail_count))
if fail_count >0:
	print('Failed Cases:')
	print(*failed_cases, sep='\n')