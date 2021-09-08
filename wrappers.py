import time
import datetime

def timer(func):
	""" Prints the time taken to complete a function call to the console. """
	def timefunc(*args, **kwargs):
		start_time = time.time()
		output = func(*args, **kwargs)
		print("\nFinished in %s" % (str(datetime.timedelta(seconds=time.time()-start_time))))
		return output
	return timefunc

def roundAll(func):
	""" Rounds every float in the array returned by wrapped function """
	#round every item in a list automatically
	def roundRapper(*args, **kwargs):
		return [round(x, 3) for x in func(*args, **kwargs)]
	return roundRapper