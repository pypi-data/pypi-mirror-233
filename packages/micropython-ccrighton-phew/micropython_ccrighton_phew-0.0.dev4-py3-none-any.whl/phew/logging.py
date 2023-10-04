import machine,os,gc
log_file='log.txt'
LOG_INFO=1
LOG_WARNING=2
LOG_ERROR=4
LOG_DEBUG=8
LOG_EXCEPTION=16
LOG_ALL=LOG_INFO|LOG_WARNING|LOG_ERROR|LOG_DEBUG|LOG_EXCEPTION
_logging_types=LOG_ALL
_log_truncate_at=11*1024
_log_truncate_to=8*1024
def datetime_string():A=machine.RTC().datetime();return'{0:04d}-{1:02d}-{2:02d} {4:02d}:{5:02d}:{6:02d}'.format(*A)
def file_size(file):
	try:return os.stat(file)[6]
	except OSError:return
def set_truncate_thresholds(truncate_at,truncate_to):global _log_truncate_at;global _log_truncate_to;_log_truncate_at=truncate_at;_log_truncate_to=truncate_to
def enable_logging_types(types):global _logging_types;_logging_types=_logging_types|types
def disable_logging_types(types):global _logging_types;_logging_types=_logging_types&~types
def truncate(file,target_size):
	H=b'\n';G='.tmp';B=file;I=file_size(B);C=I-target_size
	if C<=0:return
	with open(B,'rb')as D:
		with open(B+G,'wb')as E:
			while C>0:A=D.read(1024);C-=len(A)
			F=max(A.find(H,-C),A.rfind(H,-C))
			if F!=-1:E.write(A[F+1:])
			while True:
				A=D.read(1024)
				if not A:break
				E.write(A)
	os.remove(B);os.rename(B+G,B)
def log(level,text):
	B=datetime_string();A='{0} [{1:8} /{2:>4}kB] {3}'.format(B,level,round(gc.mem_free()/1024),text);print(A)
	with open(log_file,'a')as C:C.write(A+'\n')
	if _log_truncate_at and file_size(log_file)>_log_truncate_at:truncate(log_file,_log_truncate_to)
def info(*A):
	if _logging_types&LOG_INFO:log('info',' '.join(map(str,A)))
def warn(*A):
	if _logging_types&LOG_WARNING:log('warning',' '.join(map(str,A)))
def error(*A):
	if _logging_types&LOG_ERROR:log('error',' '.join(map(str,A)))
def debug(*A):
	if _logging_types&LOG_DEBUG:log('debug',' '.join(map(str,A)))
def exception(*A):
	if _logging_types&LOG_EXCEPTION:log('exception',' '.join(map(str,A)))