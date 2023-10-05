__version__='0.0.2'
import gc,os,machine
gc.threshold(50000)
from.import logging
remote_mount=False
try:os.statvfs('.')
except:remote_mount=True
def get_ip_address():
	import network as A
	try:return A.WLAN(A.STA_IF).ifconfig()[0]
	except:return
def is_connected_to_wifi():import network as A,time;B=A.WLAN(A.STA_IF);return B.isconnected()
def connect_to_wifi(ssid,password,timeout_seconds=30):
	import network as A,time as D;E={A.STAT_IDLE:'idle',A.STAT_CONNECTING:'connecting',A.STAT_WRONG_PASSWORD:'wrong password',A.STAT_NO_AP_FOUND:'access point not found',A.STAT_CONNECT_FAIL:'connection failed',A.STAT_GOT_IP:'got ip address'};B=A.WLAN(A.STA_IF);B.active(True);B.connect(ssid,password);G=D.ticks_ms();C=B.status();logging.debug(f"  - {E[C]}")
	while not B.isconnected()and D.ticks_ms()-G<timeout_seconds*1000:
		F=B.status()
		if C!=F:logging.debug(f"  - {E[C]}");C=F
		D.sleep(.25)
	if B.status()==A.STAT_GOT_IP:return B.ifconfig()[0]
def access_point(ssid,password=None):
	B=password;import network as C;A=C.WLAN(C.AP_IF);A.config(essid=ssid)
	if B:A.config(password=B)
	else:A.config(security=0)
	A.active(True);return A