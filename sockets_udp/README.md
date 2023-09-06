##Summary: 

A program web server that handles http requests from a client and returns an HTTP response along with requested content if content is available. 



#included files

server code: 	server_simple_udp.py
client code: 	client_simple_udp.py
file: 		file.txt #this is a test file


#Protocol Description

The client creates a checksum of the message.
The client sends both the message and the checksum to the server. 
The server receives the message as well as the checksum. It first records the local timestamp when it received the message. The server then prints the date and time, the message, and the received checksum to the screen. Then it calculates the checksum of the received message, prints it, and compares it with the received checksum. If the checksum matches, the server sends the timestamp back to the client. If the checksum does not match, the server reports an error message and acknowledges the client (e.g., value 0). 
    The client receives the response message from the server. If the message is a valid timestamp, print the date and time; otherwise, report an error message (e.g., print "message failed!"). It also calculates and prints the round-trip-time (RTT), in microseconds, from when it sent the message to when it received the response.

#usage

First run the server and then run the client. 

To star the server: 
	python .\server_simple_udp.py <port-number> 
e.g. python .\server_simple_udp.py 65015

To start client and make a request
	python webclient.py <serverhost> <serverport> <filename | text>.

	example: 
	python webclient.py localhost 65015 file.txt
	python webclient.py localhost 65015 "hello"




