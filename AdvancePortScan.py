#!/usr/bin/python3

# Created by Venujan Malaiyadni
# Lets connect -> https://www.linkedin.com/in/venujan-malaiyandi-924381227/

# optparse lib is used to pass flags into the script, just like other cli tools
# socket lib is used to connect to specific ports in the host
# threading lib is used to scan multiple ports at the same time
# colored lib is used to format for easier identification
import optparse
from socket import * 
from threading import * 
from termcolor import colored

# Tries to connect to the given port of the IP using TCP and IPv4 address
# When Success, returns a green color formated output
# When Failed, returns a red color formated output
def connectScan(trtIP, trtPort):
	try:
		sock = socket(AF_INET, SOCK_STREAM)
		sock.connect((trtIP, trtPort))
		print(colored('[+] %d / TCP open' %trtPort, 'green'))
	except:
		print(colored('[-] %d / TCP closed' %trtPort, 'red'))
	finally:
		sock.close()

# Looks up host name if given IP 
# Looks up host IP if given name
# declares the default time out as 1 sec
# Uses mutlithreading within loop to prevent the delay of the loop, by calling separate fucntions to check for port status while the loop proceeds.
# Takes in host name or IP and Port as parameter
def startPort(trtHost, trtPorts):
	try:
		trtIP = gethostbyname(trtHost)
	except:
		print('Uknown Host %s' %trtHost)
	try:
		trtNme = gethostbyaddr(trtIP)
		print('Scan result for %s' %trtNme[0])
	except:
		print('Scan result for %s' %trtIP)

	setdefaulttimeout(1)
	for trtPort in trtPorts:
		thr = Thread(target=connectScan, args=(trtIP, int(trtPort)))
		thr.start()

# Starts the parser to pass host information and port number
# -t flag is used to pass the host ip or name
# -p flag is used to pass single port or many ports, separated by comma
# Applies simple validation to redirect to usage information if success
# Passes the host name or ip and port to startPort function
def startParser():
	parser = optparse.OptionParser('[*] Usage of the script : ' + '-t <target ip or name> -p <target port(s)>')
	parser.add_option('-t', dest='trtHost', type='string', help='mention target host')
	parser.add_option('-p', dest='trtPort', type='string', help='mention target ports separated by \",\"')
	(options, arg) = parser.parse_args()
	trtHost = options.trtHost
	trtPorts = str(options.trtPort).split(',')
	if (trtHost == None) | ( trtPorts[0] == None):
		print(parser.usage)
		exit(0)
	startPort(trtHost, trtPorts)


# main 
startParser()


