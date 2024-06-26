
## Summary

A program web server that handles http requests from a client and returns an HTTP response along with requested content if content is available. 

### Included files
- server code: 	webserver.py
- client code: 	webclient.py
- file: 		HelloWorld.html
- file: 		404 #sent as response when client request file not found


### Usage
First run the server and then run the client. 

To star the server: 
	python webserver.py

To start client and make a request
	python webclient.py <serverhost> <serverport> <filename>.

	example: 
	python webclient.py localhost 65015 helloworld.html


To make a request from the browser: 
	```http://<serverhost>:<port>/<filename>```

To make a request using a command line: 
```curl http://<serverhost>:<port>/<filename>```

## Additional info
if filename is present in server directory, the server will send an 'HTTP1.1/ 200 OK' header along with the payload
if file is not present in server directory, the servier will send a 'HTTP1.1/ 404 Not Found' header to the client

### References: 
- https://docs.python.org/3/library/socket.html
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
- https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
- https://www.youtube.com/watch?v=FGdiSJakIS4
