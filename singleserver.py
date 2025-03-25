from socket import *
import sys

def main():
	'''
	Setting up server socket, calling handleSocket() and closing the socket again
	'''
	serverIp = '127.0.0.1'
	serverPort = 8000

	# Creating server socket with IPv4 (AF_INET) and TCP (SOCK_STREAM)
	serverSocket = socket(AF_INET, SOCK_STREAM)

	# Binding the socket to IP and port. Exception handling in case port
	#  is already in use.
	try:
		serverSocket.bind((serverIp, serverPort))
	except:
		print("Server could not bind to", serverIp, serverPort)
		sys.exit()

	while True:
		try:
			# Listening for incomming TCP on created socket. Queue for 1.
			serverSocket.listen(1)
			print("Ready to serve...")

			# Waiting for connection

			# When TCP arrived its accepted and given its own socket.
			connectionSocket, addr = serverSocket.accept()
			print("Printer serving addr:", addr)

			# Handling client message and response
			handleClient(connectionSocket)

		# Closing server with CTRL+C (not perfect, send a new request as well)
		except KeyboardInterrupt:
			print("KeyboardInterrupt, closing down server")
			break

		except:
			print("Something went wrong, closing down server")

	# Closing down after communication
	serverSocket.close()
	print("Server socket closed")
	sys.exit()


def handleClient(connectionSocket):
	'''
	Handles GET request and returns requested file's content if found file.
	Returns 404 Not Found if otherwise. 
	Closes down socket after communication.
	Arguments:
	connectionSocket: returned socket from accepted TCP communication.
	'''

	# Decode message recieved
	message = connectionSocket.recv(1024).decode()
	print(message)

	# Exception handling in case requested file does not exsist
	try:
		# Format filename for search, if no file specified open index.html
		filename = message.split()[1]
		if filename == '/':
			filename = 'index.html'
		elif filename.startswith('/'):
			filename = filename[1:]

		# Open and read file from disk and save in variable data	
		data = open(filename, 'r').read()

		# Add header to data
		outputdata = "HTTP/1.1 200 OK\r\n"
		outputdata += "Content-Type: text/html; charset=UTF-8\r\n"
		outputdata += "\r\n"
		outputdata += data

		# Sending encoded HTTP response back through connection socket
		connectionSocket.send(outputdata.encode())

	except IOError:
		print("Could not find file:", filename)

		# Returning HTTP 404 Not Found with header
		outputdata = "HTTP/1.1 404 Not Found\r\n"
		outputdata += "Content-Type: text/html; charset=UTF-8\r\n\r\n"
		outputdata += "<div>404 NOT FOUND</div>\r\n"

		connectionSocket.send(outputdata.encode())

	finally:
		# CLosing socket either way
		connectionSocket.close()
		print("Client socket closed")

main()