from datetime import date, timedelta

leap_years=[x for x in range(1980, 2100, 4)]

weekends=[6,7]

quarters = {1:[1,2,3], 2:[4,5,6], 3:[7,8,9], 4:[10,11,12]}

def addMonths(dt, months=1):
	dt1=''
	try:
		dt1 = date(dt.year, dt.month+months, dt.day)
	except:
		try:
			dt1 = date(dt.year, dt.month+months, dt.day-1)
		except:
			try:
				dt1 = date(dt.year, dt.month+months, dt.day-2)
			except:
				dt1 = date(dt.year, dt.month+months, dt.day-3)
	return dt1

def checkBusinessDay(dt):
	weekday = dt.weekday()
	if weekday not in weekends:
		return True
	else:
		return False
	
def getSettleDate(dt, convention='follow'):
	biz_day = checkBusinessDay(dt)
	if not biz_day:
		diff = 8-dt.weekday()
		if convention == 'follow':
			dt1 = date(dt.year, dt.month, dt.day + diff)
			return dt1
		if convention == 'modfol':
			dt1 = date(dt.year, dt.month, dt.day + diff)
			if dt1.month != dt.month:
				dt1 = date(dt.year, dt.month, dt.day + 5-dt.weekday())
			return dt1
		else:
			print('Convetion of ' + str(convention) + ' Not Valid')
			raise Exception
	else:
		return dt