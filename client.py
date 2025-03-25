from socket import *
import argparse


def main():
	'''
	Requesting resource from IP and port from command line and prints response.
	Arguments:
	-i : IP address
	-p : port
	-f : resource to request, default is '/'
	'''
	parser = argparse.ArgumentParser(description='simple args')

	# Adding command line argument options for ip, port and resource
	parser.add_argument("-i", "--ip", help="IPv4 address in format: 255.255.255.255", type=str, required=True)
	parser.add_argument("-p", "--port", help="Port, write int", type=int, required=True)
	parser.add_argument("-f", "--resource", help="Resource to request, not required", type=str, default='/')
	args = parser.parse_args()

	# Creating socket to communicate through (IPv4 TCP)
	clientSocket = socket(AF_INET, SOCK_STREAM)

	# Exception handling in case socket can not connect with IP and port
	try:
		# Connecting socket to argument IP and port
		clientSocket.connect((args.ip, args.port))
	except:
		print("Client socket could not be created. Server IP or port could be of fault")
		exit()
	
	# Formating HTTP GET request with resource (default = '/') 
	message = "GET " + args.resource + " HTTP/1.1\r\n"
	message += "Content-Type: text/html; charset=UTF-8\r\n\r\n"

	# Sending encoded message through socket
	clientSocket.send(message.encode())

	# Decoding received data from server
	recievedData = clientSocket.recv(1024).decode()

	print(recievedData)

	# Closing up socket
	clientSocket.close()

main()