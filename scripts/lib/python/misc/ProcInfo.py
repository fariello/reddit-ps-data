from datetime import datetime as dt
import os
import __main__ as main

# I just like having a class with "my" info
class ProcInfo:
	# Not super precise, but goot enough for government work.
	_t0 = dt.now()
	_cwd = os.getcwd()
	SECS_PER_MINUTE = 60
	SECS_PER_HOUR = 3600
	SECS_PER_DAY = SECS_PER_HOUR * 24
	SECS_PER_WEEK = SECS_PER_DAY * 7
	SECS_PER_YEAR = SECS_PER_DAY * 365.25
	SECS_PER_MONTH = SECS_PER_YEAR / 12
	KILO = 1000
	MEGA = 1000000
	GIGA = 1000000000
	TERA = 1000000000000
	PETA = 1000000000000000
	EXA  = 1000000000000000000

	def init_class(self):
		pre = "pico nano micro milli n kilo mega giga tera peta exa zetta yotta".split()
		ProcInfo.prefixes = pre
		start = -12
		ProcInfo.pre_min = 1.0 * 10**start
		ProcInfo.pre_max = ProcInfo.pre_min
		ProcInfo.prefix2val = {}
		ProcInfo.val2long = {}
		ProcInfo.val2short = {}
		ProcInfo.magnitutes = []
		for prefix in pre:
			short = prefix[0].upper()
			current = 1.0 * 10**start
			ProcInfo.pre_max = current
			ProcInfo.magnitutes.append(current)
			ProcInfo.prefix2val[prefix] = current
			ProcInfo.prefix2val[short] = current
			ProcInfo.val2long[current] = prefix
			ProcInfo.val2short[current] = short
			start += 3
			pass
		pass

	def __init__(self,min_tick_seconds=1.0,min_ticks=10000):
		#print(['ProcInfo',self,args])
		self.t0 = ProcInfo._t0
		self.initial_dir = ProcInfo._cwd
		# This is the "real" filename. If it was called with a symlink, this
		# will point to the target file not the symlink
		self.real_filename = os.path.realpath(main.__file__)
		# This is the filename of the called script which may not be the same
		# as the "real" filename
		self.filename = os.path.abspath(main.__file__)
		self.basename = os.path.basename(main.__file__)
		self.dir = os.path.dirname(os.path.abspath(main.__file__))
		self.timestamp = self.t0.strftime("%Y%m%d-%H%M%S")
		self.timestr = self.t0.strftime("%Y-%m-%d-%H:%M:%S")
		self.unique_logfilename = f"{self.basename}-{self.timestamp}-{os.getpid()}.log"
		self.min_tick_seconds = min_tick_seconds
		self.min_ticks = min_ticks
		self.last_tick = None
		self.init_class()
		pass

	def now(self):
		return dt.now()

	def elapsed(self,t0=None,tn=None):
		if tn is None:
			tn = self.now()
			pass
		if t0 is None:
			t0 = self.t0
			pass
		return (tn - t0).total_seconds()

	def pbytes(self,num):
		if num >= ProcInfo.PETA:
			return "%0.2fPB" %(num / ProcInfo.PETA)
		if num >= ProcInfo.TERA:
			return "%0.2fTB" %(num / ProcInfo.TERA)
		if num >= ProcInfo.GIGA:
			return "%0.2fGB" %(num / ProcInfo.GIGA)
		if num >= ProcInfo.MEGA:
			return "%0.2fMB" %(num / ProcInfo.MEGA)
		if  num >= ProcInfo.KILO:
			return "%0.2fKB" %(num / ProcInfo.KILO)
		return "%3s Bytes" %(num)

	def pnum(self,num):
		if num >= ProcInfo.PETA:
			return "%0.2fP" %(num / ProcInfo.PETA)
		if num >= ProcInfo.TERA:
			return "%0.2fT" %(num / ProcInfo.TERA)
		if num >= ProcInfo.GIGA:
			return "%0.2fG" %(num / ProcInfo.GIGA)
		if num >= ProcInfo.MEGA:
			return "%0.2fM" %(num / ProcInfo.MEGA)
		if  num >= ProcInfo.KILO:
			return "%0.2fK" %(num / ProcInfo.KILO)
		return "%3s " %(num)

	def psecs(self, secs=None):
		if secs is None:
			secs = self.elapsed()
			pass
		if secs >= ProcInfo.SECS_PER_YEAR:
			secs = secs / ProcInfo.SECS_PER_YEAR
			return f"{secs:0.2f} Years"
		if secs >= ProcInfo.SECS_PER_MONTH:
			secs = secs / ProcInfo.SECS_PER_MONTH
			return f"{secs:0.2f} Months"
		if secs >= ProcInfo.SECS_PER_WEEK:
			secs = secs / ProcInfo.SECS_PER_WEEK
			return f"{secs:0.2f} Weeks"
		if secs >= ProcInfo.SECS_PER_DAY:
			secs = secs / ProcInfo.SECS_PER_DAY
			return f"{secs:0.2f} Days"
		if secs >= ProcInfo.SECS_PER_HOUR:
			secs = secs / ProcInfo.SECS_PER_HOUR
			return f"{secs:0.2f} Hours"
		if secs >= ProcInfo.SECS_PER_MINUTE:
			secs = secs / ProcInfo.SECS_PER_MINUTE
			return f"{secs:0.2f} Minutes"
		return f"{secs:0.2f} Secs"

	def rate(self,count,tn=None,t0=None,total=None,append=""):
		secs = self.elapsed(tn,t0)
		rate = count / secs
		if total is not None:
			secs_remain = (total - count) / rate
			percent = f"{count * 100 / total:0.2f}"
			estimate = self.psecs(secs_remain)
			estimate = f" ({self.pnum(count)} of {self.pnum(total)} {percent}% ~ {estimate} Remaining)"
		else:
			estimate = ""
			pass
		if rate <= 1.0 / ProcInfo.SECS_PER_YEAR:
			rate = rate * ProcInfo.SECS_PER_YEAR
			unit = "Year"
		elif rate <= 1.0 / ProcInfo.SECS_PER_MONTH:
			rate = rate * ProcInfo.SECS_PER_MONTH
			unit = "Month"
		elif rate <= 1.0 / ProcInfo.SECS_PER_WEEK:
			rate = rate * ProcInfo.SECS_PER_WEEK
			unit = "Week"
		elif rate <= 1.0 / ProcInfo.SECS_PER_HOUR:
			rate = rate * ProcInfo.SECS_PER_HOUR
			unit = "Hour"
		elif rate <= 1.0 / ProcInfo.SECS_PER_MINUTE:
			rate = rate * ProcInfo.SECS_PER_MINUTE
			unit = "Minute"
		elif rate >= ProcInfo.KILO:
			rate = self.pnum(rate)
			return f"{rate}/Sec{estimate}"
		else:
			unit = "Second"
			pass
		return f"{rate:0.2f}/{unit}{estimate}"

	def get():
		global me
		return me
	pass
me = ProcInfo()
