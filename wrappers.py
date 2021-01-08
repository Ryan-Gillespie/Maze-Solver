import time
import datetime

def timer(func):
	def timefunc(*args, **kwargs):
		start_time = time.time()
		output = func(*args, **kwargs)
		print("\nFinished in %s" % (str(datetime.timedelta(seconds=time.time()-start_time))))
		return output
	return timefunc

def optional_arg_decorator(fn):
    def wrapped_decorator(*args):
        if len(args) == 1 and callable(args[0]):
            return fn(args[0])
        else:
            def real_decorator(decoratee):
                return fn(decoratee, *args)
            return real_decorator
    return wrapped_decorator

@optional_arg_decorator
def log(func, n_file = 'log.txt'):
	#log the output of a function
	def log_wrapper(*args, **kwargs):
		output = func(*args, **kwargs)
		with open(n_file, "a") as logFile:
			logFile.write('\n' + str(output))
		return output
	return log_wrapper

def roundAll(func):
	#round every item in a list automatically
	def roundRapper(*args, **kwargs):
		return [round(x, 3) for x in func(*args, **kwargs)]
	return roundRapper