import BaseHTTPServer
import SimpleHTTPServer
from SocketServer import ThreadingMixIn
import os
from os import getcwd
import socket
import errno

CURR_DIR = getcwd()


class ThreadingHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass

class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    current_path = CURR_DIR

    # Handle requests
    def do_GET(self):
        # Print request header information
        client_host, client_port = self.client_address
        
        print self.command, self.path, self.request_version
        print client_host + ":" + str(client_port)

        for key in self.headers:
            print key + ":", self.headers[key]
        print "---------------------------------"

        if self.path=="/":
            self.path="/index.html"

        # Check the file extension and set the mimetype

        replyFlag = False
        if self.path.endswith(".html"):
            mimetype='text/html'
            replyFlag = True
        if self.path.endswith(".jpg"):
            mimetype='image/jpg'
            replyFlag = True
        if self.path.endswith(".gif"):
            mimetype='image/gif'
            replyFlag = True
        if self.path.endswith(".js"):
            mimetype='application/javascript'
            replyFlag = True
        if self.path.endswith(".css"):
            mimetype='text/css'
            replyFlag = True

        # Send the static file
        if replyFlag:
            
            try:
                file_path = self.path.lstrip(os.sep)
                f = open(file_path)
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                
            except:
                
                print 'Cannot open:', self.path
                f = open('error.html')
                self.send_response(404)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
        else:
            f = open('error.html')
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        

        return
        # return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        


def get_server(port, remaining_attempts=0, current_path=None):
    Handler = RequestHandler
    if current_path:
        Handler.current_path = current_path
    while remaining_attempts >= 0:
        try:
            httpd = ThreadingHTTPServer(("", port), Handler)
            return httpd
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                remaining_attempts -= 1
                port += 1
            if e[0] == errno.EPIPE:
               # remote peer disconnected
               print "Detected remote disconnect"
            else:
                raise

def main():
    PORT = 8000
    current_path = CURR_DIR

    httpd = get_server(port=PORT, current_path=current_path)
    print "Server running at port:", PORT

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__" :
    main()

