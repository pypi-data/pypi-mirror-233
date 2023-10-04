import uasyncio,usocket
from.import logging
async def _handler(socket,ip_address):
	C=socket
	while True:
		try:yield uasyncio.core._io_queue.queue_read(C);B,D=C.recvfrom(256);A=B[:2];A+=b'\x81\x80';A+=B[4:6]+B[4:6];A+=b'\x00\x00\x00\x00';A+=B[12:];A+=b'\xc0\x0c';A+=b'\x00\x01\x00\x01';A+=b'\x00\x00\x00<';A+=b'\x00\x04';A+=bytes(map(int,ip_address.split('.')));C.sendto(A,D)
		except Exception as E:logging.error(E)
def run_catchall(ip_address,port=53):B=ip_address;logging.info('> starting catch all dns server on port {}'.format(port));A=usocket.socket(usocket.AF_INET,usocket.SOCK_DGRAM);A.setblocking(False);A.setsockopt(usocket.SOL_SOCKET,usocket.SO_REUSEADDR,1);A.bind(usocket.getaddrinfo(B,port,0,usocket.SOCK_DGRAM)[0][-1]);C=uasyncio.get_event_loop();C.create_task(_handler(A,B))